from modules.InitProcess import InitProcess
from modules.StrFormatter import StrFormatter

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

    print("OS: {}".format(os))

    # Start main process in accordance with mode

    # Close process


if __name__ is "__main__":
    main()