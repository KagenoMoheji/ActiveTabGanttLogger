import platform
from datetime import datetime
import time
import psutil
import math
# import pyautogui
# from pynput.mouse import Controller as mctrl
from pynput import keyboard
import threading


'''
References:
    https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    https://github.com/moses-palmer/pynput/issues/20#issuecomment-290649632
    https://qiita.com/castaneai/items/9cc33817419896667f34
    https://stackoverflow.com/a/54627646
    https://stackoverflow.com/questions/53144360/how-to-run-an-infinite-while-loop-and-keyboard-listener-from-pynput-library-at-t
    https://qiita.com/tag1216/items/db5adcf1ddcb67cfefc8
    http://nobunaga.hatenablog.jp/entry/2016/06/03/204450
    https://www.lisz-works.com/entry/python-arg-function
'''
sum_keyboard_cnt = 0
# CTRLKEY = [keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]
# prev_key = ''

class MyThread(threading.Thread):
    callback = None
    def __init__(self, target):
        super(MyThread, self).__init__()
        self.callback = target
        self.stop_event = threading.Event()
        self.setDaemon(True)
    def stop(self):
        self.stop_event.set()
    def start(self):
        self.callback()

def on_release(key):
    global sum_keyboard_cnt # , prev_key, CTRLKEY
    sum_keyboard_cnt += 1
    # if (prev_key in CTRLKEY and key == keyboard.KeyCode(char = 'c')) \
    #     or (prev_key == keyboard.KeyCode(char = 'c') and key in CTRLKEY): # コピペとかで使うので却下
    #     print("Listener exit")
    #     return False # listener.stop()
    # prev_key = key
    return True
def mainloop():
    global sum_keyboard_cnt # ここではglobalだが，class内ではクラス変数として使えそう
    recent_time = time.time()
    while True:
        current_time = time.time()

        if current_time - recent_time > 1.0: # 1秒程度経ったら
            recent_time = current_time
            print(sum_keyboard_cnt)
            sum_keyboard_cnt = 0

if __name__ == "__main__":
    os = platform.platform(terse=True)
    if "Windows" in os:
        try:
            listener = keyboard.Listener(on_release=on_release) # on_press=on_press, 
            th1 = MyThread(target=listener.start)
            th2 = MyThread(target=mainloop)
            th1.start()
            th2.start()
        except KeyboardInterrupt:
            print("Exit")
            exit()
        finally:
            print("Finally")
            th1.stop()
            th2.stop()
    elif "Darwin" in os:
        try:
            listener = keyboard.Listener(on_release=on_release) # on_press=on_press, 
            th1 = MyThread(target=listener.start)
            th2 = MyThread(target=mainloop)
            th1.start()
            th2.start()
        except KeyboardInterrupt:
            print("Exit")
            exit()
        finally:
            print("Finally")
            th1.stop()
            th2.stop()
