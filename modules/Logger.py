'''
●jsonを引数に受け取る
●jsonのid順にログ追記
●生ログ出力
●ガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import matplotlib.pyplot as plt
import numpy as np
# import threading
import concurrent.futures as confu
from datetime import datetime # 定期間隔書き出しのタイムスタンプ用

class Logger:
    os = ""
    def __init__(self, os, uuid=""):
        self.os = os
        if uuid:
            self.uuid = uuid
        # データ受け取り・定期間隔でのファイル書き出しの並列処理なので最大2？
        pass

    def close(self): pass

class PlotGraph:
    def __init__(self): pass