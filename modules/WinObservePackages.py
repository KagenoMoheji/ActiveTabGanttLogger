import datetime
import psutil
import win32gui as wg
import win32process as wp
import win32com.client as wcli

class ActiveTabObserver:
    def __init__(self):
        pass

    def run(self):
        recent_active_tab_text = "START!"
        try:
            while True:
                fw = wg.GetForegroundWindow()
        except KeyboardInterrupt:
            print("ActiveTabObserver.py: KeyboardInterrupt")

    def close(self):
        pass


'''
class MouseObserver:
    pass
class KeyboardObserver:
    pass
'''