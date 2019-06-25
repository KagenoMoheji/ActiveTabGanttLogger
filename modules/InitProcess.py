import platform
import uuid
from argparse import ArgumentParser, RawTextHelpFormatter
from modules.StrFormatter import StrFormatter

class InitProcess:
    argparser = None
    strformatter = None
    def __init__(self):
        '''
        Prepare in some initial processes.
        '''
        self.argparser = ArgsParser()
        self.strformatter = StrFormatter()

    def get_init_parameters(self):
        '''
        Get initial parameters.

        Args:
            None

        Returns:
            os (str): OS and its version
            mode (str): "Alone" or "Observer" or "Logger"
            uuid ("" | str): UUID when mode is not "Alone"

        References:
            http://ja.pymotw.com/2/platform/
        '''
        os = self.get_os()
        mode = self.argparser.identify_mode()
        if mode is "Alone":
            uuid = "None"
        elif mode is "Observer":
            uuid = self.generate_uuid()
        elif mode is "Logger":
            uuid = self.argparser.uuid
        else:
            print(self.strformatter.get_colored_console_log("red",
                "Error: Invalid variable in mode of InitProcess.py"))
            exit()

        return os, mode, uuid
    
    def get_os(self):
        '''
        Get OS and its version of platform.

        Args:
            None

        Returns:
            (str): OS and its version

        References:
            http://ja.pymotw.com/2/platform/
        '''
        return platform.platform(terse=True)

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
    strformatter = None
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
        self.strformatter = StrFormatter()
        usage = "ganttlogger [--observer] [--logger] [--uuid <UUID>] [--help]"
        self.parser = ArgumentParser(
            prog="ganttlogger",
            description="""\
Observing active-tab, mouse, keyboard,
and Logging them,
and Plot graphs (active-tab=ganttchart, mouse=line, keyboard=bar).
{}""".format(self.strformatter.get_colored_console_log("yellow",
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
            mode = "Logger"
            if not self.args.uuid:
                print(self.strformatter.get_colored_console_log("red",
                    "Error: Logger missing an option '--uuid <UUID>'."))
                exit()
            self.uuid = self.args.uuid
        else:
            if self.args.uuid:
                print(self.strformatter.get_colored_console_log("red",
                    "Error: You may need '--logger'."))
                exit()
            mode = "Alone"
        return mode