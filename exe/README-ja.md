# GanttLogger(exe)
Pythonのインストール不要で使用できるganttloggerの実行ファイル．
- [README.md - in English](https://github.com/KagenoMoheji/GanttLogger/blob/master/exe/README.md)

## 導入
- <span id="w">**Windows**</span>
    1. [Releases](https://github.com/KagenoMoheji/GanttLogger/releases)から最新版の`ganttlogger-exe-x86_64-<version>.zip`をダウンロードします．
    2. `ganttlogger-exe-x86_64-<version>.zip`を解凍します．
    3. `ganttlogger.exe`があるフォルダ`ganttlogger`までのパスをシステム環境変数に登録します(システム環境変数のPathに新規作成するやつ)．
    4. これでコマンド`ganttlogger`を使うことができます．
    5. なお，クイックスタートについては，[クイックスタート - README 日本語版](https://github.com/KagenoMoheji/GanttLogger/blob/master/README-ja.md#2-2)を参照してください．
<span id="m">**MacOS**</span>
    1. [Releases](https://github.com/KagenoMoheji/GanttLogger/releases)から最新版の`ganttlogger-exe-macos-<version>.zip`をダウンロードします．
    2. `ganttlogger-exe-macos-<version>.zip`を解凍します．
    3. `ganttlogger.exe`があるフォルダ`ganttlogger`までのパスを下記コマンドでシステム環境変数に登録します．
        ```
        $ echo 'export PATH=<ganttloggerまでのパス>/ganttlogger:$PATH' >> ~/.bash_profile
        $ source ~/.bash_profile
        ```
    4. ターミナルを再起動することで，コマンド`ganttlogger`を使うことができます．
    5. なお，クイックスタートについては，[クイックスタート - README 日本語版](https://github.com/KagenoMoheji/GanttLogger/blob/master/README-ja.md#2-2)を参照してください．