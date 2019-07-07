'''
●jsonを引数に受け取る
●jsonのid順にログ追記
●受信の場合はenv.jsonを読み込んで環境変数にする
'''
import os
import time
from datetime import datetime
# import concurrent.futures as confu
import modules.Global as global_v
from modules.Public import StrFormatter

class Logger:
    uuid = ""
    strfmr = None
    dirname = ""
    def __init__(self, uuid):
        '''
        
        References:
            https://stackoverflow.com/a/12517490
            https://kokufu.blogspot.com/2018/04/python-with.html
        '''
        self.uuid = uuid
        self.strfmr = StrFormatter()
        # Create output dirs
        self.dirname = "ganttlogger_logs/{}".format(uuid)
        readme = "{}/README.txt".format(self.dirname)
        os.makedirs(os.path.dirname(readme), exist_ok=True)
        with open(readme, "w", encoding="utf-8") as f:
            startdate = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
            text = """\
UUID       : {uuid}
StartDate  : {startdate}
Supervisor : 
Target User: 
""".format(uuid=uuid, startdate=startdate)
            f.write(text)

    def run_logger(self):
        # receive_json()とoutput()のスレッド展開
        print("Hello, Logger!")

    def receive_json(self):
        # jsonデータを受信してキューに格納する
        pass

    def output(self):
        with open("{}/active_tab.csv".format(self.dirname), "a", encoding="utf-8") as ft,\
            open("{}/mouse.csv".format(self.dirname), "a", encoding="utf-8") as fm,\
            open("{}/keyboard.csv".format(self.dirname), "a", encoding="utf-8") as fk:
            # Write attributes
            ft.write("StartTime,ApplicationName,TabText\n")
            fm.write("Time,MoveDistance\n")
            fk.write("Time,PressCount\n")
            # Add logs
            is_all_empty = True
            while True:
                print("Hello!!!!!!")
                len_tab_queue = len(global_v.tab_queue)
                len_mouse_queue = len(global_v.mouse_queue)
                len_keyboard_queue = len(global_v.keyboard_queue)
                if len_tab_queue > 0:
                    is_all_empty = False
                    for _ in range(len_tab_queue):
                        data = global_v.tab_queue.popleft()
                        log = "{startTime},{activeName},{tabText}\n".format(
                            startTime=data["startTime"],
                            activeName=data["activeName"],
                            tabText=data["tabText"]
                        )
                        ft.write(log)
                if len_mouse_queue > 0:
                    is_all_empty = False
                    for _ in range(len_mouse_queue):
                        data = global_v.mouse_queue.popleft()
                        log = "{time},{dis}\n".format(
                            time=data["time"],
                            dis=data["distance"]
                        )
                        fm.write(log)
                if len_keyboard_queue > 0:
                    is_all_empty = False
                    for _ in range(len_keyboard_queue):
                        data = global_v.keyboard_queue.popleft()
                        log = "{time},{cnt}\n".format(
                            time=data["time"],
                            cnt=data["count"]
                        )
                        fk.write(log)
                if is_all_empty and global_v.is_switched_to_exit:
                    # This is a signal that all logging finished and CLI will exit 
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Logging all finished")) # maybe...
                    break
                elif is_all_empty:
                    # This is a signal that logging is finishing
                    print(self.strfmr.get_colored_console_log("yellow",
                        "All queue are empty"))
                is_all_empty = True
                time.sleep(2) # 何秒でも良さそう


