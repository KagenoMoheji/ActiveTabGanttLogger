'''
Because we can run MouseObserver with same code regardless on Windows or Mac,
we implemented only this class.
But we can implement in per class when we have to implement following OS.
'''
import math
import time
from datetime import datetime
from collections import deque
# import pyautogui
from pynput import mouse, keyboard
from modules.Public import MyThread, StrFormatter
import modules.Global as global_v

class MouseObserver:
    sec_sum_mouse_dist = 0
    mouse_ctrl = None
    def __init__(self):
        self.sec_sum_mouse_dist = 0
        self.mouse_ctrl = mouse.Controller()

    def run(self):
        # try:
        dif_x, dif_y = 0, 0
        recent_time = time.time()
        recent_x, recent_y = self.mouse_ctrl.position # pyautogui.position()
        while not global_v.is_switched_to_exit:
            current_time = time.time()
            x, y = self.mouse_ctrl.position # pyautogui.position()
            if (x != recent_x) or (y != recent_y):
                dif_x = x - recent_x
                dif_y = y - recent_y
                self.sec_sum_mouse_dist += math.sqrt(dif_x * dif_x + dif_y * dif_y)
                recent_x, recent_y = x, y
            if current_time - recent_time > 1.0:
                # このあたりでsum_key_boardで操作する
                # ログするとか？
                print("Mouse[{datetime}]: {dist}".format(datetime=datetime.now().strftime("%H:%M:%S.%f"), dist=self.sec_sum_mouse_dist))
                recent_time = current_time
                self.sec_sum_mouse_dist = 0
            time.sleep(0.001)
        # except KeyboardInterrupt:
        #     print("MouseObserver.py: KeyboardInterrupt")
    
    def hand_data(self):
        # キューに格納するか，送信するかはここで
        pass


class KeyboardObserver:
    '''
    References:
        https://python.ms/sub/misc/list-comparison/
    '''
    sec_sum_keyboard_cnt = 0
    strfmr = None
    current_4key = deque([], maxlen=4)
    EXITCOMB_WIN = set([
        keyboard.Key.ctrl_l,
        keyboard.Key.shift_l,
        keyboard.Key.ctrl_r,
        keyboard.Key.shift_r
        # keyboard.KeyCode(char = ''),
        # keyboard.KeyCode(char = 'q')
    ])
    EXITCOMB_MAC = set([
        keyboard.Key.cmd_l,
        keyboard.Key.shift_l,
        keyboard.Key.cmd_r,
        keyboard.Key.shift_r
    ])
    def __init__(self):
        self.sec_sum_keyboard_cnt = 0
        self.strfmr = StrFormatter()

    def on_release(self, key):
        if len(self.current_4key) == 4:
            self.current_4key.popleft()
            self.current_4key.append(key)
        else:
            self.current_4key.append(key)
        if self.EXITCOMB == set(self.current_4key):
            # Here, switch a flag to exit children threads
            global_v.is_switched_to_exit = True
            # Delete all text in terminal(Flush stdin buffer?)
            # ??????????????????????????????????????????
            return False
        self.sec_sum_keyboard_cnt += 1
        time.sleep(0.001) # Max type speed is 256 wpm -> 0.002 is OK?
        return True
    
    def get_key_seconds(self):
        while not global_v.is_switched_to_exit:
            # このあたりでsum_key_boardで操作する
            # ログするとか？
            print("Keyboard[{datetime}]: {cnt}".format(datetime=datetime.now().strftime("%H:%M:%S.%f"), cnt=self.sec_sum_keyboard_cnt))
            self.sec_sum_keyboard_cnt = 0
            time.sleep(1)
    
    def run(self):
        try:
            listener = keyboard.Listener(on_release=self.on_release)
            th_on_release = MyThread(target=listener.start)
            th_mainloop = MyThread(target=self.get_key_seconds)
            th_on_release.start()
            th_mainloop.start()
        # except KeyboardInterrupt:
        #     print("KeyboardObserver.py: KeyboardInterrupt")
        finally:
            th_on_release.stop()
            th_mainloop.stop()

    def hand_data(self):
        # キューに格納するか，送信するかはここで
        pass