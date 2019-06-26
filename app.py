from modules.InitProcess import InitProcess
from modules.StrFormatter import StrFormatter
from modules.Observer import Observer
from modules.Logger import Logger

'''
[How to test]
If you have setted the pipenv, start from (3).
Or, if you have installed this CLI, start from (4).
(1)Install pipenv.
`python -m pip install pipenv` or `pip3 install pipenv`
(2)Create virtual python environment with pipenv.
`pipenv --python 3.7`
(3)Install this CLI.
`pipenv run python -m pip install -e .` or `pipenv run pip3 install -e .`
(4)Run CLI.
`pipenv run ganttlogger`
'''

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
    # print("OS: {}".format(os)) # "w" or "d"

    # Start main process(thread-loop) in accordance with mode
    if mode is "Alone":
        alone(os)
    elif mode is "Observer":
        observer(os, uuid)
    elif mode is "Logger":
        logger(os, uuid)
    '''
    elif mode is "Plotter":
        plotter(os)
    '''

    # Exit the loop above
    # Close process here? or in functions below?

def alone(os):
    print("This mode is Alone")

def observer(os, uuid):
    print("This mode is Observer")

def logger(os, uuid):
    print("This mode is Logger")

'''
def plotter():
    pass
'''



if __name__ == "__main__":
    '''
    Command `pipenv run python app.py` is run to check the action of modules.
    '''
    # main()

    # psutilモジュールではアクティブタブは分からなさそう．
    import psutil
    # https://githubja.com/giampaolo/psutil
    # https://psutil.readthedocs.io/en/latest/#process-class
    for ps in psutil.process_iter():
        text = """\
ppid: {ppid}
pid: {pid}
name: {name}
status: {status}
============================
""".format(ppid=ps.ppid(), pid=ps.pid, name=ps.name(), status=ps.status())
        print(text)