if __name__ == "__main__":
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
            recent_x, recent_y = mouse.position # pyautogui.position()
            while True:
                current_time = time.time()
                x, y = mouse.position # pyautogui.position()
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
            recent_x, recent_y = mouse.position # pyautogui.position()
            while True:
                current_time = time.time()
                x, y = mouse.position # pyautogui.position()
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