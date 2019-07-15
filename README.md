# GanttLogger
アクティブウィンドウログをガントチャートで出力する

## 構成
```
GanttLogger
├ setup.py [PyPI用設定ファイル]
├ MANIFEST.in [PyPI用設定ファイル]
├ ganttlogger [PyPI用コード]
├ exe [Windows対応exe用コード]
├ server [まだ開発しない]
├ dust [蓄積した予備・メモのコード]
├ public [公開するパッケージ・実行ファイル]
├ .gitignore
├ README.md
```

## テスト環境
- OS
    - Windows10 64bit
    - MacOS Mojave10.14.5
- ブラウザ
    - Google Chrome75.0.3770.100
- Python
    - 3.7

## 仕様
- MouseObserver・KeyboardObserverの最低デルタtは1s．
    - 1s間の操作量ごとに取得
- 出力される`active_tab.log`の最初と最後のレコードは証明用のタイムスタンプ用なので削除しないように．
- Plotterにおいて最初と最後のレコードはフィルタリングから免除している．
- `ganttlogger -p`について
    - `filter_tab`において`active_tab.log`のTabTextが空欄になっている行を削除したい場合は，フィルタータブのリストのテキストファイルに`None`を追加する．
- 文字コードは基本`utf-8`．なのでフィルタリングするタブリストのテキストファイルの文字コードもそれに合わせるのが好ましい．
- マウス・キーボードの両方がNoneになった場合以下のケースであるとしてデータから除去する
    - スリープ中である
    - 運悪く同じ秒のタイムスタンプが2連続してしまった(ごくまれかつ短時間なので除去しても気にしない？)
    - `ganttlogger`の監視が中断されて`Logging is sleeping. Will you exit?(Y/n) :`の入力待ちである
        - スリープ中との区別は，`Shift + Ctrl(Command)`の入力による直前のキーボード打鍵数の増加かな？
        - 直前に出てこない，直後に出てきてる気がする．

## 課題点
- [x] `active_tab.log`における`TabText=""=None`をどう定義する…？
    - よくわからない「アプリケーション別その他」に統一？
    - 特段何もしない．取り除きたければフィルタータブリストのテキストファイルに`None`を追記する．
- モジュール選定
    - [x] `threading.Thread`か？`concurrent.futures.ThreadPoolExecutor`か？
        - てかマルチスレッドかマルチプロセスかもわからん
        - とりま`threading.Thread`でやるか，自前関数で外部からの操作ができるかもだし．  
        `concurrent.futures`のは詳しく調べられないからよくわからん．
        - [Pythonの並列・並行処理サンプルコードまとめ | Qiita](https://qiita.com/castaneai/items/9cc33817419896667f34)
        - `KeyboardObserver`クラスで`threading.Thread`を継承した`MyThread`クラスを使用することにして，その親である`Observer`クラスで`threading.Thread`と`MyThread`クラスが使えなかったのでそちらは`concurrent.futures`を簡単に使い，更にその親である`Alone`クラスでは`concurrent.futures`と`MyThread`クラスが使えなかったので`threading.Thread`を使う方針にした．
            - [pythonでのスレッド](http://nobunaga.hatenablog.jp/entry/2016/06/03/204450)
            - これを見るに，親子のスレッドで同じモジュールやそれを継承したサブクラスを使用することができないってことなのか？？？
    - [x] `numpy.append()/pop()`か？`collections.deque.append()/popleft()`か？`[].append()/pop(0)`か？
        - 読んだ感じでは`collections.deque`>`[]`>`numpy`かねぇ．
        - [Python キュー（queue）を使う（先入れ先出し）](https://pg-chain.com/python-queue)
        - [python と numpy の配列。追加や削除、ソートなど基本操作](http://ailaby.com/list_array/#id3_2)
        - [速度：Pythonの配列の末尾に要素追加 | Qiita](https://qiita.com/ykatsu111/items/be274f76d42f6b982ba4)
        - [Pythonでリスト（配列）の要素を削除するclear, pop, remove, del](https://note.nkmk.me/python-list-clear-pop-remove-del/#pop)
    - [x] `matplotlib`か？`plotly`か？
        - `plotly.figure_factory.create_gantt`では，秒単位・サブプロットの描写ができない．
        - `matplotlib`で頑張ってみる
    - [x] Pythonの`exit()`と`sys.exit()`と`os._exit()`
        - [Python の exit(), sys.exit(), os._exit() の違い](http://uchanote.blogspot.com/2015/01/python-exit-sysexit-osexit.html)
        - メインスレッドを止められればいいので，`sys.exit()`にした
- Chrome(ブラウザ)のタブ遷移の検出について
    - [ ] タブ遷移の検出にはページタイトルの相違によって行われている
        - もしページタイトルが全部同じWebサイトだったら遷移を検出できない可能性
        - ページタブごとのプロセスIDとか識別子はあるのか？
    - [x] URLの取得が難しそう
        - [アクティブタブとなったChromeのページURLを取得したい | teratail](https://teratail.com/questions/197377)に投げてあるが期待薄
        - タブバーのテキスト(上の項目にあるやつ．ページタイトル)で区別することに．
    - [x] Googleドライブからドキュメントを開くなど外部アプリに飛ぶ際に、`Chrome(無題)`と出る。
        - これはログに書き出す前に除去しよう
        - てゆかフィルタリングリストに書いとけばいいんじゃね？？
- [x] 仮想デスクトップ移動時の瞬間的なアクティブタブの検出について
    - 最低デルタt=1s未満ならLogに追加しない
    - というか勝手に検出してくれないから気にしなくても良さそう？
- [x] スリープさせたら止まっちゃう
    - 止まらなかった．スレッドループなら止まらないんだな．
- [ ] 文字を消しているときのBack Space**長押し**の検出ができない．
    - これは今はやらず，そのうち実装しよう
    - pynputモジュールの`on_press`と`on_release`間の時間の取得になるだろうな．
    - もしくは，マウスクリック期間・キーボードプレス期間というガントチャートを新たに追加するとか．
        - ガントチャートの短形内にクリックされているキー名を表示…できるのか？できたら理想的
- [ ] `set_interval`を大きくすると，mouseの冒頭でNoneが増えたり，active-tabで描写されないガントチャートが出てきたりする．
- `xaxis_type`で`at: active-start, mk: 5(number)`とすると…
    - [x] mouse/keyboardのx軸のラベルが縦向きにならない
        - matplotlibの描写順を変えただけでOK
    - [x] mouse/keyboardのx軸のラベルに`active-start`の時刻も追加されている
        - 変数dateのclearをしてOK
- [x] `pyinstaller`で`ipaexg.ttf`をどうにか吸わせられないかなぁ…
    - Plotter.pyでの`__file__`が問題そう．
    - `__file__`からの相対パスにして`config`フォルダを`modules`フォルダと同階層に置くことでとりま解決
- [x] たまに出る
    ```
    Traceback (most recent call last):
    File "app.py", line 77, in <module>
    File "app.py", line 40, in main
    File "modules\Alone.py", line 40, in run
    File "modules\Plotter.py", line 254, in run
    File "modules\Plotter.py", line 675, in get_mouse
    IndexError: list index out of range
    [11764] Failed to execute script app
    ```
    - アクティブタブの最終時刻がマウスよりあとにあることにより，マウスのログの最後のレコードまでwhileで回るようになってしまっていたので，while内に`raw_i+1 >= len(raw_data)`の条件分岐を`new_raw_data.append()`の直後に追加(マウスのログの最後のレコードの追加まで済ませさせるため？できてるのか？)することで解決．
    - これはキーボードでも同様．
- [x] exeにしたら出た．何これ？
    ```
    C:\Users\user_name\...\ganttlogger\modules\Plotter.py:308: UserWarning: Attempting to set identical left == right == 737254.0309270591 results in singular transformations; automatically expanding.
    C:\Users\user_name\...\ganttlogger\modules\Plotter.py:346: UserWarning: Attempting to set identical left == right == 737254.0309270591 results in singular transformations; automatically expanding.
    ```
    - たぶん開始早々に終了する時に，アクティブタブの最後のタイムスタンプのあとにマウスとキーボードのログが始まっているので，(マウスとキーボードの)加工できるデータが無いとエラーになっている．
    - この対応としてObserver.pyでアクティブタブのループを抜けた後に最後のログを挿入する．
- [ ] Macでたまに出る
    ```
    /usr/local/lib/python3.7/site-packages/matplotlib/backends/backend_agg.py:211: RuntimeWarning: Glyph 128266 missing from current font.
    font.set_text(s, 0.0, flags=flags)
    /usr/local/lib/python3.7/site-packages/matplotlib/backends/backend_agg.py:180: RuntimeWarning: Glyph 128266 missing from current font.
    font.set_text(s, 0, flags=flags)
    ```
    - Warningだから無視？フォントの問題か…
- [x] Windowsのパッケージインストール後に`win32gui`もインストールされているにも関わらず，以下のエラーが出る．
    ```
    ModuleNotFoundError: No module named 'win32gui'
    ```
    - ユーザに`pywin32`の再インストールを促す．
        ```
        > python -m pip uninstall pywin32 & python -m pip install pywin32
        ```