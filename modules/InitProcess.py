import platform
import uuid
from argparse import ArgumentParser
from modules.Alert import Alert

class InitProcess:
    argparser = None
    alert = None
    def __init__(self):
        self.argparser = ArgsParser()

    def get_init_parameters(self):
        '''
        Get init parameters.

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
        mode = self.argparser.get_mode()
        if mode is "Alone":
            uuid = ""
        elif mode is "Observer":
            uuid = self.generate_uuid()
        elif mode is "Logger":
            uuid = self.argparser.uuid
        else:

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
    uuid = ""
    def __init__(self):
        '''
        Parse cli options.

        References:
            https://chroju.github.io/blog/2019/02/19/how_to_write_usage/
            https://qiita.com/petitviolet/items/aad73a24f41315f78ee4
            https://pod.hatenablog.com/entry/2017/02/11/194834
            https://qiita.com/Alice1017/items/0464a38ab335ac3b9336
        '''
        usage = "ganttlooger [--observer] [--logger <UUID>] [--help]"
        self.parser = ArgumentParser(usage=usage)

    def get_mode():