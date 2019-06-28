
if __name__ == "__main__":
    '''
    ここの処理を実行する`pipenv run python app.py`は，お試し実装の場とする．
    コメントも日本語OKで．

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

    os = platform.platform(terse=True)
    recent_active_tab_text = "START!"
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
                active_tab_text = wg.GetWindowText(fw)
                if recent_active_tab_text != active_tab_text.upper():
                    # タブ遷移時刻を取得
                    switched_time = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_tab_textの更新(大文字比較に備えておく)
                    recent_active_tab_text = active_tab_text.upper()
                    # ブラウザの場合に，取得したステータスバーのテキストの加工
                    if "CHROME" in active_name.upper(): # Chromeなら
                        splitted_active_tab_text = active_tab_text.split(" - ")[:-1]
                        active_tab_text = " - ".join(splitted_active_tab_text)

                    # 確認
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=switched_time,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=active_tab_text))

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
                active_tab_text = ""
                cg_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID) # 詳細情報を含めたWindowリストを取得
                for cg_window in cg_windows:
                    if active_name == cg_window["kCGWindowOwnerName"] and cg_window["kCGWindowName"]:
                        active_tab_text = cg_window["kCGWindowName"]
                        break
                if recent_active_tab_text != active_tab_text.upper():
                    # タブ遷移時刻を取得
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")
                    # recent_active_tab_textの更新(大文字比較に備えておく)
                    recent_active_tab_text = active_tab_text.upper()
                    
                    # 確認
                    print("{time}: {pid}: {active_name}({tab_text})".format(
                        time=timestamp,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=active_tab_text))
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exit")