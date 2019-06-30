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
        alone = Alone(os, uuid)
        alone.run()
    elif mode == "Observer":
        observer = Observer(os, uuid)
        observer.start()
    elif mode == "Logger":
        logger = Logger(uuid)
        plotter = Plotter(uuid)
        logger.run()
        plotter.run()
    elif mode == "Plotter":
        plotter = Plotter()
        plotter.start() # ここでどんな出力モードにするかとかの標準入力を求めてからrun()する
        plotter.run()



# sum_keyboard_cnt = 0
# def on_press(key):
#     global sum_keyboard_cnt
#     sum_keyboard_cnt += 1
#     return False
# def on_release(key):
#     return False

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
    # from pynput.mouse import Controller as mctrl
    from pynput import keyboard
    import threading

    os = platform.platform(terse=True)
    if "Windows" in os:
        '''
        [キーボードの1sごとの打鍵数をカウントする]
        ●pynputで実装
        ・https://stackoverflow.com/a/45592445
        ・https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
        ・上の2つ目のリンクはThread使用だったので適していないと思ったけど，1つ目のリンクで行けた
        '''
        try:
            recent_time = time.time()
            sum_keyboard_cnt = 0
            on_press = lambda key: False
            on_release = lambda key: False 
            while True:
                current_time = time.time()

                # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: # global使う場合
                #     listener.join()

                with keyboard.Listener(on_press=on_press) as listener: # lmbda使って挟む場合
                    listener.join()
                sum_keyboard_cnt += 1
                with keyboard.Listener(on_release=on_release) as listener:
                    listener.join()

                if current_time - recent_time > 1.0: # 1秒程度経ったら
                    recent_time = current_time
                    print(sum_keyboard_cnt)
                    sum_keyboard_cnt = 0
                
        except KeyboardInterrupt:
            print("Exit")
    elif "Darwin" in os:
        try:
            sum_keyboard_cnt = 0
            recent_time = time.time()
            on_press = lambda key: False
            on_release = lambda key: False 
            while True:
                current_time = time.time()
                if current_time - recent_time > 1.0: # 1秒程度経ったら
                    recent_time = current_time
                    print(sum_keyboard_cnt)
                    sum_keyboard_cnt = 0

                with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                    listener.join()
                sum_keyboard_cnt += 1
                with keyboard.Listener(on_release=on_release) as listener:
                    listener.join()
                
        except KeyboardInterrupt:
            print("Exit")



