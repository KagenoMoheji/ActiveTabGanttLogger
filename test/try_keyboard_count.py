import platform
import time
# import pyautogui
# from pynput.mouse import Controller as mctrl
from pynput import keyboard
import threading


'''
●Macの場合，キーボード監視に権限がかかっているみたいなので事前の準備が必要．
・https://stackoverflow.com/a/54659886
・つまり，"システム環境設定＞セキュリティとプライバシー＞プライバシー＞アクセシビリティ"を選択して，
「+」をクリックしてPythonや実行ファイルを実行するのに必要なアプリケーションを追加していく．
例えば"アプリケーション＞VScode.app"や"アプリケーション＞ユーティリティ＞ターミナル.app"など．
・更に実行時に"$ sudo python3 ~.py"というようにrootで実行するようにしないといけない．

●もう1つの懸念点は，マウスとキーボードの同時監視によるMacからの拒絶．まだわからんが…
・https://github.com/moses-palmer/pynput/issues/55

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





# if __name__ == "__main__":
#     import platform
#     import time
#     from pynput import keyboard

#     os = platform.platform(terse=True)
#     if "Windows" in os:
#         '''
#         [キーボードの1sごとの打鍵数をカウントする]
#         ●pynputで実装
#         ・https://stackoverflow.com/a/45592445
#         ・https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
#         ・上の2つ目のリンクはThread使用だったので適していないと思ったけど，1つ目のリンクで行けた
#         ・ただしメインループとの互換が悪そう，工夫が必要．最有力候補ではある
#         ●msvcrt.kbhit()で実装
#         ・https://stackoverflow.com/a/303976
#         ・無限ループに入ってしまう，脱出方法がわからん
#         ●termios(とtty)を使って実装
#         ・http://www.jonwitts.co.uk/archives/896
#         ・https://qiita.com/tortuepin/items/e6c72f48115f20744ace
#         ・termiosがUnix向けなので無理そう
#         '''
#         try:
#             recent_time = time.time()
#             sum_keyboard_cnt = 0
#             on_press = lambda key: False
#             on_release = lambda key: False 
#             while True:
#                 current_time = time.time()

#                 # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: # global使う場合
#                 #     listener.join()

#                 with keyboard.Listener(on_press=on_press) as listener: # lmbda使って挟む場合
#                     listener.join()
#                 sum_keyboard_cnt += 1
#                 with keyboard.Listener(on_release=on_release) as listener:
#                     listener.join()

#                 if current_time - recent_time > 1.0: # 1秒程度経ったら
#                     recent_time = current_time
#                     print(sum_keyboard_cnt)
#                     sum_keyboard_cnt = 0
                
#         except KeyboardInterrupt:
#             print("Exit")
#     elif "Darwin" in os:
#         try:
#             recent_time = time.time()
#             sum_keyboard_cnt = 0
#             on_press = lambda key: False
#             on_release = lambda key: False 
#             while True:
#                 current_time = time.time()

#                 # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: # global使う場合
#                 #     listener.join()

#                 with keyboard.Listener(on_press=on_press) as listener: # lmbda使って挟む場合
#                     listener.join()
#                 sum_keyboard_cnt += 1
#                 with keyboard.Listener(on_release=on_release) as listener:
#                     listener.join()

#                 if current_time - recent_time > 1.0: # 1秒程度経ったら
#                     recent_time = current_time
#                     print(sum_keyboard_cnt)
#                     sum_keyboard_cnt = 0
                
#         except KeyboardInterrupt:
#             print("Exit")
