from modules.InitProcess import InitProcess
import colorama

def main():
    # Initial Process
    colorama.init() # Initialization of colorama for StrFormat.py
    init = InitProcess()
    os, mode, uuid = init.get_init_parameters()
    print("OS: {}".format(os))
    print("mode: {}".format(mode))
    print("Your ID is: {}".format(uuid))

    # Start main process in accordance with mode

    # Close process


if __name__ is "__main__":
    main()