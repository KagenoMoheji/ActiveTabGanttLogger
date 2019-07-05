'''
●送信時はenv.jsonを読み込んで環境変数として使う
●Aloneのときはjsonを使わずRawDataの後ろに格納するだけ

もっと簡潔に書けるよな！？？！？！？？！？！？！OS判別でimportするやつ変えるだけだし！！
'''

'''
References:
    https://heavywatal.github.io/python/concurrent.html
    https://torina.top/detail/270/
    https://qiita.com/castaneai/items/9cc33817419896667f34
    https://qiita.com/pumbaacave/items/942f86269b2c56313c15
    https://qiita.com/tag1216/items/db5adcf1ddcb67cfefc8
    https://minus9d.hatenablog.com/entry/2017/10/26/231241
'''
import time
from datetime import datetime
# import numpy as np
import concurrent.futures as confu
from collections import deque
import modules.Global as global_v
from modules.Public import StrFormatter, MyThread
from modules.CommonObservePackages import MouseObserver, KeyboardObserver

class Observer:
    observer = None
    strfmr = None
    def __init__(self, os, uuid):
        self.strfmr = StrFormatter()
        if os == "w":
            self.observer = WinObserver(uuid)
        elif os == "d":
            self.observer = MacObserver(uuid)
        else:
            print(self.strfmr.get_colored_console_log("red",
                "Error: This can work on 'Windows' or 'MacOS'"))

    def start(self):
        print(self.strfmr.get_colored_console_log("yellow",
            "Start after finising setting logger.\nReady to start?(Y/n) : "), end="")
        st_input = input().strip()
        if st_input == "n":
            print("GanttLogger closed")
            exit()
        if st_input != "Y":
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid input. Input 'Y'(=yes) or 'n'(=no)."))
            exit()
        self.observer.run() # self.run()

    def run(self):
        self.observer.run()



class WinObserver:
    uuid = ""
    strfmr = None
    ob_activetab = None
    ob_mouse = None
    ob_keyboard = None
    th_activetab = None
    th_mouse = None
    th_keyboard = None
    def __init__(self, uuid):
        from modules.WinObservePackages import ActiveTabObserver
        self.strfmr = StrFormatter()
        self.ob_activetab = ActiveTabObserver()
        self.ob_mouse = MouseObserver()
        self.ob_keyboard = KeyboardObserver()
        self.uuid = uuid
        # ★："threading" can't work multi-threading well,
        # but exit by "Ctrl+C" can work below.
        # self.th_activetab = MyThread(target=self.ob_activetab.run)
        # self.th_mouse = MyThread(target=self.ob_mouse.run)
        # self.th_keyboard = MyThread(target=self.ob_keyboard.run)
        # ▲："concurrent.future" can work multi-threading well,
        # but we need to devise a way to exit("Ctrl+C" can't work).
        self.executor = confu.ThreadPoolExecutor(max_workers=3)

    def run(self):
        # ★
        # self.th_activetab.start()
        # self.th_mouse.start()
        # self.th_keyboard.start()
        while True:
            # ▲
            self.executor.submit(self.ob_activetab.run)
            self.executor.submit(self.ob_mouse.run)
            self.executor.submit(self.ob_keyboard.run)
            while not global_v.is_switched_to_exit:
                time.sleep(1)
            is_confirmed_exiting = self.confirm_exiting()
            if is_confirmed_exiting:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer exited."))
                break
            else:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer restarted."))
                global_v.is_switched_to_exit = False
        self.executor.shutdown()

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
    

class MacObserver:
    uuid = ""
    strfmr = None
    ob_activetab = None
    ob_mouse = None
    ob_keyboard = None
    th_activetab = None
    th_mouse = None
    th_keyboard = None
    def __init__(self, uuid):
        from modules.MacObservePackages import ActiveTabObserver
        self.strfmr = StrFormatter()
        self.ob_activetab = ActiveTabObserver()
        self.ob_mouse = MouseObserver()
        self.ob_keyboard = KeyboardObserver()
        self.uuid = uuid
        # ★："threading" can't work multi-threading well,
        # but exit by "Ctrl+C" can work below.
        # self.th_activetab = MyThread(target=self.ob_activetab.run)
        # self.th_mouse = MyThread(target=self.ob_mouse.run)
        # self.th_keyboard = MyThread(target=self.ob_keyboard.run)
        # ▲："concurrent.future" can work multi-threading well,
        # but we need to devise a way to exit("Ctrl+C" can't work).
        self.executor = confu.ThreadPoolExecutor(max_workers=3)

    def run(self):
        # ★
        # self.th_activetab.start()
        # self.th_mouse.start()
        # self.th_keyboard.start()
        # ▲
        while True:
            # ▲
            self.executor.submit(self.ob_activetab.run)
            self.executor.submit(self.ob_mouse.run)
            self.executor.submit(self.ob_keyboard.run)
            while not global_v.is_switched_to_exit:
                time.sleep(1)
            is_confirmed_exiting = self.confirm_exiting()
            if is_confirmed_exiting:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer exited."))
                break
            else:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Observer restarted."))
                global_v.is_switched_to_exit = False
        self.executor.shutdown()

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

