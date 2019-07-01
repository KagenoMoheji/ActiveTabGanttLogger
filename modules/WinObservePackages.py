from datetime import datetime
import time
import psutil
import win32gui as wg
import win32process as wp

class ActiveTabObserver:
    def __init__(self):
        pass

    def run(self):
        recent_active_tab_text = "START!"
        try:
            while True:
                try:
                    fw = wg.GetForegroundWindow()
                    active_pid = wp.GetWindowThreadProcessId(fw)[-1]
                    # print("pids: {}".format(wp.GetWindowThreadProcessId(fw)))
                    active_name = psutil.Process(active_pid).name()
                    active_tab_text = wg.GetWindowText(fw)
                except (ValueError, psutil.NoSuchProcess):
                    # pid取得が間に合ってなかったら
                    # print("Error: Failed in getting process information")
                    continue
                if recent_active_tab_text != active_tab_text.upper():
                    switched_time = datetime.now().strftime("%H:%M:%S.%f")
                    recent_active_tab_text = active_tab_text.upper()
                    if "CHROME" in active_name.upper():
                        # In Windows10, we have to reshape the tab_text(title) when
                        # active_name is Google Chrome.
                        splitted_active_tab_text = active_tab_text.split(" - ")[:-1]
                        active_tab_text = " - ".join(splitted_active_tab_text)

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