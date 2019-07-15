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

[How to create exe (for Windows)]
(for Windows)
> pipenv run pyinstaller -y --add-data "C:/Users/reegg/git/ActiveTabGanttLogger/modules/font/ipaexg.ttf";"config/ipaexg.ttf" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pypiwin32 --hidden-import colorama --hidden-import pyobjc --hidden-import pyobjc-framework-Quartz  "C:/Users/reegg/git/ActiveTabGanttLogger/app.py"

上のコマンドでは合ってる気がしないので，
> pipenv install auto-py-to-exe
> pipenv run auto-py-to-exe
をしてアプリケーションを起動して，
●Script Location  : app.pyを選択
●Onefile          : One Directoryを選択
(●Additional Files : ipaexg.ttfを追加)
●Advanced
・Output Directory: distフォルダを選択
・-n              : ganttlogger-exe
・--hidden-import : matplotlib,numpy,psutil,pynput,pypiwin32,colorama(,pyobjc,pyobjc-framework-Quartz)
'''

from modules.InitProcess import InitProcess
from modules.Public import StrFormatter
from modules.Alone import Alone
from modules.Observer import WinObserver, MacObserver
from modules.Logger import Logger
from modules.Plotter import Plotter
from modules.Displayer import Displayer

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

    # Start main process(thread-loop) in accordance with mode
    if mode == "Alone":
        alone = Alone(os, uuid)
        alone.run()
    elif mode == "AloneWithPlot":
        alone = Alone(os, uuid, withplot=True)
        alone.run()
    elif mode == "Observer":
        print("We can't execute Observer because it hasn't been implemented.")
        # if os == "w":
        #     observer = WinObserver(uuid=uuid, is_alone=False)
        # elif os == "d":
        #     observer = MacObserver(uuid=uuid, is_alone=False)
        # observer.start()
    elif mode == "Logger":
        print("We can't execute Logger because it hasn't been implemented.")
        # logger = Logger(uuid)
        # plotter = Plotter(uuid)
        # logger.run_logger()
        # plotter.run()
    elif mode == "Plotter":
        plotter = Plotter()
        plotter.start()
    elif mode == "Displayer":
        displayer = Displayer()
        displayer.start()


if __name__ == "__main__":
    '''
    ここの処理を実行する`pipenv run python app.py`は，お試し実装の場とする．
    コメントも日本語OKで．

    ●start()は標準入力や注意書きをターミナルに表示させるとかの直前の処理をしてからrun()する関数，run()はそのままrun()する．

    [メモ]
    ●拡張ディスプレイ・仮想デスクトップでもアクティブタブは認識できてる？
    ・仮想デスクトップだと，デスクトップ別のアクティブタブが選択される状態になる．
    →そこまで気にすることないか？
    →短時間でタブ切り替えされたアプリケーションは，使われないものとして除去するのもアリ
    →ガントチャートプロット時に1sより短かったら切り捨てるとか？
    ・拡張ディスプレイでやってもアクティブタブの単一検出はできた。
    '''
    main()



