'''
●送信時はenv.jsonを読み込んで環境変数として使う
●Aloneのときはjsonを使わずRawDataの後ろに格納するだけ
'''

'''
References:
    https://heavywatal.github.io/python/concurrent.html
    https://torina.top/detail/270/
    https://qiita.com/castaneai/items/9cc33817419896667f34
    https://qiita.com/pumbaacave/items/942f86269b2c56313c15
    https://qiita.com/tag1216/items/db5adcf1ddcb67cfefc8
    https://minus9d.hatenablog.com/entry/2017/10/26/231241

マルチスレッドよりマルチプロセスの方が良い…？
ただしマルチプロセス化する関数間での変数の受け渡しが無い方が良さそう
まずはマルチスレッドで．
'''
from datetime import datetime
# import numpy as np
from collections import deque
from modules.Public import StrFormatter, MyThread
from modules.CommonObservePackages import MouseObserver, KeyboardObserver
from modules.Logger import RawDataStore

class Observer:
    observer = None
    strfmr = None
    def __init__(self, os, uuid):
        self.strfmr = StrFormatter()
        if os == "w":
            self.observer = WindowsObserver(uuid)
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
        elif st_input != "Y":
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid input. Input 'Y'(=yes) or 'n'(=no)."))
            exit()
        self.run()

    def run(self):
        self.observer.run()

    def close(self):
        self.observer.close()


class WindowsObserver:
    uuid = "" # If mode 'Alone', unused.
    store = None
    ob_activetab = None
    ob_mouse = None
    ob_keyboard = None
    def __init__(self, uuid):
        from modules.WinObservePackages import ActiveTabObserver
        self.uuid = uuid
        self.store = RawDataStore()
        self.ob_activetab = ActiveTabObserver()
        self.ob_mouse = MouseObserver()
        self.ob_keyboard = KeyboardObserver()

    def run(self):
        # このあたりでスレッド展開
        print("Hello, WindowsObserver!")

    def close(self):
        # self.ob_activetab.close()
        # self.ob_mouse.close()
        # self.ob_keyboard.close()
        pass

    '''
    rawdataへの格納はどうやる？
    データ送信はどうやる？
    '''
    

class MacObserver:
    uuid = "" # If mode 'Alone', unused.
    store = None
    ob_activetab = None
    ob_mouse = None
    ob_keyboard = None
    def __init__(self, uuid):
        from modules.MacObservePackages import ActiveTabObserver
        self.uuid = uuid
        self.store = RawDataStore()
        self.ob_activetab = ActiveTabObserver()
        self.ob_mouse = MouseObserver()
        self.ob_keyboard = KeyboardObserver()

    def run(self):
        # このあたりでスレッド展開
        print("Hello, MacObserver!")

    def close(self):
        # self.ob_activetab.close()
        # self.ob_mouse.close()
        # self.ob_keyboard.close()
        pass

