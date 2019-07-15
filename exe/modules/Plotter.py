'''
●ログファイルを読み込んでガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import os
import sys
import re
import datetime
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as pld
import matplotlib.font_manager as plf
# import plotly.offline as ploff
# import plotly.tools as pltl
# import plotly.graph_objs as plgo
# import plotly.figure_factory as plff
from modules.Public import StrFormatter

'''
References:
    http://ailaby.com/matplotlib_fig/#id4_1
    https://qiita.com/fujiy/items/f738aa9d0bb7427e07a4#%E8%A7%A3%E6%B1%BA%E7%AD%96
    https://www.haya-programming.com/entry/2018/05/26/031355
    https://note.nkmk.me/python-list-common/
    https://github.com/spyder-ide/spyder/issues/5401
    https://note.nkmk.me/python-check-int-float/
    https://pythondatascience.plavox.info/numpy/%E6%95%B0%E5%AD%A6%E7%B3%BB%E3%81%AE%E9%96%A2%E6%95%B0
    https://yukun.info/python-file/
    https://qiita.com/shibainurou/items/0b0f8b0233c45fc163cd
    https://note.nkmk.me/python-numpy-dtype-astype/
    https://www.javadrive.jp/python/list/index10.html#section3
    https://note.nkmk.me/python-datetime-timedelta-measure-time/
    https://stackoverflow.com/questions/31487732/simple-way-to-drop-milliseconds-from-python-datetime-datetime-object
    https://codeday.me/jp/qa/20181209/68124.html
'''

class Plotter:
    uuid = "" # If empty, this variable is unused
    dirname = ""
    sec_interval = 1 # The minimum interval is value is 1 second
    filter_tab_list = []
    hide_filtered_tab_duration = False
    filter_tab_durations = [] # ex. [[datetime.datetime(2017/01/01 12:53:23.525), datetime.datetime(2017/01/01 12:55:03.121)], [?,?], ...]
    select_data = ["all"]
    xaxis_type_at = "active-start"
    xaxis_type_mk = "10"
    strfmr = None
    '''
    ●List construction of plotting data
    plot_active_tab = np.array(
        # After getting variables other than FinishTime at a function 'get_activetab()',
        # we get FinishTime at a function 'more_reshape_activetab()'.
        [StartTime, ActiveName, TabText, FinishTime],
        ...,
        dtype=object
    )
    df_active_tab = dict{
        "ActiveName(TabText|Empty)": [
            (StartTime, Duration(=FinishTime-StartTime)), # type(StartTime)=datetime.datetime, type(Duration)=datetime.timedelta
            ...
        ],
        ...
    }

    plot_mouse = np.array(
        [CurrentTimeFollowingInterval, SumOfDistance|None], # type(CurrentTimeFollowingInterval)=str
        ...,
        dtype=object
    )
    plot_keyboard = np.array(
        [CurrentTimeFollowingInterval, SumOfCount|None], # type(CurrentTimeFollowingInterval)=str
        ...,
        dtype=object
    )
    '''
    plot_active_tab = np.array([["", "", ""]])
    plot_mouse = np.array([["", None]])
    plot_keyboard = np.array([["", None]])
    df_active_tab = {}
    def __init__(self, uuid=""):
        '''
        When arg "uuid" is empty, the mode is "plotter".
        -> Get data from current directory.
        When it is not empty, the mode is "alone" or "logger".
        -> Specify the output directory.
        '''
        self.strfmr = StrFormatter()
        if uuid:
            self.uuid = uuid
            self.dirname = "ganttlogger_logs/{}".format(uuid)
        else:
            # Get current directory
            self.dirname = os.getcwd()
        os.makedirs(os.path.dirname("{dirname}/graphs/".format(dirname=self.dirname)), exist_ok=True)
        self.sec_interval = 1
        self.filter_tab_list = []
        self.hide_filtered_tab_duration = False
        self.filter_tab_durations = []
        self.select_data = ["all"]
        self.xaxis_type_at = "active-start"
        self.xaxis_type_mk = "10"
        self.plot_active_tab = np.array([[None, "", ""]])
        self.plot_mouse = np.array([[None, None]])
        self.plot_keyboard = np.array([[None, None]])
        self.df_active_tab = {}

    def start(self):
        '''
        ●標準入力で
        (1)出力モードの選択(filter_tab/set_interval)
        (2)出力モードに合わせた必須項目への回答
        ・set_interval -> デルタtの数値指定(単位は秒)
        ・fiter_tab -> 不要なタブ名(ログからコピペ)をまとめたテキストファイルの指定
        ・select_data -> 3つのデータをサブプロットでまとめて出力するか，選択したデータで独立のプロットを出力するか(例えば，"all"なら1つの出力に3つのサブプロットが入っているが，一方3つのデータを選択した入力なら3つの出力が出る)
        ・xaxis_type -> 横軸の時刻目盛りを，アクティブタブ開始時刻にするか，等間隔(ユーザ指定[秒])にするか
        '''
        try:
            plot_types_labels = set(["set_interval", "filter_tab", "select_data", "xaxis_type"])
            plot_types_flags = {
                "set_interval": False,
                "filter_tab": False,
                "select_data": False,
                "xaxis_type": False
            }

            print(self.strfmr.get_colored_console_log("yellow",
                "===============[select plot types]==============="))
            print("""\
'set_interval': Set interval by seconds(Integer). Default is 1-second.
'filter_tab'  : Filter unnecessary tab texts in a text file before plotting.
'select_data' : Select whether you use all data to plot to an output or some data plot to each output. 
                Default - when you don't input in 'select_data' - is the former.
'xaxis_type'  : Select x-axis scale from whether 'active-start'(the start times of active tabs) or number
                of seconds interval.""")
            while True:
                print(self.strfmr.get_colored_console_log("yellow",
                    "Select plot types separated by ',',  or enter without input.: "), end="")
                plot_types = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                if not plot_types[0]:
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
                    continue
                xor_plot_types = set(plot_types) ^ plot_types_labels
                if len(xor_plot_types) == 0 or \
                    all(x in plot_types_labels for x in xor_plot_types):
                    break
                else:
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
            # Update flags following 'plot_types'
            for plot_type in plot_types:
                plot_types_flags[plot_type] = True
            # Get arguments from stdin following 'plot_types_flags'
            if plot_types_flags["set_interval"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[set_interval]-----------------"))
                print("There are a required setting.")
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Set the number of interval by seconds: "), end="")
                    st_input = input().strip()
                    # To avoid allowing the input with full-width digit, we don't use try-except(ValueError).
                    if re.compile(r'^[0-9]+$').match(st_input) and int(st_input) > 0:
                        self.sec_interval = int(st_input)
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval, input '2'."))
            if plot_types_flags["filter_tab"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[filter_tab]-----------------"))
                print("There are two required settings.")
                while True:
                    try:
                        print(self.strfmr.get_colored_console_log("yellow",
                        "(1)Input a file name written a list of tab text you want to filter.: "), end="")
                        filename = input().strip()
                        if not filename:
                            print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
                            continue
                        txtname = "{dirname}/{filename}".format(dirname=self.dirname, filename=filename)
                        with open(txtname, "r", encoding="utf-8") as f:
                            self.filter_tab_list = f.read().split("\n")
                            i_none = self.index_safety(self.filter_tab_list, "None")
                            if i_none != -1:
                                self.filter_tab_list[i_none] = None
                            break
                    except FileNotFoundError:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: File not found."))
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "(2)Do you want to hide mouse and keyboard graph depictions of the duration filtered regarding tab text?(Y/n) : "), end="")
                    st_input = input().strip()
                    if st_input == "Y":
                        self.hide_filtered_tab_duration = True
                        break
                    elif st_input == "n":
                        # self.hide_filtered_tab_duration = False
                        break
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input."))
            if plot_types_flags["select_data"]:
                select_data_labels = set(["active_tab", "mouse", "keyboard", "mouse-keyboard"])
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[select_data]-----------------"))
                print("There are a required setting.")
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Select 'all' or list separated by ',' from ('active_tab'|'mouse'|'keyboard'|'mouse-keyboard').: "), end="")
                    input_select_data = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                    if not input_select_data[0]:
                        # If empty input, no need to update self.select_data (keep "all")
                        break
                    elif "all" in input_select_data: 
                        if len(input_select_data) == 1:
                            # No need to update self.select_data
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: Too many select despite 'all'."))
                            continue
                    else:
                        xor_select_data = set(input_select_data) ^ select_data_labels
                        if len(xor_select_data) == 0 or \
                            all(x in select_data_labels for x in xor_select_data):
                            self.select_data = input_select_data
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: There are some invalid names of .log files."))
            if plot_types_flags["xaxis_type"]:
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[xaxis_type]-----------------"))
                print("There are two required settings.")
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Select x-axis type for ActiveTab from whether 'active-start' or number of the interval by seconds: "), end="")
                    st_input = input().strip()
                    if st_input == "active-start":
                        self.xaxis_type_at = st_input
                        break
                    # To avoid allowing the input with full-width digit, we don't use try-except(ValueError).
                    if re.compile(r'^[0-9]+$').match(st_input) and int(st_input) > 0:
                        self.xaxis_type_at = st_input
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval of the xaxis scale, input '2'.\nOr, input 'active-start' if you want set active start time to the xaxis scale."))
                        continue
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval of the xaxis scale, input '2'.\nOr, input 'active-start' if you want set active start time to the xaxis scale."))
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Select x-axis type for Mouse or Keyboard from whether 'active-start' or number of the interval by seconds: "), end="")
                    st_input = input().strip()
                    if st_input == "active-start":
                        self.xaxis_type_mk = st_input
                        break
                    # To avoid allowing the input with full-width digit, we don't use try-except(ValueError).
                    if re.compile(r'^[0-9]+$').match(st_input) and int(st_input) > 0:
                        self.xaxis_type_mk = st_input
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval of the xaxis scale, input '2'.\nOr, input 'active-start' if you want set active start time to the xaxis scale."))
                        continue
                    print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval of the xaxis scale, input '2'.\nOr, input 'active-start' if you want set active start time to the xaxis scale."))

            if self.select_data[0] == "all":
                self.run()
            else:
                self.run_each()
        except KeyboardInterrupt:
            print("Exit")
            sys.exit()

    def index_safety(self, l, target):
        try:
            return l.index(target)
        except ValueError:
            return -1

    def run(self): # plot(self)
        '''
        ●We must execute four functions in the following order.
        (1)self.get_activetab()
        (2)self.get_mouse() or self.get_keyboard()
        (3)self.more_reshape_activetab()

        References:
            http://pineplanter.moo.jp/non-it-salaryman/2018/03/23/python-2axis-graph/
            https://qiita.com/supersaiakujin/items/e2ee4019adefce08e381
            https://sabopy.com/py/matplotlib-26/
        '''
        print("Run, Plotter!")
        self.get_activetab()
        self.get_mouse()
        self.get_keyboard()
#         print("""
# =================================================
# ----------------[plot_active_tab]----------------
# {t}
# ----------------[mouse]----------------
# {m}
# ----------------[keyboard]----------------
# {k}
# """.format(t=self.plot_active_tab, m=self.plot_mouse, k=self.plot_keyboard))
#         # By force. It can't be hepled. Give me the better code.
        self.more_reshape_activetab()
#         print("""
# ----------------[plot_active_tab (after appending FinishTime)]----------------
# {t}
# ----------------[df_plot_active_tab]----------------
# {df}
# =================================================
# """.format(t=self.plot_active_tab, df=self.df_active_tab))

        '''
        こっから下は横方向の棒グラフの描写をしていく．matplotlib.dates.DateFormatter()やmatplotlib.dates.date2num()とかを使う．
        datetime.dates.date2numによるdatenumsとか無くてもいけるっぽい？？？念のためdate2numを使う場合もコメントアウトに残しとく．

        References:
            https://stackoverflow.com/questions/4090383/plotting-unix-timestamps-in-matplotlib
            https://stackoverflow.com/questions/40395227/minute-and-second-format-for-x-label-of-matplotlib
            https://triplepulu.blogspot.com/2013/06/pythonmatplotlib_285.html
            https://sabopy.com/py/matplotlib-26/
            http://www.jiajianhudong.com/question/382840.html
            ▲https://stackoverflow.com/questions/24425908/matplotlib-how-to-use-timestamps-with-broken-barh
            https://codeday.me/jp/qa/20190324/471800.html
            https://note.nkmk.me/python-datetime-usage/#datetime
            https://teratail.com/questions/74084
            http://naga-tsuzuki.sblo.jp/article/179645369.html#tick-y-
            https://qiita.com/Yoterph/items/e0039309a47c75dade05
            https://datumstudio.jp/blog/matplotlib%E3%81%AE%E6%97%A5%E6%9C%AC%E8%AA%9E%E6%96%87%E5%AD%97%E5%8C%96%E3%81%91%E3%82%92%E8%A7%A3%E6%B6%88%E3%81%99%E3%82%8Bwindows%E7%B7%A8
            https://qiita.com/canard0328/items/a859bffc9c9e11368f37
            http://bicycle1885.hatenablog.com/entry/2014/02/14/023734 (sharexによるx軸の共有がax1とax2の一致に使えるのでは？)
            http://ailaby.com/subplots_adjust/#id1
            http://nok0714.hatenablog.com/entry/2017/04/13/140525
            http://kuroneko0208.hatenablog.com/entry/2014/07/28/161453
            http://pineplanter.moo.jp/non-it-salaryman/2018/03/23/python-2axis-graph/
            https://qiita.com/supersaiakujin/items/e2ee4019adefce08e381
            http://nok0714.hatenablog.com/entry/2017/04/13/140525
        '''
        fig = plt.figure(figsize=(15, 9))
        # Get range of x axis
        init = self.plot_active_tab[0][0] # pld.date2num(self.plot_active_tab[0][0])
        last = self.plot_active_tab[len(self.plot_active_tab)-1][0] # pld.date2num(self.plot_active_tab[len(self.plot_active_tab)-1][0])

        # Create upper graph(ganttchart)
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_xlim(init, last) # Important for plotting ganttchart by seconds!
        dates = []
        if self.xaxis_type_at == "active-start":
            # activetabの開始時刻(と最終時刻)のみ
            dates = [t for t in self.plot_active_tab[:-1, 0]]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
        else:
            # ログの開始時刻から終了時刻までの等間隔秒刻み
            t = self.plot_active_tab[0][0]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            while (last_t - t).total_seconds() >= 0:
                dates.append(t)
                t += datetime.timedelta(seconds=int(self.xaxis_type_at))
            # print(last_t.second - dates[len(dates) - 1].second)
            # print(dates[len(dates) - 1].second - last_t.second)
        # 最後の日時を追加
        if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
            dates.append(last_t)
        # datenums = pld.date2num(dates)
        ax1.set_xticks(dates) # ax1.set_xticks(datenums)
        ax1.axes.tick_params(axis="x", labelsize=7, rotation=270)
        ax1.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
        fp = plf.FontProperties(fname="{}/../config/font/ipaexg.ttf".format(os.path.dirname(__file__)), size=8)
        y = [7.5 + i * 10 for i in range(len(self.df_active_tab.keys()))]
        y.append(y[len(y) - 1] + 10)
        ax1.set_yticks(y)
        ax1.set_yticklabels(self.df_active_tab.keys(), fontproperties=fp)
        for i, k in enumerate(self.df_active_tab.keys()): # 上のy軸方向の順(=self.df_active_tab.keys()の順)に従ってx軸方向のガントチャートを描写
            # print(self.df_active_tab[k])
            ax1.broken_barh(self.df_active_tab[k], (5+i*10, 5), facecolor="red")
        plt.subplots_adjust(top=0.85, bottom=0.15, right=0.95, hspace=0) # left=0.3, right=0.9
        plt.title("SwitchActiveTab(interval: {}s)".format(self.sec_interval))
        ax1.xaxis.tick_top() # 横軸をグラフの上に設置
        ax1.grid(axis="y") # 縦軸のグリッド線を引く
        

        # Create lower graph(line or bar graph)
        # ax2_1:mouse, ax2_2:keyboard
        ax2_1 = fig.add_subplot(2, 1, 2) # , sharex=ax1
        ax2_2 = ax2_1.twinx()
        ax2_1.set_xlim(init, last)
        dates.clear()
        if self.xaxis_type_mk == "active-start":
            # activetabの開始時刻(と最終時刻)のみ
            dates = [t for t in self.plot_active_tab[:-1, 0]]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
        else:
            # ログの開始時刻から終了時刻までの等間隔秒刻み
            t = self.plot_active_tab[0][0]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            while (last_t - t).total_seconds() >= 0:
                dates.append(t)
                t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
        # 最後の日時を追加
        if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
            dates.append(last_t)
        # datenums = pld.date2num(dates)
        ax2_1.plot(self.plot_mouse[:, 0], self.plot_mouse[:, 1], color="orange", label="mouse-distance")
        ax2_2.plot(self.plot_keyboard[:, 0], self.plot_keyboard[:, 1], color="skyblue", label="keyboard-count")
        ax2_1.legend(bbox_to_anchor=(0.6, -0.1), loc='upper left', borderaxespad=0.5, fontsize=10)
        ax2_2.legend(bbox_to_anchor=(0.8, -0.1), loc='upper left', borderaxespad=0.5, fontsize=10)
        plt.xlabel("t")
        ax2_1.set_xticks(dates) # ax2_1.set_xticks(datenums)
        ax2_1.axes.tick_params(axis="x", labelsize=7, rotation=270)
        ax2_1.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S"))
        ax2_1.set_ylabel("Mouse Distance[/interval]")
        ax2_2.set_ylabel("Keyboard Count[/interval]")
        ax2_2.grid(axis="y")
        ax2_1.set_ylim(bottom=0)
        ax2_2.set_ylim(bottom=0)

        # Save and Show
        filetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open("{dirname}/graphs/output_{datetime}_all.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
            pickle.dump(fig, f)
        plt.savefig("{dirname}/graphs/output_{datetime}_all".format(dirname=self.dirname, datetime=filetime))
        # plt.show()


    def run_each(self): # plot_each(self)
        '''
        ●run()が3つのサブプロットで1つのファイル出力をするのに対し，run_each()は
        1つのプロットで1つのファイル出力をする，つまり独立した出力をする関数．
        ●self.select_dataに従って，get_activetab，get_mouse，get_keyboardのいずれかを実行して各々の独立ファイルを出力．
        ●各出力ファイル名に日時を追加する．
        
        ●We must execute four functions in the following order.
        (1)self.get_activetab()
        (2)self.get_mouse() or self.get_keyboard()
        (3)self.more_reshape_activetab()
        '''
        print("Run, Plotter-Each!")
        self.get_activetab()
        self.get_mouse()
        self.get_keyboard()
        self.more_reshape_activetab()

        filetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        init = self.plot_active_tab[0][0] # pld.date2num(self.plot_active_tab[0][0])
        last = self.plot_active_tab[len(self.plot_active_tab)-1][0] # pld.date2num(self.plot_active_tab[len(self.plot_active_tab)-1][0])
        
        # if active_tabの出力が選択されていたら
        if "active_tab" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            if self.xaxis_type_at == "active-start":
                # activetabの開始時刻(と最終時刻)のみ
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                # ログの開始時刻から終了時刻までの等間隔秒刻み
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_at))
            # 最後の日時を追加
            if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
                dates.append(last_t)
            # datenums = pld.date2num(dates)
            ax.set_xticks(dates) # ax.set_xticks(datenums)
            plt.xlabel("t")
            ax.axes.tick_params(axis="x", labelsize=7, rotation=270) # rotation=25
            ax.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
            fp = plf.FontProperties(fname="{}/../config/font/ipaexg.ttf".format(os.path.dirname(__file__)), size=8)
            y = [7.5 + i * 10 for i in range(len(self.df_active_tab.keys()))]
            y.append(y[len(y) - 1] + 10)
            ax.set_yticks(y)
            ax.set_yticklabels(self.df_active_tab.keys(), fontproperties=fp)
            for i, k in enumerate(self.df_active_tab.keys()): # 上のy軸方向の順(=self.df_active_tab.keys()の順)に従ってx軸方向のガントチャートを描写
                # print(self.df_active_tab[k])
                ax.broken_barh(self.df_active_tab[k], (5+i*10, 5), facecolor="red")
            plt.title("SwitchActiveTab(interval: {}s)".format(self.sec_interval))
            ax.grid(axis="y") # 縦軸のグリッド線を引く
            plt.subplots_adjust(top=0.95, bottom=0.2, right=0.99, left=0.2)
            with open("{dirname}/graphs/output_{datetime}_active_tab.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_active_tab".format(dirname=self.dirname, datetime=filetime))
        
        # if mouseの出力が選択されていたら
        if "mouse" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_mk == "active-start":
                # activetabの開始時刻(と最終時刻)のみ
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                # ログの開始時刻から終了時刻までの等間隔秒刻み
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # 最後の日時を追加
            if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
                dates.append(last_t)
            # datenums = pld.date2num(dates)
            ax.plot(self.plot_mouse[:, 0], self.plot_mouse[:, 1], color="orange", label="mouse-distance")
            plt.xlabel("t")
            ax.set_xticks(dates) # ax.set_xticks(datenums)
            ax.axes.tick_params(axis="x", labelsize=7, rotation=270)
            ax.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
            plt.subplots_adjust(top=0.95, bottom=0.23)
            ax.set_ylabel("Mouse Distance[/interval]")
            ax.set_ylim(bottom=0)
            ax.set_ylim(bottom=0)
            plt.title("Mouse Distance(interval: {}s)".format(self.sec_interval))
            with open("{dirname}/graphs/output_{datetime}_mouse.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_mouse".format(dirname=self.dirname, datetime=filetime))
        
        # if keyboardの出力が選択されていたら
        if "keyboard" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_mk == "active-start":
                # activetabの開始時刻(と最終時刻)のみ
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                # ログの開始時刻から終了時刻までの等間隔秒刻み
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # 最後の日時を追加
            if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
                dates.append(last_t)
            # datenums = pld.date2num(dates)
            ax.plot(self.plot_keyboard[:, 0], self.plot_keyboard[:, 1], color="skyblue", label="keyboard-count")
            plt.xlabel("t")
            ax.set_xticks(dates) # ax.set_xticks(datenums)
            ax.axes.tick_params(axis="x", labelsize=7, rotation=270)
            ax.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
            plt.subplots_adjust(top=0.95, bottom=0.23)
            ax.set_ylabel("Keyboard Count[/interval]")
            ax.set_ylim(bottom=0)
            ax.set_ylim(bottom=0)
            ax.grid(axis="y")
            plt.title("Keyboard Count(interval: {}s)".format(self.sec_interval))
            with open("{dirname}/graphs/output_{datetime}_keyboard.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_keyboard".format(dirname=self.dirname, datetime=filetime))

        if "mouse-keyboard" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax2 = ax.twinx()
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_mk == "active-start":
                # activetabの開始時刻(と最終時刻)のみ
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                # ログの開始時刻から終了時刻までの等間隔秒刻み
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # 最後の日時を追加
            if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
                dates.append(last_t)
            # datenums = pld.date2num(dates)
            ax.plot(self.plot_mouse[:, 0], self.plot_mouse[:, 1], color="orange", label="mouse-distance")
            ax2.plot(self.plot_keyboard[:, 0], self.plot_keyboard[:, 1], color="skyblue", label="keyboard-count")
            ax.legend(bbox_to_anchor=(0.6, -0.2), loc='upper left', borderaxespad=0.5, fontsize=10)
            ax2.legend(bbox_to_anchor=(0.8, -0.2), loc='upper left', borderaxespad=0.5, fontsize=10)
            plt.xlabel("t")
            ax.set_xticks(dates) # ax.set_xticks(datenums)
            ax.axes.tick_params(axis="x", labelsize=7, rotation=270)
            ax.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
            ax.set_ylabel("Mouse Distance[/interval]")
            ax2.set_ylabel("Keyboard Count[/interval]")
            ax.set_ylim(bottom=0)
            ax.set_ylim(bottom=0)
            ax2.grid(axis="y")
            plt.title("Mouse and Keyboard(interval: {}s)".format(self.sec_interval))
            plt.subplots_adjust(top=0.95, bottom=0.25)
            with open("{dirname}/graphs/output_{datetime}_mouse-keyboard.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_mouse-keyboard".format(dirname=self.dirname, datetime=filetime))


    def get_activetab(self):
        '''
        ファイル読み込み・データ加工をここで行い，縦軸と横軸のリストを返す
        
        References:
            http://oimokihujin.hatenablog.com/entry/2015/10/01/112450
            https://deepage.net/features/numpy-empty.html
            https://note.nkmk.me/python-numpy-delete/
        '''
        try:
            with open("{dirname}/active_tab.log".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "StartTime" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split("]:+:[")) != 3:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split("]:+:[")
                    if len(splitted_column) != 3:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'active_tab.log'"))
                        sys.exit()
                    if not splitted_column[2]:
                        splitted_column[2] = None # If np.nan, its type will change str, so set None
                    # Here, change type of timestamp(str -> datetime.datetime)
                    raw_data.append([datetime.datetime.strptime(splitted_column[0], "%Y/%m/%d %H:%M:%S.%f"), splitted_column[1], splitted_column[2]])
            # print("before: {}".format(raw_data))
            # print(np.array(raw_data)[:,2])

            if len(self.filter_tab_list) > 0:
                del_indexs = []
                # Get duration of filtered tab text before filtering
                for i in range(1, len(raw_data) - 1): # We don't filter the first and last row not to break the timing of timestamps
                    if raw_data[i][2] in self.filter_tab_list:
                        '''
                        ###############################################################
                        Because we don't need '.%f' in filtering at mouse and keyboard, split by '.' and remove '.%f'.
                        But maybe we should calculate in milliseconds...
                        ###############################################################
                        '''
                        self.filter_tab_durations.append([raw_data[i][0].replace(microsecond=0), raw_data[i+1][0].replace(microsecond=0)])
                        del_indexs.append(i)
                # Filter tab text
                '''
                ###############################################################
                This code below maybe bad.
                Delete columns during loop, length of array changes...
                ###############################################################
                '''
                gap_i = 0
                for del_i in del_indexs:
                    raw_data = np.delete(raw_data, del_i - gap_i, axis=0)
                    gap_i += 1
            # print("after: {}".format(raw_data))

            self.plot_active_tab = np.array(raw_data, dtype=object)
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'active_tab.log' not found."))
            sys.exit()
    
    def more_reshape_activetab(self):
        '''
        マウス・キーボードのデータを取得した後でのアクティブタブのデータの加工．
        こんなコード構成は不本意だがゴリゴリやる．

        ここでスリープ期間の(マウス・キーボードの両方がNoneという前提での)削ぎ落としと，self.df_active_tabを得る
        '''
        new_data = self.plot_active_tab.tolist()
        m_i, k_i = 0, 0
        for i in range(len(self.plot_active_tab) - 1):
            '''
            ●各レコードにFinishTimeを第3インデックスとして追加していく．
            ●もしマウス・キーボードが両方Noneでなければ，次のレコードのStartTimeをFinishTimeに格納する
            ●もし両方NoneならそのレコードのFinishTimeにマウス・キーボードのいずれかの値がある方のタイムスタンプを格納する

            ●(self.plot_active_tab[0][0]を初期タイムスタンプとして，)そのレコードのStartTime～その次のレコードのStartTimeの間をself.sec_interval(良くなかったら1秒間隔)で調べた時に，マウス・キーボードの両方がNoneになったら，その直前の時刻をそのレコードのFinishTimeにする．
            '''
            current_time = self.plot_active_tab[i][0].replace(microsecond=0)
            next_tab_start = self.plot_active_tab[i+1][0]
            exist_both_None = False
            while (next_tab_start - current_time).total_seconds() > 0:
                for j in range(m_i, len(self.plot_mouse) - 1):
                    if self.plot_mouse[j][0] == current_time:
                        m_i = j
                        break
                for j in range(k_i, len(self.plot_keyboard) - 1):
                    if self.plot_keyboard[j][0] == current_time:
                        k_i = j
                        break
                if (self.plot_mouse[m_i][1] is None) and (self.plot_keyboard[k_i][1] is None):
                    exist_both_None = True
                    break
                current_time += datetime.timedelta(seconds=1) # self.sec_interval
            if not exist_both_None:
                new_data[i].append(self.plot_active_tab[i+1][0])
            else:
                '''
                ###############################################################
                If lists of mouse and keyboard have timestamps with microseconds, the code below will work well.
                But the lists have timestamps without microseconds because of being removed at functions 'get_mouse()' and
                'get_keyboard()'.
                So we set the first 'both None' timestamp between StartTimes of two consecutive tab data as FinishTime here.
                ###############################################################
                '''
                # finish_m_i, finish_k_i = m_i, k_i
                # while self.plot_mouse[finish_m_i][1] is None:
                #     finish_m_i -= 1
                # while self.plot_keyboard[finish_k_i][1] is None:
                #     finish_k_i -= 1
                # m_time = self.plot_mouse[finish_m_i][0]
                # k_time = self.plot_keyboard[finish_k_i][0]
                # if (m_time - k_time).total_seconds() > 0:
                #     finish = m_time
                # else:
                #     finish = k_time
                # self.plot_active_tab[i].append(finish)
                new_data[i].append(current_time)
        # The appending (third) index 'FinishTime' of the last record is the 'StartTime' of itself.
        new_data[len(self.plot_active_tab)-1].append(self.plot_active_tab[len(self.plot_active_tab)-1][0])
        self.plot_active_tab = np.array(new_data, dtype=object)
        # print(self.plot_active_tab)

        # Create dataframe 'self.df_active_tab' groupby 'ActiveName(TabText)'
        for i in range(len(self.plot_active_tab) - 1):
            name = self.plot_active_tab[i][1]
            if self.plot_active_tab[i][2]:
                name += "({})".format(self.plot_active_tab[i][2])
            start = self.plot_active_tab[i][0]
            finish = self.plot_active_tab[i][3] # self.plot_active_tab[i+1][0]
            if name in self.df_active_tab.keys():
                self.df_active_tab[name].append((start, finish - start))
                # self.df_active_tab[name].append((pld.date2num(start), pld.date2num(finish) - pld.date2num(start)))
            else:
                self.df_active_tab[name] = [(start, finish - start)]
                # self.df_active_tab[name] = [(pld.date2num(start), pld.date2num(finish) - pld.date2num(start))]
        # print(self.df_active_tab)
    
    def get_mouse(self):
        '''
        ●(完)activetabで最後に終了タイムスタンプをしているけど，それより後の分もkeyboardとmouseはログが残っているので，除去すべきかも？
        したがって，開始時刻・終了時刻はactivetabのself.plot_active_tabの0番目と最後の時刻に基づく．
        ●(完)self.hide_filtered_tab_duration=Trueの場合に，self.filter_tab_durationsに従ってNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
        ●None埋めとかにして，グラフプロット前にデータをNone期間で分割していってそれぞれでグラフプロットして後から重ねていくとか？
        http://natsutan.hatenablog.com/entry/20110713/1310513258
        というか普通に同じとこに，同じ色でプロットしていけばよくね？でも空白期間の表現できるのかな？
        ●np.nan埋めでいけるっぽい？
        https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/nan_test.html
        ●それともget_activetab()で除去した部分のマークをしないようにNone埋めする？
        https://stackoverflow.com/questions/14399689/matplotlib-drawing-lines-between-points-ignoring-missing-data
        ●その他よくわからんけど参考になりそうな…
        https://codeday.me/jp/qa/20190318/374532.html
        ●plotlyを使う場合，np.nanではなくNoneでいけそう
        '''
        try:
            with open("{dirname}/mouse.log".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "Time" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split("]:+:[")) != 2:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split("]:+:[")
                    if len(splitted_column) != 2:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'mouse.log'"))
                        sys.exit()
                    # Digit check (If error, catch ValueError)
                    splitted_column[1] = float(splitted_column[1])
                    # Here, don't change type of timestamp(str)
                    raw_data.append(splitted_column)
            # print("before: {}".format(raw_data))
            # raw_data = [[str(h:m:s.ms), str]]

            # [1st] Reshape raw_data to 1-second interval data (and fill in the blanks with None)
            # Get initial timestamp from self.plot_active_tab
            # Use as 1-second interval timestamp 
            current_time = self.plot_active_tab[0][0].replace(microsecond=0)
            '''
            # This code below is fixing current_time because the timestamp of mouse is earlier than the one of active_tab.
            # But there is also keyboard, so we should define the first timestamp of active_tab is the fastest log. (And the last timestamp of active_tab is the last log of active_tab, mouse, and keyboard)
            current_time = self.plot_active_tab[0][0]
            if (current_time - datetime.datetime.strptime(raw_data[0][0], "%Y/%m/%d %H:%M:%S.%f")).total_seconds() > 0:
                for mouse_i in range(1, len(raw_data)):
                    mouse_time = datetime.datetime.strptime(raw_data[mouse_i][0], "%Y/%m/%d %H:%M:%S.%f")
                    if (current_time - mouse_time).total_seconds() < 0:
                        break
                current_time = mouse_time
            '''
            # Get final timestamp from self.plot_active_tab
            # This final timestamp is also used in [3rd]
            final_time = self.plot_active_tab[len(self.plot_active_tab)-1][0].replace(microsecond=0)
            new_raw_data = []
            raw_i = 0
            while (final_time - current_time).total_seconds() >= 0: # 秒までの時刻で比較
                # 文字列の時刻に変換するときはマイクロ秒は含めない
                str_current_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
                if str_current_time in raw_data[raw_i][0]: # 秒までの時刻で文字列比較する方が良い
                    # タイムスタンプでもマイクロ秒は含めない
                    new_raw_data.append([current_time, raw_data[raw_i][1]])
                    if raw_i + 1 >= len(raw_data):
                        break
                    if str_current_time in raw_data[raw_i+1][0]: # 秒までの時刻で文字列比較する方が良い
                        # Rarely, the same seconds duplicates in consecutive two timestamps
                        # print("Duplicated!!!: " + str_current_time)
                        new_raw_data[len(new_raw_data)-1][1] += raw_data[raw_i+1][1]
                        raw_i += 1
                    raw_i += 1
                else:
                    # タイムスタンプでもマイクロ秒は含めない
                    new_raw_data.append([current_time, None])
                current_time += datetime.timedelta(seconds=1)
            raw_data = new_raw_data
            # raw_data = [[datetime.datetime(h:m:s), int|None]]
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            # [2nd]If self.hide_filtered_tab_duration=True, replace value to None in the duration of filtered tab
            if self.hide_filtered_tab_duration:
                durations_i = 0
                # filter_start = self.filter_tab_durations[durations_i][0]
                # filter_end = self.filter_tab_durations[durations_i][1]
                for i in range(len(raw_data) - 1): # Don't filter because the last row has the time logging finished (But the first can be filtered)
                    '''
                    ###############################################################
                    Because we removed '.%f' at [1st], we calculate in seconds.
                    But maybe we should calculate in milliseconds...
                    ###############################################################
                    '''
                    if (self.filter_tab_durations[durations_i][1] - raw_data[i][0]).total_seconds() < 0:
                        durations_i += 1
                    if durations_i == len(self.filter_tab_durations):
                        break

                    after_filter_start = (self.filter_tab_durations[durations_i][0] - raw_data[i][0]).total_seconds() <= 0
                    before_filter_end = (self.filter_tab_durations[durations_i][1] - raw_data[i][0]).total_seconds() > 0 # Don't add timestamp of next tab
                    if after_filter_start and before_filter_end:
                        raw_data[i][1] = None
            # print(np.array(raw_data))
            # raw_data = [[datetime.datetime(h:m:s), int|None]]
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # [3rd] If user setted set_interval, reshape data following the user-setted interval
            if self.sec_interval > 1:
                current_time = raw_data[0][0]
                new_raw_data = [raw_data[0]]
                raw_i = 1
                while raw_i < len(raw_data):
                    current_time += datetime.timedelta(seconds=self.sec_interval)
                    raw_time = raw_data[raw_i][0]
                    sum_interval = None
                    while (current_time - raw_time).total_seconds() >= 0:
                        if sum_interval is not None:
                            if raw_data[raw_i][1] is not None:
                                sum_interval += raw_data[raw_i][1]
                        else:
                            if raw_data[raw_i][1] is not None:
                                sum_interval = raw_data[raw_i][1]
                        raw_i += 1
                        if raw_i == len(raw_data):
                            break
                        raw_time = raw_data[raw_i][0]
                    if (current_time - final_time).total_seconds() > 0:
                        # If current_time added by final interval is larger than 
                        # final_time(final timestamp of active_tab), replace the 
                        # value of current_time to the value of final_time.
                        current_time = final_time
                    new_raw_data.append([current_time, sum_interval])
                raw_data = new_raw_data
            # print(np.array(raw_data))
            # raw_data = [[datetime.datetime(h:m:s), int|None]]

            self.plot_mouse = np.array(raw_data, dtype=object)
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'mouse.log' not found."))
            sys.exit()
        except ValueError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid record in 'mouse.log'."))
            sys.exit()

    def get_keyboard(self):
        '''
        ●(完)activetabで最後に終了タイムスタンプをしているけど，それより後の分もkeyboardとmouseはログが残っているので，除去すべきかも？
        したがって，開始時刻・終了時刻はactivetabのself.plot_active_tabの0番目と最後の時刻に基づく．
        ●(完)self.hide_filtered_tab_duration=Trueの場合に，self.filter_tab_durationsに従ってNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
        ●None埋めとかにして，グラフプロット前にデータをNone期間で分割していってそれぞれでグラフプロットして後から重ねていくとか？
        http://natsutan.hatenablog.com/entry/20110713/1310513258
        というか普通に同じとこに，同じ色でプロットしていけばよくね？でも空白期間の表現できるのかな？
        ●np.nan埋めでいけるっぽい？
        https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/nan_test.html
        ●それともget_activetab()で除去した部分のマークをしないようにNone埋めする？
        https://stackoverflow.com/questions/14399689/matplotlib-drawing-lines-between-points-ignoring-missing-data
        ●その他よくわからんけど参考になりそうな…
        https://codeday.me/jp/qa/20190318/374532.html
        ●plotlyを使う場合，np.nanではなくNoneでいけそう
        '''
        try:
            with open("{dirname}/keyboard.log".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "Time" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split("]:+:[")) != 2:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split("]:+:[")
                    if len(splitted_column) != 2:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'keyboard.log'"))
                        sys.exit()
                    # Digit check (If error, catch ValueError)
                    splitted_column[1] = int(splitted_column[1])
                    # Here, don't change type of timestamp(str)
                    raw_data.append(splitted_column)
            # print("before: {}".format(raw_data))
            # raw_data = [[str(h:m:s.ms), str]]

            # [1st] Reshape raw_data to 1-second interval data (and fill in the blanks with None)
            # Get initial timestamp from self.plot_active_tab
            # Use as 1-second interval timestamp 
            current_time = self.plot_active_tab[0][0].replace(microsecond=0)
            '''
            # This code below is fixing current_time because the timestamp of mouse is earlier than the one of active_tab.
            # But there is also keyboard, so we should define the first timestamp of active_tab is the fastest log. (And the last timestamp of active_tab is the last log of active_tab, mouse, and keyboard)
            current_time = self.plot_active_tab[0][0]
            if (current_time - datetime.datetime.strptime(raw_data[0][0], "%Y/%m/%d %H:%M:%S.%f")).total_seconds() > 0:
                for mouse_i in range(1, len(raw_data)):
                    mouse_time = datetime.datetime.strptime(raw_data[mouse_i][0], "%Y/%m/%d %H:%M:%S.%f")
                    if (current_time - mouse_time).total_seconds() < 0:
                        break
                current_time = mouse_time
            '''
            # Get final timestamp from self.plot_active_tab
            # This final timestamp is also used in [3rd]
            final_time = self.plot_active_tab[len(self.plot_active_tab)-1][0].replace(microsecond=0)
            new_raw_data = []
            raw_i = 0
            while (final_time - current_time).total_seconds() >= 0: # 秒までの時刻で比較
                str_current_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
                if str_current_time in raw_data[raw_i][0]: # 秒までの時刻で文字列比較する方が良い
                    # タイムスタンプでもマイクロ秒は含めない
                    new_raw_data.append([current_time, raw_data[raw_i][1]])
                    if raw_i + 1 >= len(raw_data):
                        break
                    if str_current_time in raw_data[raw_i+1][0]: # 秒までの時刻で文字列比較する方が良い
                        # Rarely, the same seconds duplicates in consecutive two timestamps
                        # print("Duplicated!!!: " + str_current_time)
                        new_raw_data[len(new_raw_data)-1][1] += raw_data[raw_i+1][1]
                        raw_i += 1
                    raw_i += 1
                else:
                    # タイムスタンプでもマイクロ秒は含めない
                    new_raw_data.append([current_time, None])
                current_time += datetime.timedelta(seconds=1)
            raw_data = new_raw_data
            # print(np.array(raw_data))
            # raw_data = [[datetime.datetime(h:m:s), int|None]]
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            # [2nd]If self.hide_filtered_tab_duration=True, replace value to None in the duration of filtered tab
            if self.hide_filtered_tab_duration:
                durations_i = 0
                # filter_start = self.filter_tab_durations[durations_i][0]
                # filter_end = self.filter_tab_durations[durations_i][1]
                for i in range(len(raw_data) - 1): # Don't filter because the last row has the time logging finished (But the first can be filtered)
                    '''
                    ###############################################################
                    Because we removed '.%f' at [1st], we calculate in seconds.
                    But maybe we should calculate in milliseconds...
                    ###############################################################
                    '''
                    if (self.filter_tab_durations[durations_i][1] - raw_data[i][0]).total_seconds() < 0:
                        durations_i += 1
                    if durations_i == len(self.filter_tab_durations):
                        break

                    after_filter_start = (self.filter_tab_durations[durations_i][0] - raw_data[i][0]).total_seconds() <= 0
                    before_filter_end = (self.filter_tab_durations[durations_i][1] - raw_data[i][0]).total_seconds() > 0 # Don't add timestamp of next tab
                    if after_filter_start and before_filter_end:
                        raw_data[i][1] = None
            # print(np.array(raw_data))
            # raw_data = [[datetime.datetime(h:m:s), int|None]]
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # [3rd] If user setted set_interval, reshape data following the user-setted interval
            if self.sec_interval > 1:
                current_time = raw_data[0][0]
                new_raw_data = [raw_data[0]]
                raw_i = 1
                while raw_i < len(raw_data):
                    current_time += datetime.timedelta(seconds=self.sec_interval)
                    raw_time = raw_data[raw_i][0]
                    sum_interval = None
                    while (current_time - raw_time).total_seconds() >= 0:
                        if sum_interval is not None:
                            if raw_data[raw_i][1] is not None:
                                sum_interval += raw_data[raw_i][1]
                        else:
                            if raw_data[raw_i][1] is not None:
                                sum_interval = raw_data[raw_i][1]
                        raw_i += 1
                        if raw_i == len(raw_data):
                            break
                        raw_time = raw_data[raw_i][0]
                    if (current_time - final_time).total_seconds() > 0:
                        # If current_time added by final interval is larger than 
                        # final_time(final timestamp of active_tab), replace the 
                        # value of current_time to the value of final_time.
                        current_time = final_time
                    new_raw_data.append([current_time, sum_interval])
                raw_data = new_raw_data
            # print(np.array(raw_data))
            # raw_data = [[datetime.datetime(h:m:s), int|None]]

            self.plot_keyboard = np.array(raw_data, dtype=object)
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'keyboard.log' not found."))
            sys.exit()
        except ValueError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid record in 'keyboard.log'."))
            sys.exit()
    