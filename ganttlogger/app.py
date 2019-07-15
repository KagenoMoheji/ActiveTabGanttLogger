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

[How to create packages (for Windows, Mac)]
Reference:
    https://qiita.com/cvusk/items/00294f7f0cb38f420584
    
> pipenv run python setup.py sdist --formats=gztar,zip

上記コマンドではpipパッケージが作成されるが，pythonとpipがクライアント側でインストールされていないといけない．
ちなみにインストールは
> python -m pip install -e .
$ pip3 install -e .
というより，下の方が3つ目のパスが表示されずそれっぽいので良い
> python setup.py install
$ python3 setup.py install
'''

from ganttlogger.modules.InitProcess import InitProcess
from ganttlogger.modules.Public import StrFormatter
from ganttlogger.modules.Alone import Alone
from ganttlogger.modules.Observer import WinObserver, MacObserver
from ganttlogger.modules.Logger import Logger
from ganttlogger.modules.Plotter import Plotter
from ganttlogger.modules.Displayer import Displayer

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



