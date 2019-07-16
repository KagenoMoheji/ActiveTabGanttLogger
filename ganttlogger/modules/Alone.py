import sys
import threading
import time
from ganttlogger.modules.Public import StrFormatter
import ganttlogger.modules.Global as global_v
from ganttlogger.modules.Observer import WinObserver, MacObserver
from ganttlogger.modules.Logger import Logger
from ganttlogger.modules.Plotter import Plotter

class Alone:
    uuid = ""
    observer = None
    logger = None
    strfmr = None
    withplot = False
    def __init__(self, os, uuid, withplot=False):
        '''
        Work as all of 'observer', 'logger' and 'plotter'.
        '''
        self.uuid = uuid
        if os == "w":
            self.observer = WinObserver(uuid=self.uuid, is_alone=True)
        elif os == "d":
            self.observer = MacObserver(uuid=self.uuid, is_alone=True)
        self.logger = Logger(uuid=self.uuid)
        self.strfmr = StrFormatter()
        self.withplot = withplot
    
    def run(self):
        th_observer = threading.Thread(target=self.observer.run)
        th_logger = threading.Thread(target=self.logger.output)
        th_observer.start()
        th_logger.start()

        while not global_v.cli_exit:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                continue
        if global_v.is_threadloop_error: # When "Thread loop exited by any problem!!!!" occured
            sys.exit()

        while not global_v.finish_logging:
            time.sleep(1)
        if self.withplot:
            plotter = Plotter(self.uuid)
            plotter.run()


