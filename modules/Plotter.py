'''
●ログファイルを読み込んでガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import numpy as np
import matplotlib.pyplot as plt

class Plotter:
    uuid = ""
    def __init__(self, uuid=""):
        # uuidが空 -> plotterモード -> カレントディレクトリに出力
        # uuidがある -> Alone or Logger -> 引数のuuidを使って出力先指定
        if uuid:
            self.uuid = uuid
        pass

    def start(self):
        '''
        ●標準入力で
        (1)出力モードの選択(filter_tab/set_interval)
        (2)出力モードに合わせた必須項目への回答
        ・fiter_tab -> 不要なタブ名(ログからコピペ)をまとめたテキストファイルの指定
        ・set_interval -> デルタtの数値指定(単位は秒)
        '''
        print("Start, Plotter!")

    def run(self):
        print("Run, Plotter!")

    def plot_activetab(self):
        pass
    
    def plot_mouse(self):
        pass

    def plot_keyboard(self):
        pass