from modules.InitProcess import InitProcess
from modules.StrFormatter import StrFormatter
from modules.Observer import Observer
from modules.Logger import Logger

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
        alone(os)
    elif mode == "Observer":
        observer(os, uuid)
    elif mode == "Logger":
        logger(os, uuid)
    '''
    elif mode == "Plotter":
        plotter(os)
    '''

    # Exit the loop above
    # Close process here? or in functions below?

def alone(os):
    print("This mode is Alone")

def observer(os, uuid):
    print("This mode is Observer")

def logger(os, uuid):
    print("This mode is Logger")

'''
def plotter():
    pass
'''



if __name__ == "__main__":
    '''
    ここの処理を実行する`pipenv run python app.py`は，お試し実装の場とする．
    コメントも日本語OKで．

    [メモ]
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
    ・拡張ディスプレイで，タイマー(ブラウザ)を映すことやってみるか???????????????????????????????
    '''
    # main()
    import platform
    from datetime import datetime
    import time
    import psutil

    os = platform.platform(terse=True)
    recent_active_name = "START!"
    recent_tab_text = ""
    if "Windows" in os:
        import win32gui as wg
        import win32process as wp
        import win32com.client as wcli

        try:
            while True:
                # ForegroundWindowのオブジェクト取得
                fw = wg.GetForegroundWindow()
                # pidの取得
                active_pid = wp.GetWindowThreadProcessId(fw)[-1]
                # fwの実行ファイル名の取得
                active_name = psutil.Process(active_pid).name()
                # fwのステータスバーのテキスト取得
                tab_text = wg.GetWindowText(fw)
                if recent_active_name != active_name.upper():
                    # タブ遷移時刻を取得
                    switched_time = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_nameの更新(大文字比較に備えておく)
                    recent_active_name = active_name.upper()
                    # ブラウザの場合に，取得したステータスバーのテキストの加工
                    if "CHROME" in active_name.upper(): # Chromeなら
                        tab_text_list = tab_text.split(" - ")[:-1]
                        tab_text = " - ".join(tab_text_list)
                        recent_tab_text = tab_text

                    # 確認
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=switched_time,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=tab_text))
                elif "CHROME" in active_name.upper(): # ブラウザ内切り替えがあるかもなので
                    tab_text_list = tab_text.split(" - ")[:-1]
                    tab_text = " - ".join(tab_text_list)
                    if recent_tab_text != tab_text: # ステータスバーのページタイトルが違ってたら
                        switched_time = datetime.now().strftime("%H:%M:%S.%f")
                        recent_tab_text = tab_text

                        print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=switched_time,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=tab_text))

                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")
    elif "Darwin" in os:
        from AppKit import NSWorkspace as nsw
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

        try:
            while True:
                # ForegroundWindowのオブジェクト取得
                fw = nsw.sharedWorkspace().activeApplication()
                # pidの取得
                active_pid = fw["NSApplicationProcessIdentifier"]
                # fwの実行ファイル名の取得
                active_name = fw["NSApplicationName"]
                # fwのステータスバーのテキスト取得
                tab_text = ""
                cg_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID) # 詳細情報を含めたWindowリストを取得
                for cg_window in cg_windows:
                    if active_name == cg_window["kCGWindowOwnerName"] and cg_window["kCGWindowName"]:
                        tab_text = cg_window["kCGWindowName"]
                        break
                if recent_active_name != active_name.upper():
                    # タブ遷移時刻を取得
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_nameの更新(大文字比較に備えておく)
                    recent_active_name = active_name.upper()
                    # ブラウザの場合に，取得したステータスバーのテキストの加工
                    if "CHROME" in active_name.upper(): # Chromeなら
                        recent_tab_text = tab_text
                    
                    # 確認
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=timestamp,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=tab_text))
                elif "CHROME" in active_name.upper(): # ブラウザ内切り替えがあるかもなので
                    if recent_tab_text != tab_text: # ステータスバーのページタイトルが違ってたら
                        switched_time = datetime.now().strftime("%H:%M:%S.%f")
                        recent_tab_text = tab_text

                        print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=switched_time,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=tab_text))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")


    



