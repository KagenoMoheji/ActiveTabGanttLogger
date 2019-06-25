class Alert:
    terminalColors = {
        "red": "\u001b[31m",
        "yellow": "\u001b[33m",
        "clear": "\u001b[0m"
    }

    def coloredAlert(self, color, message):
        if not color in self.terminalColors:
            print("{0}Error: Invalid in Arg 'color'.\nYou can select from 'yellow' or 'red'.{1}".format(self.terminalColors["red"], self.terminalColors["clear"]))
            exit()
        print("{0}{1}{2}".format(self.terminalColors[color], message, self.terminalColors["clear"]))
