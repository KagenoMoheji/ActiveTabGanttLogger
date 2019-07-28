import os
import sys
import platform
import datetime
from ganttlogger.modules.Public import StrFormatter

class Merger:
    currdir = ""
    mergedir = ""
    run_merge = {
        "active_tab": False,
        "mouse": False,
        "keyboard": False
    }
    strfmr = None
    def __init__(self):
        '''
        Merge logs in folders in "ganttlogger_logs".
        '''
        self.strfmr = StrFormatter()
        # Check whether current folder name is "ganttlogger_logs"
        self.currdir = os.getcwd()
        is_win = "Windows" in platform.platform(terse=True)
        curr_name = ""
        if  is_win:
            curr_name = self.currdir.split("\\")[-1]
        else:
            curr_name = self.currdir.split("/")[-1]
        if curr_name != "ganttlogger_logs":
            print(self.strfmr.get_colored_console_log("red",
                "Error: You must move to a folder 'ganttlogger_logs'."))
            sys.exit()
        self.mergedir = "{currdir}/merged_{datetime}".format(currdir=self.currdir, datetime=datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    
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
            os.makedirs(os.path.dirname("{}/".format(self.mergedir)), exist_ok=True)
            print("Created an output folder '{}'.".format(self.mergedir))
            self.run()
        except KeyboardInterrupt:
            print("Exit")
            sys.exit()
    
    def run(self):
        # Get dictionary of directorys in a folder "ganttlogger_logs" except for directorys including "merged" in its name.
        log_folders = {f: None for f in os.listdir(self.currdir) if (os.path.isdir(os.path.join(self.currdir, f))) and (not "merged" in f)}
        # 
        remove_keys_list = []
        for key in log_folders.keys():
            readme = "{dir}/{folder}/README.txt".format(dir=self.currdir, folder=key)
            if not os.path.exists(readme):
                remove_keys_list.append(key)
                continue
            # Read from text file until appearing 'StartDate' till 4 rows.
            has_startdate = False
            row_startdate = ""
            with open(readme, "r", encoding="utf-8") as f:
                for row in range(4):
                    row_startdate = f.readline()
                    if "StartDate" in row_startdate:
                        has_startdate = True
                        break
            if not has_startdate: # If README.txt doesn't have a row "StartDate".
                print(self.strfmr.get_colored_console_log("yellow",
                    "Warning: File '{readme}' doesn't have a row 'StartDate'.".format(readme=readme)))
                remove_keys_list.append(key)
                continue
            # Add value of "StartDate" to list
            try:
                log_folders[key] = datetime.datetime.strptime((row_startdate.split(": ")[-1]).strip(), "%Y/%m/%d %H:%M:%S.%f")
            except ValueError:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: Invalid format of a value of 'StartDate' in {readme}.".format(readme=readme)))
                sys.exit()
        # Remove values in specific keys in "log_folders"
        for k in remove_keys_list:
            log_folders.pop(k)
        # Sort "log_folders" by datetime of values in ASC
        log_folders = dict(sorted(log_folders.items(), key=lambda x:x[1]))
#         print("""
# log_folders: {log_folders}
# """.format(log_folders=log_folders))

        if self.run_merge["active_tab"]:
            self.merge_active_tab_logs(log_folders)
        if self.run_merge["mouse"]:
            self.merge_mouse_logs(log_folders)
        if self.run_merge["keyboard"]:
            self.merge_keyboard_logs(log_folders)

    def merge_active_tab_logs(self, sorted_folders_dict):
        with open("{mergedir}/active_tab.log".format(mergedir=self.mergedir), "a", encoding="utf-8") as af:
            af.write("StartTime]:+:[ApplicationName]:+:[TabText\n")
            for folder in sorted_folders_dict:
                try:
                    filedir = "{currdir}/{folder}/active_tab.log".format(currdir=self.currdir, folder=folder)
                    with open(filedir, "r", encoding="utf-8") as rf:
                        log = rf.read().strip() # Remove the last "\n"
                        splitted_log = log.split("\n", 1)
                        if "StartTime]:+:[" in splitted_log[0]:
                            log = splitted_log[1]
                    log += "\n"
                    af.write(log)
                except FileNotFoundError:
                    print(self.strfmr.get_colored_console_log("red",
                        "Error: File '{filedir}' not found.".format(filedir=filedir)))
                    sys.exit()
        print("ActiveTab merged!")

    def merge_mouse_logs(self, sorted_folders_dict):
        with open("{mergedir}/mouse.log".format(mergedir=self.mergedir), "a", encoding="utf-8") as af:
            af.write("Time]:+:[MoveDistance\n")
            for folder in sorted_folders_dict:
                try:
                    filedir = "{currdir}/{folder}/mouse.log".format(currdir=self.currdir, folder=folder)
                    with open(filedir, "r", encoding="utf-8") as rf:
                        log = rf.read().strip() # Remove the last "\n"
                        splitted_log = log.split("\n", 1)
                        if "Time]:+:[" in splitted_log[0]:
                            log = splitted_log[1]
                    log += "\n"
                    af.write(log)
                except FileNotFoundError:
                    print(self.strfmr.get_colored_console_log("red",
                        "Error: File '{filedir}' not found.".format(filedir=filedir)))
                    sys.exit()
        print("Mouse merged!")

    def merge_keyboard_logs(self, sorted_folders_dict):
        with open("{mergedir}/keyboard.log".format(mergedir=self.mergedir), "a", encoding="utf-8") as af:
            af.write("Time]:+:[PressCount\n")
            for folder in sorted_folders_dict:
                try:
                    filedir = "{currdir}/{folder}/keyboard.log".format(currdir=self.currdir, folder=folder)
                    with open(filedir, "r", encoding="utf-8") as rf:
                        log = rf.read().strip() # Remove the last "\n"
                        splitted_log = log.split("\n", 1)
                        if "Time]:+:[" in splitted_log[0]:
                            log = splitted_log[1]
                    log += "\n"
                    af.write(log)
                except FileNotFoundError:
                    print(self.strfmr.get_colored_console_log("red",
                        "Error: File '{filedir}' not found.".format(filedir=filedir)))
                    sys.exit()
        print("Keyboard merged!")
