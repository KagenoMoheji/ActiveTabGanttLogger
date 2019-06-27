# ActiveTabGanttLogger
アクティブウィンドウログをガントチャートで出力する

## 流れ
1. プロセスログを取得
2. プロセスID(名前)，開始時刻を配列に
3. 遷移したらその時刻を終了時刻としても配列にし，直後のプロセスの開始時刻にもする
4. 終了アクションがあったら出力処理でガントチャートをプロセスID(名前)別に時系列に出力
5. 図の保存

## テスト環境
- OS
    - Windows10 64bit
    - MacOS Mojave10.14.5
- ブラウザ
    - Google Chrome75.0.3770.100
- Python
    - 3.7

## 名称やコマンドの改名
- 「ActiveTabGanttLogger」や`ganttlogger`は微妙
- アクティブウィンドウ遷移・マウス・キーボードを観測してガントチャート・折れ線・棒グラフを出力するし…
- タスクを監視…「PCTaskObserver」と`taskobserver`？
- ほかに良い名前無いかな…

## 仕様
- MouseObserver・KeyboardObserverの最低デルタtは1s．
