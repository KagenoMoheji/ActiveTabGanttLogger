from datetime import datetime
import time
import psutil
from AppKit import NSWorkspace as nsw
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

class ActiveTabObserver:
    def __init__(self):
        pass
    
    def run(self):
        recent_active_tab_text = "START!"
        try:
            while True:
                try:
                    fw = nsw.sharedWorkspace().activeApplication()
                    active_pid = fw["NSApplicationProcessIdentifier"]
                    active_name = fw["NSApplicationName"]
                    active_tab_text = ""
                    cg_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
                    for cg_window in cg_windows:
                        if active_name == cg_window["kCGWindowOwnerName"] and cg_window["kCGWindowName"]:
                            active_tab_text = cg_window["kCGWindowName"]
                            break
                except (ValueError, psutil.NoSuchProcess):
                    # pid取得が間に合ってなかったら
                    # print("Error: Failed in getting process information")
                    continue
                if recent_active_tab_text != active_tab_text.upper():
                    switched_time = datetime.now().strftime("%H:%M:%S.%f")
                    recent_active_tab_text = active_tab_text.upper()

                    # このあたりでsum_key_boardで操作する
                    # ログするとか？hand_data()
                    print("ActiveTab[{time}]: {pid}: {active_name}({tab_text})".format(
                        time=switched_time,
                        pid=active_pid,
                        active_name=active_name,
                        tab_text=active_tab_text))
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("ActiveTabObserver.py: KeyboardInterrupt")

    def hand_data(self):
        # キューに格納するか，送信するかはここで
        pass
    def close(self):
        pass



'''
class MouseObserver:
    pass
class KeyboardObserver:
    pass
'''