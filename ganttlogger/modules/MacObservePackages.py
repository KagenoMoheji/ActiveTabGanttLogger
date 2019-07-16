from datetime import datetime
import time
import psutil
from AppKit import NSWorkspace as nsw
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)
import ganttlogger.modules.Global as global_v

class ActiveTabObserver:
    uuid = ""
    data_process = None
    def __init__(self, uuid, is_alone):
        '''
        Monitor active-tab on Mac.
        '''
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
                    fw = nsw.sharedWorkspace().activeApplication()
                    # active_pid = fw["NSApplicationProcessIdentifier"]
                    active_name = fw["NSApplicationName"]
                    active_tab_text = ""
                    cg_windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
                    for cg_window in cg_windows:
                        if active_name == cg_window["kCGWindowOwnerName"] and cg_window["kCGWindowName"]:
                            active_tab_text = cg_window["kCGWindowName"]
                            break
                    if recent_active_tab_text != active_tab_text.upper():
                        switched_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
                        recent_active_tab_text = active_tab_text.upper()
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