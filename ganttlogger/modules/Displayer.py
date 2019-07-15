import sys
import pickle
import matplotlib.pyplot as plt
from ganttlogger.modules.Public import StrFormatter

class Displayer:
    strfmr = None
    filename = ""
    def __init__(self):
        '''
        Load .pkl and display a graph with matplotlib on Python.
        '''
        self.strfmr = StrFormatter()
        self.filename = ""

    def start(self):
        while True:
            print(self.strfmr.get_colored_console_log("yellow",
                    "Input file name of '.pkl': "), end="")
            self.filename = input().strip()
            if not self.filename:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: Invalid input."))
                continue
            if not ".pkl" in self.filename:
                self.filename += ".pkl"
            break
        self.display()
    
    def display(self):
        try:
            with open(self.filename, "rb") as f:
                fig = pickle.load(f)
            plt.show()
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: File not found."))
            sys.exit()