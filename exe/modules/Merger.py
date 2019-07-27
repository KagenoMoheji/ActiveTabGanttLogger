import os
import sys
import platform
import datetime
from modules.Public import StrFormatter

class Merger:
    mergedir = ""
    run_merge = {
        "active_tab": False,
        "mouse": False,
        "keyboard": False
    }
    strfmr = None
    def __init__(self):
        self.strfmr = StrFormatter()
        # Check whether current folder name is "ganttlogger_logs"
        currdir = os.getcwd()
        is_win = "Windows" in platform.platform(terse=True)
        curr_name = ""
        if  is_win:
            curr_name = currdir.split("\\")[-1]
        else:
            curr_name = currdir.split("/")[-1]
        if curr_name != "ganttlogger_logs":
            print(self.strfmr.get_colored_console_log("red",
                "Error: You must move to a folder 'ganttlogger_logs'."))
            sys.exit()
        self.mergedir = "{currdir}/merged_{datetime}/".format(currdir=currdir, datetime=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    def start(self):
        try:
            select_log_names = set(["active_tab", "mouse", "keyboard"])
            while True:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Select 'all' or names separated by ',' from ('active_tab'|'mouse'|'keyboard').: "), end="")
                input_select = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                if not input_select[0]:
                    print(self.strfmr.get_colored_console_log("red",
                        "Error: Invalid input."))
                    continue
                elif "all" in input_select: 
                    if len(input_select) == 1:
                        self.run_merge["active_tab"] = True
                        self.run_merge["mouse"] = True
                        self.run_merge["keyboard"] = True
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Too many select despite 'all'."))
                        continue
                else:
                    xor_select = set(input_select) ^ select_log_names
                    if len(xor_select) == 0 or \
                        all(x in select_log_names for x in xor_select):
                        if "active_tab" in input_select:
                            self.run_merge["active_tab"] = True
                        if "mouse" in input_select:
                            self.run_merge["mouse"] = True
                        if "keyboard" in input_select:
                            self.run_merge["keyboard"] = True
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: There are some invalid names."))
                        continue

            # Create new folder where is outputted merged logs
            os.makedirs(os.path.dirname(self.mergedir), exist_ok=True)
            self.run()
        except KeyboardInterrupt:
            print("Exit")
            sys.exit()
    
    def run(self):
        # ここでganttlogger_logs内のID名のフォルダをREADMEの開始日時を元にソートしてファイル名リストに格納

        if self.run_merge["active_tab"]:
            self.merge_active_tab_logs()
        if self.run_merge["mouse"]:
            self.merge_mouse_logs()
        if self.run_merge["keyboard"]:
            self.merge_keyboard_logs()

    def merge_active_tab_logs(self, folders_list):
        print("ActiveTab merged!")
    def merge_mouse_logs(self, folders_list):
        print("Mouse merged!")
    def merge_keyboard_logs(self, folders_list):
        print("Keyboard merged!")