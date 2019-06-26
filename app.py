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
    ここの処理を実行する`pipenv run python app.py`は，お試し実装の場とする．
    コメントも日本語OKで．
    '''
    # main()

#     # Get PID and its name
#     # https://githubja.com/giampaolo/psutil
#     # https://psutil.readthedocs.io/en/latest/#process-class
#     # psutilモジュールではアクティブタブは分からなさそう．
#     # psutil: {Windows: OK, MacOS: OK}
    import psutil
#     for ps in psutil.process_iter():
#         text = """\
# ppid: {ppid}
# pid: {pid}
# name: {name}
# status: {status}
# ============================
# """.format(ppid=ps.ppid(), pid=ps.pid, name=ps.name(), status=ps.status())
#         print(text)

    # [Windows10-64bit]Get active window
    # (wnck)https://askubuntu.com/a/483619 -> Failed. Only run on Unix?
    # (linux向けらしい)https://stackoverflow.com/questions/46628209/get-the-process-of-the-active-window-with-python-in-linux
    # (win32gui)https://www.reddit.com/r/learnpython/comments/90onta/getting_activeforeground_window_title_on_windows/
    # win32guiのモジュールのインストールについて
    # http://blog.livedoor.jp/kmiwa_project/archives/1058907748.html
    # https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/
    # https://github.com/mhammond/pywin32/releases
    # https://stackoverflow.com/questions/42370339/python-3-6-install-win32api
    # https://github.com/Googulator/pypiwin32
    # Windows10-64bitに向けては，`pip install pypiwin32`を採用
    import win32gui as w
    import win32process as wp
    from datetime import datetime
    import time
    # pids = wp.GetWindowThreadProcessId(w.GetForegroundWindow())
    # print(psutil.Process(pids[-1]))
    current_active_pid = -1
    try:
        while True:
            # 同じアプリケーションで異なるウィンドウを開いていても同じpidで区別はつかないらしい
            pid = wp.GetWindowThreadProcessId(w.GetForegroundWindow())[-1]
            if pid is not current_active_pid:
                current_active_pid = pid
            print("{time}: {pid}: {active_name}".format(
                time=datetime.now().strftime("%H:%M:%S.%f"),
                pid=current_active_pid,
                active_name=psutil.Process(current_active_pid).name()))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit")
    # [MacOS]Get active window
    # (Win: win32gui, Mac: Appkit)https://stackoverflow.com/a/36419702
    # (Mac Appkit)https://codeday.me/jp/qa/20190523/885948.html
    # (Mac向け？xpropやxdotoolのインストールが必要？)https://stackoverflow.com/questions/3983946/get-active-window-title-in-x
    



