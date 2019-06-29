'''
●json形式にして渡したり送信したり
{
    uuid: UUID
    activeTab: {
        id: アクティブタブログでの一意の連続数値,
    },
    mouse: {
        id: マウスログでの一意の連続数値,
    },
    keybord: {
        id: キーボードログでの一意の連続数値,
    }
}
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
import numpy as np
import psutil
import math
import pyautogui
from modules.StrFormatter import StrFormatter

class Observer:
    observer = None
    strfmr = None
    def __init__(self, os, uuid=""):
        if os == "w":
            self.observer = WindowsObserver(uuid)
        elif os == "d":
            self.observer = MacObserver(uuid)
        self.strfmr = StrFormatter()

    def start(self):
        print("Ready to start?(Y/n) : ", end="")
        st_input = input().strip()
        if st_input == "n":
            print("GanttLogger closed")
            exit()
        elif st_input != "Y":
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid input. Input 'Y'(=yes) or 'n'(=no)."))
            exit()
        
        # このあたりでスレッド展開
        print("Hello, Observer!")
        # self.observer.run()

class RawDataStore():
    raw_tab_data = np.array()
    raw_mouse_data = np.array()
    raw_keyboard_data = np.array()

class WindowsObserver:
    uuid = ""
    store = None
    def __init__(self, uuid=""):
        import win32gui as wg
        import win32process as wp
        import win32com.client as wcli
        
        if uuid:
            self.uuid = uuid
        self.store = RawDataStore()
    

class MacObserver:
    uuid = ""
    store = None
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
