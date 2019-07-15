from ganttlogger.modules.InitProcess import InitProcess
from ganttlogger.modules.Public import StrFormatter
from ganttlogger.modules.Alone import Alone
from ganttlogger.modules.Observer import WinObserver, MacObserver
from ganttlogger.modules.Logger import Logger
from ganttlogger.modules.Plotter import Plotter
from ganttlogger.modules.Displayer import Displayer

def main():
    '''
    Initial Process
    '''
    # A start of a module 'StrFormatter' for coloring terminal
    strformatter = StrFormatter()
    strformatter.start()
    # Main initialization
    init = InitProcess()
    os, mode, uuid = init.get_init_parameters()

    # Start main process(thread-loop) in accordance with mode
    if mode == "Alone":
        alone = Alone(os, uuid)
        alone.run()
    elif mode == "AloneWithPlot":
        alone = Alone(os, uuid, withplot=True)
        alone.run()
    elif mode == "Observer":
        print("We can't execute Observer because it hasn't been implemented.")
        # if os == "w":
        #     observer = WinObserver(uuid=uuid, is_alone=False)
        # elif os == "d":
        #     observer = MacObserver(uuid=uuid, is_alone=False)
        # observer.start()
    elif mode == "Logger":
        print("We can't execute Logger because it hasn't been implemented.")
        # logger = Logger(uuid)
        # plotter = Plotter(uuid)
        # logger.run_logger()
        # plotter.run()
    elif mode == "Plotter":
        plotter = Plotter()
        plotter.start()
    elif mode == "Displayer":
        displayer = Displayer()
        displayer.start()


if __name__ == "__main__":
    main()



