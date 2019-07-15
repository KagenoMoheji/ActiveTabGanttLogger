from modules.Public import StrFormatter
from modules.Observer2 import Observer
from modules.Logger import Logger
from modules.Plotter import Plotter

class Alone:
    observer = None
    logger = None
    plotter = None
    strfmr = None
    def __init__(self, os, uuid):
        self.observer = Observer(os, uuid)
        self.logger = Logger(uuid)
        self.plotter = Plotter(uuid)
        self.strfmr = StrFormatter()
    
    def run(self):
        '''
        [alone]
        storeの配列をキューとして扱って，observerは後ろに追加していき，
        loggerは前から取っていく(空なら何もしない)ことをすればよいか！
        plotterはobserver・loggerの処理が終わったあとに行う．
        つまりスレッド数は最大2つ．

        ・・・けど，observer・loggerが単体でやるときはどうしよう．
        [observer]
        ・逐次送信？数分おきにまとめて送信？
        [logger]
        ・logger終了後にplotterなので，受信と記録のスレッド2つ？
        '''
        # このあたりでスレッド展開
        print("Hello, Alone!")


