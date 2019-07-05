import platform
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter
from modules.Public import StrFormatter

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
            mode (str): "Alone" or "Observer" or "Logger"
            uuid ("" | str): UUID when mode is not "Alone" and "Plotter"

        References:
            http://ja.pymotw.com/2/platform/
        '''
        os = self.get_os()
        mode = self.argparser.identify_mode()
        if mode == "Plotter":
            uuid = "None"
        elif (mode == "Alone") or (mode == "Observer"):
            uuid = self.generate_uuid()
        elif mode == "Logger":
            uuid = self.argparser.uuid
        else:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid variable in mode of InitProcess.py"))
            exit()

        print("OS: {}".format(os))
        print("mode: {}".format(mode))
        print("Your ID is: {}".format(uuid))

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

        References:
            http://ja.pymotw.com/2/platform/
        '''
        os = platform.platform(terse=True)

        # This CLI can work on Windows or Mac
        if ("Windows" in os) or ("Darwin" in os):
            return os
        else:
            print(self.strfmr.get_colored_console_log("red",
                "Error: This can work on 'Windows' or 'MacOS'"))
            exit()

    def generate_uuid(self):
        '''
        Generate UUID.

        Args:
            None

        Returns:
            (str): UUID

        References:
            https://www.python.ambitious-engineer.com/archives/1436
        '''
        return uuid.uuid4()

class ArgsParser:
    parser = None
    args = None
    uuid = ""
    strfmr = None
    def __init__(self):
        '''
        Parse cli options.

        References:
            https://docs.python.org/ja/3/library/argparse.html
            https://chroju.github.io/blog/2019/02/19/how_to_write_usage/
            https://qiita.com/petitviolet/items/aad73a24f41315f78ee4
            https://pod.hatenablog.com/entry/2017/02/11/194834
            https://qiita.com/Alice1017/items/0464a38ab335ac3b9336
            https://stackoverflow.com/a/3853776
        '''
        self.strfmr = StrFormatter()
        usage = "ganttlogger [--observer] [--logger] [--uuid <UUID>] [--help] [--plotter]"
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
            help="Use this option if you want other outputs by a log after getting one and a graph."
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
                exit()
            mode = "Logger"
            self.uuid = self.args.uuid
        elif self.args.plotter:
            mode = "Plotter"
        else:
            if self.args.uuid:
                print(self.strfmr.get_colored_console_log("red",
                    "Error: You may need '--logger'."))
                exit()
            mode = "Alone"
        
        return mode