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
# import threading
import concurrent.futures as confu
import platform
from datetime import datetime
import time
# import numpy as np
from collections import deque
import psutil
import math
import pyautogui
from modules.StrFormatter import StrFormatter
from modules.Logger import RawDataStore

class Observer:
    observer = None
    strfmr = None
    def __init__(self, os, uuid=""):
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
        
        self.observer.run()


class WindowsObserver:
    uuid = ""
    store = None
    common = None
    def __init__(self, uuid=""):
        import win32gui as wg
        import win32process as wp
        import win32com.client as wcli
        
        if uuid:
            self.uuid = uuid
        self.store = RawDataStore()
        self.common = CommonObserver()

    def run(self):
        # このあたりでスレッド展開
        print("Hello, WindowsObserver!")

    def active_tab_observer(self):
        pass

    '''
    Because we can run functions below with same code,we implemented them in class 'CommonObserver'.
    But we can implement here when we have to implement following OS.
    '''
    # def mouse_distance_measurer(self):
    # def keyboard_counter(self):
    

class MacObserver:
    uuid = ""
    store = None
    common = None
    def __init__(self, uuid=""):
        from AppKit import NSWorkspace as nsw
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID
        )

        if uuid:
            self.uuid = uuid
        self.store = RawDataStore()
        self.common = CommonObserver()

    def run(self):
        # このあたりでスレッド展開
        print("Hello, MacObserver!")

    def active_tab_observer(self):
        pass

    '''
    Because we can run functions below with same code,we implemented them in class 'CommonObserver'.
    But we can implement here when we have to implement following OS.
    '''
    # def mouse_distance_measurer(self):
    # def keyboard_counter(self):


class CommonObserver:
    '''
    Functions who can run regardress OS.
    '''
    def mouse_distance_measurer(self):
        pass
    def keyboard_counter(self):
        pass
