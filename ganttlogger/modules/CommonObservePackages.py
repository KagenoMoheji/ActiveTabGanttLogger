'''
Because we can run MouseObserver and KeyboardObserver with same code
regardless on Windows or Mac, we implemented common classes here.
But we can implement in per classes when we have to implement following OS.
'''
import math
import time
from datetime import datetime
from collections import deque
# import pyautogui
from pynput import mouse, keyboard
from ganttlogger.modules.Public import MyThread, StrFormatter
import ganttlogger.modules.Global as global_v

class MouseObserver:
    uuid = ""
    sec_sum_mouse_dist = 0
    mouse_ctrl = None
    data_process = None
    def __init__(self, uuid, is_alone):
        self.uuid = uuid
        self.sec_sum_mouse_dist = 0
        self.mouse_ctrl = mouse.Controller()
        if is_alone:
            self.data_process = self.enqueue_data
        else:
            self.data_process = self.send_json

    def run(self):
        try:
            dif_x, dif_y = 0, 0
            recent_time = time.time()
            recent_x, recent_y = self.mouse_ctrl.position # pyautogui.position()
            while not global_v.is_sleeping:
                try:
                    current_time = time.time()
                    x, y = self.mouse_ctrl.position # pyautogui.position()
                    if (x != recent_x) or (y != recent_y):
                        dif_x = x - recent_x
                        dif_y = y - recent_y
                        self.sec_sum_mouse_dist += math.sqrt(dif_x * dif_x + dif_y * dif_y)
                        recent_x, recent_y = x, y
                    if current_time - recent_time > 1.0:
                        self.data_process(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), self.sec_sum_mouse_dist)
                        # print("Mouse[{datetime}]: {dist}".format(datetime=datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), dist=self.sec_sum_mouse_dist))
                        recent_time = current_time
                        self.sec_sum_mouse_dist = 0
                    time.sleep(0.001)
                except TypeError:
                    # Avoid to exit thread loop (by rebooting from pc sleep)
                    continue
                except KeyboardInterrupt:
                    continue
        except:
            # If this thread stopped by rebooting from sleep, maybe...
            import traceback
            print("Thread loop exited by any problem!!!!")
            global_v.is_threadloop_error = True
            global_v.is_sleeping = True
            traceback.print_exc()
    
    def send_json(self, t, dis_sec):
        pass

    def enqueue_data(self, t, dis_sec):
        global_v.mouse_id += 1
        global_v.mouse_queue.append({
            "uuid": self.uuid,
            "type": "m",
            "id": global_v.mouse_id,
            "distance": dis_sec,
            "time": t
        })


class KeyboardObserver:
    uuid = ""
    data_process = None
    sec_sum_keyboard_cnt = 0
    current_4key = deque([], maxlen=4)
    EXITCOMB_WIN = set([
        keyboard.KeyCode(char = '1'),
        keyboard.KeyCode(char = '/'),
        keyboard.KeyCode(char = 'z'),
        keyboard.KeyCode(char = '^')
    ])
    EXITCOMB_MAC = set([
        keyboard.KeyCode(char = '1'),
        keyboard.KeyCode(char = '/'),
        keyboard.KeyCode(char = 'z'),
        keyboard.KeyCode(char = '^')
    ])
    def __init__(self, uuid, is_alone):
        self.uuid = uuid
        self.sec_sum_keyboard_cnt = 0
        if is_alone:
            self.data_process = self.enqueue_data
        else:
            self.data_process = self.send_json

    def on_release(self, key):
        if len(self.current_4key) == 4:
            self.current_4key.popleft()
            self.current_4key.append(key)
        else:
            self.current_4key.append(key)
        if (self.EXITCOMB_WIN == set(self.current_4key)) or (self.EXITCOMB_MAC == set(self.current_4key)):
            # Here, switch a flag to exit children threads
            global_v.is_sleeping = True
            '''
            ###############################################################
            Delete all text in terminal(Flush stdin buffer?)
            ??????????????????????????????????????????
            ###############################################################
            '''
            return False
        self.sec_sum_keyboard_cnt += 1
        time.sleep(0.001) # Max type speed is 256 wpm -> 0.002 is OK?
        return True
    
    def get_key_second(self):
        try:
            while not global_v.is_sleeping:
                try:
                    self.data_process(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), self.sec_sum_keyboard_cnt)
                    # print("Keyboard[{datetime}]: {cnt}".format(datetime=datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"), cnt=self.sec_sum_keyboard_cnt))
                    print("""\
============[tab]==============\n
{t}
-----------[mouse]-----------\n
{m}
-----------[keyboard]-----------\n
{k}
""".format(t=global_v.tab_queue, m=global_v.mouse_queue, k=global_v.keyboard_queue))
                    self.sec_sum_keyboard_cnt = 0
                    time.sleep(1)
                except KeyboardInterrupt:
                    continue
        except:
            # If this thread stopped by rebooting from sleep, maybe...
            import traceback
            print("Thread loop exited by any problem!!!!")
            global_v.is_threadloop_error = True
            global_v.is_sleeping = True
            traceback.print_exc()
    
    def run(self):
        try:
            listener = keyboard.Listener(on_release=self.on_release)
            th_on_release = MyThread(target=listener.start)
            th_mainloop = MyThread(target=self.get_key_second)
            th_on_release.start()
            th_mainloop.start()
        # except KeyboardInterrupt:
        #     print("KeyboardObserver.py: KeyboardInterrupt")
        finally:
            th_on_release.stop()
            th_mainloop.stop()

    def send_json(self, t, cnt_sec):
        pass

    def enqueue_data(self, t, cnt_sec):
        global_v.keyboard_id += 1
        global_v.keyboard_queue.append({
            "uuid": self.uuid,
            "type": "k",
            "id": global_v.keyboard_id,
            "count": cnt_sec,
            "time": t
        })