import time
from pynput import keyboard

if __name__ == "__main__":
    try:
        recent_time = time.time()
        sum_keyboard_cnt = 0
        on_press = lambda key: False
        on_release = lambda key: False 
        while True:
            current_time = time.time()

            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
            sum_keyboard_cnt += 1
            with keyboard.Listener(on_release=on_release) as listener:
                listener.join()

            if current_time - recent_time > 1.0: # 1秒程度経ったら
                recent_time = current_time
                print(sum_keyboard_cnt)
                sum_keyboard_cnt = 0
    except KeyboardInterrupt:
        print("Exit")