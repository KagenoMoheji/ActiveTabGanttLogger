import sys
import threading
# import concurrent.futures as confu
import platform

class MyThread(threading.Thread):
    callback = None
    def __init__(self, target):
        super(MyThread, self).__init__()
        self.callback = target
        self.stop_event = threading.Event()
        self.setDaemon(True)
    def stop(self):
        self.stop_event.set()
    def start(self):
        self.callback()

class StrFormatter:
    # Standardly, 'terminalColors' has escape sequences for MacOS and Unix.
    terminalColors = {
        "red": "\u001b[31m",
        "yellow": "\u001b[33m",
        "clear": "\u001b[0m"
    }
    def start(self):
        '''
        When executed in __init__, it is executed each time this class is instantiated, so it is prevented by coding in this function.
        '''
        os = platform.platform(terse=True)
        if "Windows" in os:
            # If os is Windows, use module 'colorama'. And only init to fit terminal to ANSI.
            # Mac and Unix can't import colorama, so import here.
            from colorama import init
            init()

    def get_colored_console_log(self, color, message):
        '''
        Show colored message like error or warning in terminal.

        Args:
            coloe (str): "red" or "yellow"
            message (str): Alert message

        Returns:
            (str): Colored text for terminal
        '''
        if not color in self.terminalColors:
            print("{0}Error: Invalid in Arg 'color'.\nYou can select from 'yellow' or 'red'.{1}".format(self.terminalColors["red"], self.terminalColors["clear"]))
            sys.exit()
        return "{0}{1}{2}".format(self.terminalColors[color], message, self.terminalColors["clear"])

