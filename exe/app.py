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

[How to create exe]
- pyinstallerによるビルドは，Python実行ファイルへのパスが見えてしまうので，C直下にある(フォルダ`exe`下のファイル群をコピーした)プロジェクト`GanttLogger`配下にpipenvの仮想環境`.venv`を作成し，ビルドするようにする！！
- `config/font/ipaexg.ttf`は追加ファイルにせず実行可能ファイルと同階層にして一緒に圧縮することにする．  
つまり生成されて以下の出力構成になるようにする．
    ```
    dist
    ├ ganttlogger.exe
    ├ config
        └ font
            └ ipaexg.ttf
    └ ganttlogger-exe-<os>-<version>.zip
    ```
- 必要なWindows向けモジュールをインストール下pipenvを構築し，更に`pyinstaller`・`auto-py-to-exe`をインストール．
    - `pyinstaller`のみを使用
        ```
        > pipenv run pyinstaller -y -F -i "C:/BuildProjects/GanttLogger/icon/favicon.ico" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pypiwin32 --hidden-import colorama  "C:/BuildProjects/GanttLogger/app.py"
        ```
    - 出力先を指定してやる場合は`auto-py-to-exe`を使う(上のコマンドもauto-py-to-exeから得ている)．  
    なお，インストールできるモジュールにOS依存があるので，WindowsのモジュールはWindowsで，MacのモジュールはMacで，という感じにそれぞれのマシンで`auto-py-to-exe`を実行する．
        ```
        > pipenv install auto-py-to-exe
        > pipenv run auto-py-to-exe
        ```
        をしてアプリケーションを起動して，
        - Script Location  : app.pyを選択
        - Onefile          : One Directoryを選択
        - Advanced
            - Output Directory: `config/font/ipaexg.ttf`があるdistフォルダを選択
            - -n              : ganttlogger
            - --hidden-import : 
                - (Windows)matplotlib,numpy,psutil,pynput,pypiwin32,colorama
                - (MacOS)matplotlib,numpy,psutil,pynput,pyobjc,pyobjc-framework-Quartz
        - なお，上記で指定して得たコマンドが下記．
            - (Windows)※Python実行ファイルのパスにユーザ名が入らないようにディスクC直下にビルド用フォルダを配置し，プロジェクト配下にpipenvの仮想環境フォルダ`.venv`が生成されるようにする．  
            (参考:[Windowsでのpipenv](https://qiita.com/youkidkk/items/b6a6e39ee3a109001c75#-%E7%92%B0%E5%A2%83%E5%A4%89%E6%95%B0%E3%81%AE%E8%BF%BD%E5%8A%A0))
                ```
                pyinstaller -y -F -i "C:/BuildProjects/GanttLogger/icon/favicon.ico" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pypiwin32 --hidden-import colorama  "C:/BuildProjects/GanttLogger/app.py"
                ```
            - (Mac)※ユーザ名がusrになるのでどこでもよい？ただし，pipenvなど仮想環境には標準モジュールのはずのdistutilsが入っていないようで、仮想環境ではないローカルでpyinstallerを実行すべき．  
            また，過去版の`ganttlogger.spec`・`build`・`ganttlogger.exec`を削除してから実行するほうが，最新になることは確実なので堅実に．
                ```
                pyinstaller -y -F -i "/Users/<usrname>/Desktop/VSCodeProjects/python/GanttLogger/exe/icon/favicon.ico" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pyobjc --hidden-import pyobjc-framework-Quartz  "/Users/<usrname>/Desktop/VSCodeProjects/python/GanttLogger/exe/app.py"
                ```
                または，(pipenv runは，distを出力するディレクトリに移動してから実行すること．)
                ```
                ($ pipenv run )pyinstaller -y --onefile -i "/Users/<usrname>/Desktop/VSCodeProjects/python/GanttLogger/exe/icon/favicon.ico" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pyobjc --hidden-import pyobjc-framework-Quartz  "/Users/<usrname>/Desktop/VSCodeProjects/python/GanttLogger/exe/app.py"
                ```


- 実行ファイルの実行について
    - Windowsは普通に`> ganttlogger`でいける．
    - Macは`$ ./ganttlogger`で実行できる．
    - いずれにしても，システム環境変数に登録すれば`ganttlogger`で動かせる．

- **`config/font/ipaexg.ttf`と実行可能ganttloggerをフォルダ`ganttlogger`に入れてから圧縮**し，圧縮フォルダ名を`ganttlogger-exe-<macos|win_x86_64>-<Version>`として公開．
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



