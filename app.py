from modules.InitProcess import InitProcess

def main():
    # Initial Process
    init = InitProcess()
    os, mode, uuid = init.get_init_parameters()
    print("OS: {}".format(os))
    print("Your ID is: {}".format(uuid))

    # Start main process in accordance with mode

    # Close process


if __name__ is "__main__":
    main()