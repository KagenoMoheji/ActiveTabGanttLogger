'''
{
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
# https://qiita.com/castaneai/items/9cc33817419896667f34
# import threading
import concurrent.futures as confu

class Observer:
    def __init__(self):
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