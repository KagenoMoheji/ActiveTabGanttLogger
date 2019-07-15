import sys
import time
from datetime import datetime
# import numpy as np
import concurrent.futures as confu
from collections import deque
import modules.Global as global_v
from modules.Public import StrFormatter
from modules.CommonObservePackages import MouseObserver, KeyboardObserver

'''
References:
    https://blog.codecamp.jp/python-class-2
    https://www.lifewithpython.com/2014/01/python-super-function.html
'''

class Observer:
    strfmr = None
    ob_activetab = None
    ob_mouse = None
    ob_keyboard = None
    executor = None
    def __init__(self, uuid, is_alone):
        self.ob_mouse = MouseObserver(uuid, is_alone)
        self.ob_keyboard = KeyboardObserver(uuid, is_alone)
        self.strfmr = StrFormatter()
        self.executor = confu.ThreadPoolExecutor(max_workers=3)

    def start(self):
        print(self.strfmr.get_colored_console_log("yellow",
            "Start after finising setting logger.\nReady to start?(Y/n) : "), end="")
        st_input = input().strip()
        if st_input == "n":
            print("GanttLogger closed")
            sys.exit()
        if st_input != "Y":
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid input. Input 'Y'(=yes) or 'n'(=no)."))
            sys.exit()
        self.run()

    def run(self):
        while True:
            self.executor.submit(self.ob_activetab.run)
            self.executor.submit(self.ob_mouse.run)
            self.executor.submit(self.ob_keyboard.run)
            while not global_v.is_sleeping:
                time.sleep(1)
            if global_v.is_threadloop_error: # When "Thread loop exited by any problem!!!!" occured
                self.executor.shutdown()
                sys.exit()
            is_confirmed_exiting = self.confirm_exiting()
            if is_confirmed_exiting:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer exited."))
                break
            else:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer restarted."))
                global_v.is_sleeping = False
        self.executor.shutdown()
        global_v.cli_exit = True

    def confirm_exiting(self):
        while True:
            print(self.strfmr.get_colored_console_log("yellow",
                "Logging is sleeping. Will you exit?(Y/n) : "), end="")
            str_input = input().strip()
            if str_input == "Y":
                return True
            elif str_input == "n":
                return False
            else:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: Invalid input. Input 'Y'(=yes) or 'n'(=no)."))
    

class WinObserver(Observer):
    def __init__(self, uuid, is_alone):
        super().__init__(uuid, is_alone)
        from modules.WinObservePackages import ActiveTabObserver
        self.ob_activetab = ActiveTabObserver(uuid, is_alone)


class MacObserver(Observer):
    def __init__(self, uuid, is_alone):
        super().__init__(uuid, is_alone)
        from modules.MacObservePackages import ActiveTabObserver
        self.ob_activetab = ActiveTabObserver(uuid, is_alone)
