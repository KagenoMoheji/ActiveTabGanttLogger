from datetime import datetime
import time
import psutil
import win32gui as wg
import win32process as wp
import ganttlogger.modules.Global as global_v

class ActiveTabObserver:
    uuid = ""
    data_process = None
    def __init__(self, uuid, is_alone):
        self.uuid = uuid
        if is_alone:
            self.data_process = self.enqueue_data
        else:
            self.data_process = self.send_json

    def run(self):
        try:
            recent_active_tab_text = "START!"
            while not global_v.is_sleeping:
                try:
                    fw = wg.GetForegroundWindow()
                    active_pid = wp.GetWindowThreadProcessId(fw)[-1]
                    active_name = psutil.Process(active_pid).name()
                    active_tab_text = wg.GetWindowText(fw)
                    if recent_active_tab_text != active_tab_text.upper():
                        switched_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
                        recent_active_tab_text = active_tab_text.upper()
                        splitted_active_tab_text = active_tab_text.split(" - ")
                        if len(splitted_active_tab_text) > 1:
                            # Remove application name from tab text
                            active_tab_text = " - ".join(splitted_active_tab_text[:-1])

                        self.data_process(switched_time, active_name, active_tab_text)
                        # print("ActiveTab[{time}]: {pid}: {active_name}({tab_text})".format(
                        #     time=switched_time,
                        #     pid=active_pid,
                        #     active_name=active_name,
                        #     tab_text=active_tab_text))
                    time.sleep(0.001)
                except (ValueError, psutil.NoSuchProcess):
                    # If not in time to get pid
                    # print("Warning: Failed in getting process information")
                    continue
                except KeyboardInterrupt:
                    continue
            # Output the last log
            switched_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
            splitted_active_tab_text = active_tab_text.split(" - ")
            if len(splitted_active_tab_text) > 1:
                # Remove application name from tab text
                active_tab_text = " - ".join(splitted_active_tab_text[:-1])
            self.data_process(switched_time, active_name, active_tab_text)
        except:
            # If this thread stopped by rebooting from sleep, maybe...
            import traceback
            print("Thread loop exited by any problem!!!!")
            global_v.is_threadloop_error = True
            global_v.is_sleeping = True
            traceback.print_exc()

    def send_json(self, t, active_name, tab_text):
        pass

    def enqueue_data(self, t, active_name, tab_text):
        global_v.tab_id += 1
        global_v.tab_queue.append({
            "uuid": self.uuid,
            "type": "t",
            "id": global_v.tab_id,
            "activeName": active_name,
            "tabText": tab_text,
            "startTime": t
        })



'''
# If neccesary to implement observer for each OS, implement below.
class MouseObserver:
    pass
class KeyboardObserver:
    pass
'''