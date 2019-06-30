from pynput import keyboard
import threading, time

sum_keyboard_cnt = 0

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
    return True

def mainloop():
    global sum_keyboard_cnt
    recent_time = time.time()
    while True:
        current_time = time.time()

        if current_time - recent_time > 1.0: # 1秒程度経ったら
            recent_time = current_time
            print(sum_keyboard_cnt)
            sum_keyboard_cnt = 0

if __name__ == "__main__":
    try:
        listener = keyboard.Listener(on_release=on_release)
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