import threading
from modules.Public import StrFormatter
from modules.Observer import WinObserver, MacObserver
from modules.Logger import Logger
from modules.Plotter import Plotter

class Alone:
    observer = None
    logger = None
    plotter = None
    strfmr = None
    def __init__(self, os, uuid):
        if os == "w":
            self.observer = WinObserver(uuid=uuid, is_alone=True)
        elif os == "d":
            self.observer = MacObserver(uuid=uuid, is_alone=True)
        self.logger = Logger(uuid=uuid)
        self.plotter = Plotter(uuid)
        self.strfmr = StrFormatter()
    
    def run(self):
        th_observer = threading.Thread(target=self.observer.run)
        th_logger = threading.Thread(target=self.logger.output)
        th_observer.start()
        th_logger.start()
        # while True:
        #     if global_v.is_switched_to_exit:
        #         self.plotter.run()
        #     sleep(5)


