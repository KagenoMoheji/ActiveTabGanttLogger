# import threading
import concurrent.futures as confu
from modules.StrFormatter import StrFormatter
from modules.Observer import Observer
from modules.Logger import Logger, RawDataStore
from modules.Plotter import Plotter

class Alone:
    store = None
    observer = None
    logger = None
    plotter = None
    strfmr = None
    def __init__(self, os):
        self.store = RawDataStore()
        self.observer = Observer(os)
        self.logger = Logger()
        self.plotter = Plotter()
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
        pass


