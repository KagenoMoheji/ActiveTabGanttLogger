# GanttLogger(exe)
Windowsのexe向け．Pythonインストール不要で動く？？？(まだ確認していない)

### ビルド方法個人メモ
- pyinstallerによるビルドは，Python実行ファイルへのパスが見えてしまうので，C直下にある(フォルダ`exe`下のファイル群をコピーした)プロジェクト`GanttLogger`配下にpipenvの仮想環境`.venv`を作成し，ビルドするようにする！！
- 必要なWindows向けモジュールをインストール下pipenvを構築し，更に`pyinstaller`・`auto-py-to-exe`をインストール．
    - `pyinstaller`のみを使用
        ```
        > pipenv run pyinstaller -y --add-data "C:/Users/reegg/git/ActiveTabGanttLogger/modules/font/ipaexg.ttf";"config/ipaexg.ttf" -n ganttlogger --hidden-import matplotlib --hidden-import numpy --hidden-import psutil --hidden-import pynput --hidden-import pypiwin32 --hidden-import colorama --hidden-import pyobjc --hidden-import pyobjc-framework-Quartz  "C:/Users/reegg/git/ActiveTabGanttLogger/app.py"
        ```

    - 上のコマンドでは合ってる気がしないし，出力先を指定できないっぽいので，`auto-py-to-exe`を使う．
        ```
        > pipenv install auto-py-to-exe
        > pipenv run auto-py-to-exe
        ```
        をしてアプリケーションを起動して，
        - Script Location  : app.pyを選択
        - Onefile          : One Directoryを選択
        - ~~Additional Files : ipaexg.ttfを追加~~
        - Advanced
            - Output Directory: distフォルダを選択
            - -n              : ganttlogger
            - --hidden-import : matplotlib,numpy,psutil,pynput,pypiwin32,colorama (,pyobjc,pyobjc-framework-Quartz)

- 圧縮フォルダ名を`ganttlogger-exe`として公開．
