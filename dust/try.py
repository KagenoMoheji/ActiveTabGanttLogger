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

    '''
    [Get PID and its name]
    ・https://githubja.com/giampaolo/psutil
    ・https://psutil.readthedocs.io/en/latest/#process-class
    ●psutilモジュールではアクティブタブは分からなさそう．
    ●psutil: {Windows: OK, MacOS: OK}
    '''
    import psutil
#     for ps in psutil.process_iter():
#         text = """\
# ppid: {ppid}
# pid: {pid}
# name: {name}
# status: {status}
# ============================
# """.format(ppid=ps.ppid(), pid=ps.pid, name=ps.name(), status=ps.status())
#         print(text)
    os = platform.platform(terse=True)
    if "Windows" in os:
        '''
        [Get active window ※Windows10-64bit]
        ●win32guiモジュールのインストールについて
        ・http://blog.livedoor.jp/kmiwa_project/archives/1058907748.html
        ・https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/
        ・https://github.com/mhammond/pywin32/releases
        ・https://stackoverflow.com/questions/42370339/python-3-6-install-win32api
        ・https://github.com/Googulator/pypiwin32
        →Windows10-64bitに向けては，`pip install pypiwin32`を採用
        ●win32系のドキュメント？
        ・http://docs.activestate.com/activepython/2.4/pywin32/win32_modules.html
        ●実装参考
        ・https://www.reddit.com/r/learnpython/comments/90onta/getting_activeforeground_window_title_on_windows/
        ●アクティブタブがchromeだった場合のリンクの取得について
        ・https://stackoverflow.com/questions/11645123/how-do-i-get-the-url-of-the-active-google-chrome-tab-in-windows
        ・https://codeday.me/jp/qa/20190401/509668.html
        →上記リンクはいずれもダメ

        '''
        import win32gui as wg
        import win32process as wp
        import win32com.client as wcli
        # import win32con as wc

        # pids = wp.GetWindowThreadProcessId(w.GetForegroundWindow())
        # print(psutil.Process(pids[-1]))
        recent_active_pid = -1
        try:
            while True:
                # ForegroundWindowのオブジェクト取得=============================================
                fw = wg.GetForegroundWindow()
                # pidの取得=============================================
                # 同じアプリケーションで異なるウィンドウを開いていても同じpidで区別はつかないらしい
                # それだとブラウザ内のページの区別つかないな
                active_pid = wp.GetWindowThreadProcessId(fw)[-1]
                if active_pid != recent_active_pid:
                    # タブ遷移時刻を取得=============================================
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_pidの更新=============================================
                    recent_active_pid = active_pid
                    # fwの実行ファイル名の取得=============================================
                    active_name = psutil.Process(recent_active_pid).name()
                    # fwの詳細テキストの取得=============================================
                    # 下記の一行でステータスバー(ブラウザならページのタイトル)のテキストを取得できる
                    tab_text = wg.GetWindowText(fw)
                    if "CHROME" in active_name.upper(): # Chromeなら
                        tab_text_list = tab_text.split(" - ")[:-1]
                        tab_text = " - ".join(tab_text_list)

                    # ブラウザならtab_textはURL，それ以外はステータスバー=============================================
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=timestamp,
                        pid=recent_active_pid,
                        active_name=active_name,
                        tab_text=tab_text))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")
    elif "Darwin" in os:
        '''
        [Get active window ※MacOS Mojave]
        ・(Win: win32gui, Mac: Appkit)https://stackoverflow.com/a/36419702
        ・(Mac Appkit)https://codeday.me/jp/qa/20190523/885948.html
        ・(Mac向け？xpropやxdotoolのインストールが必要？)https://stackoverflow.com/questions/3983946/get-active-window-title-in-x
        ・(Quartz)https://stackoverflow.com/questions/29814634/what-is-an-alternative-to-win32gui-in-python-2-7-for-mac
        ●Appkit・Quartzモジュールのインストールについて
        ・http://palepoli.skr.jp/wp/2019/01/31/python3-pyobjc/
        ・https://pypi.org/project/pyobjc/
        ・https://pypi.org/project/pyobjc-framework-Quartz/
        ●実装参考
        ・https://developer.apple.com/documentation/appkit/nsworkspace#1965656
        ・https://developer.apple.com/documentation/appkit/nswindow
        ・https://stackoverflow.com/a/36419702
        ・https://stackoverflow.com/questions/28815863/how-to-get-active-window-title-using-python-in-mac/37368813#37368813
        ●アクティブタブがchromeだった場合のリンクの取得について

        '''
        from AppKit import NSWorkspace as nsw
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

        recent_active_pid = -1
        try:
            while True:
                # ForegroundWindowのオブジェクト取得=============================================
                fw = nsw.sharedWorkspace().activeApplication()
                # pidの取得=============================================
                active_pid = fw["NSApplicationProcessIdentifier"]
                if active_pid != recent_active_pid:
                    # タブ遷移時刻を取得=============================================
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_pidの更新=============================================
                    recent_active_pid = active_pid
                    # fwの実行ファイル名の取得=============================================
                    active_name = fw["NSApplicationName"]
                    # fwの詳細テキストの取得=============================================
                    tab_text = ""
                    # 詳細情報を含めたWindowリストを取得
                    cg_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
                    for cg_window in cg_windows:
                        if active_name == cg_window["kCGWindowOwnerName"] and cg_window["kCGWindowName"]:
                            tab_text = cg_window["kCGWindowName"]
                            break
                    # if "CHROME" in active_name.upper(): # Chromeなら

                    # ブラウザならtab_textはURL，それ以外はステータスバー=============================================
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=timestamp,
                        pid=recent_active_pid,
                        active_name=active_name,
                        tab_text=tab_text))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")