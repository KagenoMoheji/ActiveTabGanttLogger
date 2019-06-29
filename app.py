'''
[How to test]
If you have setted the pipenv, start from (3).
Or, if you have installed this CLI, start from (4).
(1)Install pipenv.
`python -m pip install pipenv` or `pip3 install pipenv`
(2)Create virtual python environment with pipenv.
`pipenv --python 3.7`
(3)Install this CLI.
`pipenv run python -m pip install -e .` or `pipenv run pip3 install -e .`
(4)Run CLI.
`pipenv run ganttlogger`
'''

from modules.InitProcess import InitProcess
from modules.StrFormatter import StrFormatter
from modules.Alone import Alone
from modules.Observer import Observer
from modules.Logger import Logger
from modules.Plotter import Plotter

def main():
    '''
    Initial Process
    '''
    # A start of a module 'StrFormatter' for coloring terminal
    strformatter = StrFormatter()
    strformatter.start()
    # Main initialization
    init = InitProcess()
    os, mode, uuid = init.get_init_parameters()
    # print("OS: {}".format(os)) # "w" or "d"

    # Start main process(thread-loop) in accordance with mode
    if mode == "Alone":
        alone = Alone(os)
        alone.run()
    elif mode == "Observer":
        observer = Observer(os, uuid)
        observer.start()
    elif mode == "Logger":
        logger = Logger(uuid)
        plotter = Plotter()
        logger.run()
        plotter.run()
    elif mode == "Plotter":
        plotter = Plotter()
        plotter.start() # ここでどんな出力モードにするかとかの標準入力を求めてからrun()する
        plotter.run()



if __name__ == "__main__":
    '''
    ここの処理を実行する`pipenv run python app.py`は，お試し実装の場とする．
    コメントも日本語OKで．

    ●start()は標準入力や注意書きをターミナルに表示させるとかのrun()を実行する直前の関数，run()はマジ実行(？)

    [メモ]
    ●アクティブタブのステータスバーのテキストの照合によってアクティブタブ遷移を検出
    しているが、Chrome以外はそのテキストは参考のため(ログには書く)で、グラフプロット時は
    実行ファイル名で統合してプロットする。
    ●実際にobserverするとき，長時間稼働して配列(numpy)に格納するデータ数膨大に
    なるから，一定時間(5-10m)経った時にそれまでの配列を別スレッド立ててファイル
    書き出ししつつ元の配列の変数を初期化して再利用する並列処理した方がええのかな．

    ●「デルタt間」のマウス移動ピクセル数・キーボード打鍵数はどう取得したものかな…
    →アクティブタブに対して操作しているかは考えず，普通にマウス移動・キーボード打鍵
    の検出をしていく？
    まぁ最前面に表示するソフトを使うとかの悪者出てきそうだけど無い前提で研究すればいいか．
    →開始時刻をあらかじめ変数に格納してデルタt経ったらマウス移動・キーボード打鍵の
    総和を格納する変数を初期化？
    →そもそもデルタt＝1sとか短めに設定しておいて(最低デルタtにして)データ取得して，
    プロット時に最低デルタt以上の指定で自由な間隔調整ができるようにする？

    ●拡張ディスプレイ・仮想デスクトップでもアクティブタブは認識できてる？
    ・仮想デスクトップだと，デスクトップ別のアクティブタブが選択される状態になる．
    →そこまで気にすることないか？
    →短時間でタブ切り替えされたアプリケーションは，使われないものとして除去するのもアリ
    →ガントチャートプロット時に1sより短かったら切り捨てるとか？
    ・拡張ディスプレイでやってもアクティブタブの単一検出はできた。
    ・拡張ディスプレイで，タイマー(ブラウザ)を映すことやってみるか。休憩時刻確認の時に。
    '''
    # main()
    import platform
    from datetime import datetime
    import time
    import psutil
    import math
    # import pyautogui
    from pynput.mouse import Controller as mctrl

    os = platform.platform(terse=True)
    mouse = mctrl()
    if "Windows" in os:
        '''
        [マウスの移動ピクセル数を1s間隔で検出する]
        ●リアルタイムで動作確認するとき，出力されたログをVSCodeで開いて
        続けてアクションを起こすと更新を見ることができそう.
        ●pyautoguiで実装する(Windows・Mac両対応)
        ・https://qiita.com/hirohiro77/items/78e26a59c2e45a0fe4e3
        ・https://pyautogui.readthedocs.io/en/latest/mouse.html#the-screen-and-mouse-position
        ●pynputで実装する
        ・https://pynput.readthedocs.io/en/latest/mouse.html
        ●win32guiで実装する
        ・https://stackoverflow.com/a/3698659
        ●「1秒間隔」
        ・unix時間の差分で求めるのが良さそう．
        ・datetimeのmicrosecondsでやろうと思ったけど，1000000になる前に0にされるので差分計算できない
        ・https://note.nkmk.me/python-datetime-timedelta-measure-time/
        '''
        # import win32gui as wg
        # import win32process as wp
        # import win32com.client as wcli

        try:
            sum_mouse_move_pxs = 0
            dif_x, dif_y = 0, 0
            recent_time = time.time()
            recent_x, recent_y = mouse.position
            while True:
                current_time = time.time()
                x, y = mouse.position
                if x != recent_x or y != recent_y: # 直前のカーソル座標との違いがあったら
                    dif_x = x - recent_x
                    dif_y = y - recent_y
                    sum_mouse_move_pxs += math.sqrt(dif_x * dif_x + dif_y*dif_y)
                    recent_x, recent_y = x, y

                if current_time - recent_time > 1.0: # 1秒程度経ったら
                    recent_time = current_time
                    print(sum_mouse_move_pxs)
                    sum_mouse_move_pxs = 0
                
        except KeyboardInterrupt:
            print("Exit")
    elif "Darwin" in os:
        '''
        [マウスの移動ピクセル数を1s間隔で検出する]
        ●Windowsと同じくpyautoguiで可能
        ●pyautoguiモジュール使用時のエラー回避例
        ・https://teratail.com/questions/159780
        ●pynputでMacでも使用可能
        ●Quartzでやる場合？
        ・https://stackoverflow.com/questions/281133/how-to-control-the-mouse-in-mac-using-python
        '''
        # from AppKit import NSWorkspace as nsw
        # from Quartz import (
        #     CGWindowListCopyWindowInfo,
        #     kCGWindowListOptionOnScreenOnly,
        #     kCGNullWindowID
        # )

        try:
            sum_mouse_move_pxs = 0
            dif_x, dif_y = 0, 0
            recent_time = time.time()
            recent_x, recent_y = mouse.position
            while True:
                current_time = time.time()
                x, y = mouse.position
                if x != recent_x or y != recent_y: # 直前のカーソル座標との違いがあったら
                    dif_x = x - recent_x
                    dif_y = y - recent_y
                    sum_mouse_move_pxs += math.sqrt(dif_x * dif_x + dif_y*dif_y)
                    recent_x, recent_y = x, y

                if current_time - recent_time > 1.0: # 1秒程度経ったら
                    recent_time = current_time
                    print(sum_mouse_move_pxs)
                    sum_mouse_move_pxs = 0
                
        except KeyboardInterrupt:
            print("Exit")


    



