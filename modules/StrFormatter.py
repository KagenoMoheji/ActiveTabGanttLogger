import platform
from colorama import Fore

# Check on Mac! If colored, you can remove commentouts below!!

class StrFormatter:
    # We can use this in only whose terminal uses UTF8 like MacOS.
    # terminalColors = {
    #     "red": "\u001b[31m",
    #     "yellow": "\u001b[33m",
    #     "clear": "\u001b[0m"
    # }
    # def __init__(self):
    #     # WindowsだったらShiftJISに変換しようと思ったけど，色つかなかった．
    #     os = platform.platform(terse=True)
    #     if "Windows" in os:
    #         self.terminalColors = {k: v.encode("shift-jis") for (k, v) in self.terminalColors.items()}

    def get_colored_console_log(self, color, message):
        '''
        Show colored message like error or warning in terminal.

        Args:
            coloe (str): "red" or "yellow"
            message (str): Alert message

        Returns:
            None
        '''
        # if not color in self.terminalColors:
        #     print("{0}Error: Invalid in Arg 'color'.\nYou can select from 'yellow' or 'red'.{1}".format(self.terminalColors["red"], self.terminalColors["clear"]))
        #     exit()
        # return "{0}{1}{2}".format(self.terminalColors[color], message, self.terminalColors["clear"])
        if color is "red":
            return "{0}{1}{2}".format(Fore.RED, message, Fore.RESET)
        elif color is "yellow":
            return "{0}{1}{2}".format(Fore.YELLOW, message, Fore.RESET)
        else:
            print("{0}Error: Invalid in Arg 'color'.\nYou can select from 'yellow' or 'red'.{1}".format(Fore.RED, Fore.RESET))
            exit()
