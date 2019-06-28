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

class Observer:
    os = ""
    uuid = ""
    def __init__(self, os, uuid=""):
        # ActiveTab，Mouse，Keybord(，PID)で並列処理するので，最大4？
        self.os = os
        if uuid:
            self.uuid = uuid
        pass

    def close(self): pass

class ActiveTabObserver:
    def __init__(self):
        pass

class MouseObserver:
    def __init__(self):
        pass

class KeybordObserver:
    def __init__(self):
        pass

# class PidObserver:
#     def __init__(self):
#         pass