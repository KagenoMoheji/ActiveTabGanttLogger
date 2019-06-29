# import threading
import concurrent.futures as confu
from modules.StrFormatter import StrFormatter
from modules.Observer import Observer
from modules.Logger import Logger
from modules.Plotter import Plotter

class Alone:
    observer = None
    logger = None
    plotter = None
    strfmr = None
    def __init__(self, os):
        self.observer = Observer(os)
        self.logger = Logger()
        self.plotter = Plotter()
        self.strfmr = StrFormatter()
    
    def start(self):


