import sys
import platform
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter
from ganttlogger.modules.Public import StrFormatter

class InitProcess:
    argparser = None
    strfmr = None
    def __init__(self):
        '''
        Prepare in some initial processes.
        '''
        self.argparser = ArgsParser()
        self.strfmr = StrFormatter()

    def get_init_parameters(self):
        '''
        Get initial parameters.

        Args:
            None

        Returns:
            os (str): OS and its version
            mode (str): "Alone" or "AloneWithPlot" or "Observer" or "Logger" or "Plotter" or "Displayer"
            uuid ("" | str): UUID when mode is not "Plotter" and "Displayer"
        '''
        os = self.get_os()
        mode = self.argparser.identify_mode()
        if (mode == "Plotter") or (mode == "Displayer"):
            uuid = "None"
        elif (mode == "Alone") or (mode == "Observer") or (mode=="AloneWithPlot"):
            uuid = self.generate_uuid()
        elif mode == "Logger":
            uuid = self.argparser.uuid
        else:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid variable in mode of InitProcess.py"))
            sys.exit()

        print(self.strfmr.get_colored_console_log("yellow", """\
OS        : {os}
mode      : {mode}
Your ID is: {uuid}
""".format(os=os, mode=mode, uuid=uuid)))

        # Get simpler os parameter
        if "Windows" in os:
            os = "w"
        elif "Darwin" in os:
            os = "d"

        return os, mode, uuid
    
    def get_os(self):
        '''
        Get OS and its version of platform.

        Args:
            None

        Returns:
            os (str): OS and its version
        '''
        os = platform.platform(terse=True)

        # This CLI can work on Windows or Mac
        if ("Windows" in os) or ("Darwin" in os):
            return os
        else:
            print(self.strfmr.get_colored_console_log("red",
                "Error: This can work on 'Windows' or 'MacOS'"))
            sys.exit()

    def generate_uuid(self):
        '''
        Generate UUID.

        Args:
            None

        Returns:
            (str): UUID
        '''
        return str(uuid.uuid4())

class ArgsParser:
    parser = None
    args = None
    uuid = ""
    strfmr = None
    def __init__(self):
        '''
        Parse cli options.
        '''
        self.strfmr = StrFormatter()
        usage = "ganttlogger [--observer] [--logger] [--uuid <UUID>] [--help] [--plotter] [--withplot] [--displayer]"
        self.parser = ArgumentParser(
            prog="ganttlogger",
            description="""\
This CLI will do Observing active-tab, mouse, keyboard,
and Logging them,
and Plotting graphs (active-tab=ganttchart, mouse=line, keyboard=bar).
{}""".format(self.strfmr.get_colored_console_log("yellow",
"If you don't set any option, this work both of 'observer' and 'logger'.")),
            usage=usage,
            formatter_class=RawTextHelpFormatter
        )
        self.parser.add_argument(
            "-o", "--observer",
            action="store_true",
            help="The role of this PC is only observing action."
        )
        self.parser.add_argument(
            "-l", "--logger",
            action="store_true",
            help="The role of this PC is only logging and plotting. You must also set '--uuid'."
        )
        self.parser.add_argument(
            "-u", "--uuid",
            type=str,
            dest="uuid",
            help="When you set '--logger', you must also set this by being informed from 'observer' PC."
        )
        self.parser.add_argument(
            "-p", "--plotter",
            action="store_true",
            help="Use this option if you want other outputs by a log in the current directory after getting one and a graph."
        )
        self.parser.add_argument(
            "--withplot",
            action="store_true",
            help="Use this option when you want to get a graph after running 'Alone'."
        )
        self.parser.add_argument(
            "-d", "--displayer",
            action="store_true",
            help="Use this option when you want to look a graph from a '.pkl' file."
        )
        self.args = self.parser.parse_args()

    def identify_mode(self):
        '''
        Identify mode from args.

        Args:
            None

        Returns:
            mode (str): "Alone" or "Observer" or "Logger"
        '''
        mode = ""
        if self.args.observer:
            mode = "Observer"
        elif self.args.logger:
            if not self.args.uuid:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: Logger missing an option '--uuid <UUID>'."))
                sys.exit()
            mode = "Logger"
            self.uuid = self.args.uuid
        elif self.args.plotter:
            mode = "Plotter"
        elif self.args.displayer:
            mode = "Displayer"
        else:
            if self.args.uuid:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: You may need '--logger'."))
                sys.exit()
            if self.args.withplot:
                mode = "AloneWithPlot"
            else:
                mode = "Alone"
        
        return mode