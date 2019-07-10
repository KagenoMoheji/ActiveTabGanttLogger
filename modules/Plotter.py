'''
●ログファイルを読み込んでガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import os
import re
import datetime
import numpy as np
# import matplotlib.pyplot as plt
import plotly.offline as ploff
import plotly.graph_objs as plgo
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
'''

class Plotter:
    uuid = "" # If empty, this variable is unused
    dirname = ""
    sec_interval = 1 # The minimum interval is value is 1 second
    filter_tab_list = []
    hide_filtered_tab_duration = False
    filter_tab_durations = [] # ex. [["2017/01/01 12:53:23.525", "2017/01/01 12:55:03.121"], [?,?], ...]
    select_data = ["all"]
    strfmr = None
    '''
    ●List construction of plotting data
    plot_active_tab = np.array(
        [StartTime, Active(App)Name, TabText],
        ...
    )
    plot_mouse = np.array(
        [CurrentTimeFollowingInterval, SumOfDistance|None],
        ...
    )
    plot_keyboard = np.array(
        [CurrentTimeFollowingInterval, SumOfCount|None],
        ...
    )
    '''
    plot_active_tab = np.array([["", "", ""]])
    plot_mouse = np.array([["", None]])
    plot_keyboard = np.array([["", None]])
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
            self.dirname = os.getcwd()
        print(self.dirname)
        self.sec_interval = 1
        self.filter_tab_list = []
        self.hide_filtered_tab_duration = False
        self.filter_tab_durations = []
        self.select_data = ["all"]
        self.plot_active_tab = np.array([["", "", ""]])
        self.plot_mouse = np.array([["", None]])
        self.plot_keyboard = np.array([["", None]])

    def start(self):
        '''
        ●標準入力で
        (1)出力モードの選択(filter_tab/set_interval)
        (2)出力モードに合わせた必須項目への回答
        ・set_interval -> デルタtの数値指定(単位は秒)
        ・fiter_tab -> 不要なタブ名(ログからコピペ)をまとめたテキストファイルの指定
        ・select_data -> 3つのデータをサブプロットでまとめて出力するか，選択したデータで独立のプロットを出力するか(例えば，"all"なら1つの出力に3つのサブプロットが入っているが，一方3つのデータを選択した入力なら3つの出力が出る)
        '''
        try:
            plot_types_labels = set(["set_interval", "filter_tab", "select_data"])
            plot_types_flags = {
                "set_interval": False,
                "filter_tab": False,
                "select_data": False
            }

            print(self.strfmr.get_colored_console_log("yellow",
                "===============[select plot types]==============="))
            print("""\
'set_interval': Set interval by seconds(Integer). Default is 1-second.
'filter_tab'  : Filter unnecessary tab texts in a text file before plotting.
'select_data' : Select whether you use all data to plot to an output or some data plot to each output. 
                Default - when you don't input in 'select_data' - is the former.''""")
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
                    self.sec_interval = input().strip()
                    # To avoid allowing the input with full-width digit, we don't use try-except(ValueError).
                    if re.compile(r'^[0-9]+$').match(self.sec_interval) and int(self.sec_interval) > 0:
                        self.sec_interval = int(self.sec_interval)
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
                        txtname = "{dirname}/{filename}".format(dirname=self.dirname, filename=input().strip())
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
                print(self.strfmr.get_colored_console_log("yellow",
                    "-----------------[select_data]-----------------"))
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "Select 'all' or list separated by ',' with some csv file names like 'active_tab'.: "), end="")
                    print("There are a required setting.")
                    input_select_data = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                    if not input_select_data[0]:
                        # No need to update self.select_data
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
                        select_data_labels = set(["active_tab", "mouse", "keyboard"])
                        xor_select_data = set(input_select_data) ^ select_data_labels
                        if len(xor_select_data) == 0 or \
                            all(x in select_data_labels for x in xor_select_data):
                            self.select_data = input_select_data
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: There are some Invalid names of csv files."))

#             print("""\
# sec_interval: {0}
# filter_tab_list: {1}
# select_data: {2}""".format(self.sec_interval, self.filter_tab_list, self.select_data))
            if self.select_data[0] == "all":
                self.run()
            else:
                self.run_each()
        except KeyboardInterrupt:
            print("Exit")
            exit()

    def index_safety(self, l, target):
        try:
            return l.index(target)
        except ValueError:
            return -1

    def run(self): # plot(self)
        '''
        ●get_activetab，get_mouse，get_keyboardの全部を行う．
        ●plotで3つのサブプロットを用意するとして，どうやってサブプロットを
        上記3つの関数に渡すのか？？？？
        ●上記3つの関数でファイル読み込み・データ加工したリストを用意して，ここで
        サブプロットにプロット？

        ●plotlyとmatplotlibの両方で実装！！(plotlyでのネット不通に備えて)

        References:
            http://pineplanter.moo.jp/non-it-salaryman/2018/03/23/python-2axis-graph/
            https://qiita.com/supersaiakujin/items/e2ee4019adefce08e381
        '''
        print("Run, Plotter!")
        self.get_activetab()
#         print("""\
# hide_filtered_tab_duration: {0}
# filter_tab_durations: {1}""".format(self.hide_filtered_tab_duration, self.filter_tab_durations))
        self.get_mouse()
        # self.get_keyboard()
        print("""
=================================================
----------------[plot_active_tab]----------------
{t}
----------------[moouse]----------------
----------------[keyboard]----------------
=================================================
""".format(t=self.plot_active_tab)) # , m=self.plot_mouse, k=self.plot_keyboard

    def run_each(self): # plot_each(self)
        '''
        ●run()が3つのサブプロットで1つのファイル出力をするのに対し，run_each()は
        1つのプロットで1つのファイル出力をする，つまり独立した出力をする関数．
        ●self.select_dataに従って，get_activetab，get_mouse，get_keyboardのいずれかを実行して各々の独立ファイルを出力．
        ●各出力ファイル名に日時を追加する．
        
        ●We must implement get_activetab() ahead.
        '''
        print("Run, Plotter-Each!")

    def get_activetab(self):
        '''
        ファイル読み込み・データ加工をここで行い，縦軸と横軸のリストを返す
        
        References:
            http://oimokihujin.hatenablog.com/entry/2015/10/01/112450
            https://deepage.net/features/numpy-empty.html
            https://note.nkmk.me/python-numpy-delete/
        '''
        try:
            with open("{dirname}/active_tab.csv".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "StartTime" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split(",")) != 3:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split(",")
                    if len(splitted_column) != 3:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'active_tab.csv'"))
                        exit()
                    if not splitted_column[2]:
                        splitted_column[2] = None # If np.nan, its type will change str, so set None
                    raw_data.append(splitted_column)
                raw_data = np.array(raw_data)
            # print("before: {}".format(raw_data))
            # print(raw_data[:,2])

            if len(self.filter_tab_list) > 0:
                del_indexs = []
                # Get duration of filtered tab text before filtering
                for i in range(len(raw_data) - 1): # The last row has the time logging finished
                    if raw_data[i][2] in self.filter_tab_list:
                        self.filter_tab_durations.append([raw_data[i][0], raw_data[i+1][0]])
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
            
            # こっから下は，matplotlib・plotlyでデータ渡ししやすい配列の形に変形させてself.plot_active_tabに格納

            self.plot_active_tab = raw_data
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'active_tab.csv' not found."))
            exit()
    
    def get_mouse(self):
        '''
        ●(完)activetabで最後に終了タイムスタンプをしているけど，それより後の分もkeyboardとmouseはログが残っているので，除去すべきかも？
        したがって，開始時刻・終了時刻はactivetabのself.plot_active_tabの0番目と最後の時刻に基づく．
        ●self.hide_filtered_tab_duration=Trueの場合に，self.filter_tab_durationsに従ってNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
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
            with open("{dirname}/mouse.csv".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "Time" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split(",")) != 2:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split(",")
                    if len(splitted_column) != 2:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'mouse.csv'"))
                        exit()
                    # Digit check (If error, catch ValueError)
                    splitted_column[1] = float(splitted_column[1])
                    raw_data.append(splitted_column)
            # print("before: {}".format(raw_data))

            # [1st] Reshape raw_data to 1-second interval data (and fill in the blanks with None)
            # Get initial timestamp from self.plot_active_tab
            # Use as 1-second interval timestamp 
            current_time = datetime.datetime.strptime(self.plot_active_tab[0][0].split(".")[0], "%Y/%m/%d %H:%M:%S")
            '''
            # This code below is fixing current_time because the timestamp of mouse is earlier than the one of active_tab.
            # But there is also keyboard, so we should define the first timestamp of active_tab is the fastest log. (And the last timestamp of active_tab is the last log of active_tab, mouse, and keyboard)
            current_time = datetime.datetime.strptime(self.plot_active_tab[0][0], "%Y/%m/%d %H:%M:%S.%f")
            if (current_time - datetime.datetime.strptime(raw_data[0][0], "%Y/%m/%d %H:%M:%S.%f")).total_seconds() > 0:
                for mouse_i in range(1, len(raw_data)):
                    mouse_time = datetime.datetime.strptime(raw_data[mouse_i][0], "%Y/%m/%d %H:%M:%S.%f")
                    if (current_time - mouse_time).total_seconds() < 0:
                        break
                current_time = mouse_time
            '''
            # Get final timestamp from self.plot_active_tab
            # This final timestamp is also used in [2nd]
            final_time = datetime.datetime.strptime(self.plot_active_tab[len(self.plot_active_tab) - 1][0].split(".")[0], "%Y/%m/%d %H:%M:%S")
            new_raw_data = []
            raw_i = 0
            while (final_time - current_time).total_seconds() >= 0:
                str_current_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
                if str_current_time in raw_data[raw_i][0]:
                    new_raw_data.append([str_current_time, raw_data[raw_i][1]])
                    if str_current_time in raw_data[raw_i + 1][0]:
                        # Rarely, the same seconds duplicates in consecutive two timestamps
                        # print("Duplicated!!!: " + str_current_time)
                        new_raw_data[len(new_raw_data) - 1][1] += raw_data[raw_i + 1][1]
                        raw_i += 1
                    raw_i += 1
                else:
                    new_raw_data.append([str_current_time, None])
                current_time += datetime.timedelta(seconds=1)
            raw_data = new_raw_data
            # print(np.array(raw_data))
            # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            
            # [2nd]If self.hide_filtered_tab_duration=True, replace value to None in the duration of filtered tab
            if self.hide_filtered_tab_duration:
                durations_i = 0
                filter_start = datetime.datetime.strptime(self.filter_tab_durations[durations_i][0], "%Y/%m/%d %H:%M:%S")
                filter_end = datetime.datetime.strptime(self.filter_tab_durations[durations_i][1], "%Y/%m/%d %H:%M:%S")
                for raw_column in raw_data:
                    raw_time = datetime.datetime.strptime(raw_column[0], "%Y/%m/%d %H:%M:%S")
                    if filter_end

            print(np.array(raw_data))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            # [3rd] If user setted set_interval, reshape data following the user-setted interval
            if self.sec_interval > 1:
                current_time = datetime.datetime.strptime(raw_data[0][0], "%Y/%m/%d %H:%M:%S")
                new_raw_data = [raw_data[0]]
                raw_i = 1
                while raw_i < len(raw_data):
                    current_time += datetime.timedelta(seconds=self.sec_interval)
                    raw_time = datetime.datetime.strptime(raw_data[raw_i][0], "%Y/%m/%d %H:%M:%S")
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
                        raw_time = datetime.datetime.strptime(raw_data[raw_i][0], "%Y/%m/%d %H:%M:%S")
                    if (current_time - final_time).total_seconds() > 0:
                        # If current_time added by final interval is larger than 
                        # final_time(final timestamp of active_tab), replace the 
                        # value of current_time to the value of final_time.
                        current_time = final_time
                    new_raw_data.append([current_time.strftime("%Y/%m/%d %H:%M:%S"), sum_interval])
                raw_data = new_raw_data
            print(np.array(raw_data))

            self.plot_mouse = np.array(raw_data, dtype=object)
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'mouse.csv' not found."))
            exit()
        except ValueError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid record in 'mouse.csv'."))
            exit()

    def get_keyboard(self):
        '''
        ●activetabで最後に終了タイムスタンプをしているけど，それより後の分もkeyboardとmouseはログが残っているので，除去すべきかも？
        したがって，開始時刻・終了時刻はactivetabのself.plot_active_tabの0番目と最後の時刻に基づく．
        ●get_activetab()で削除したタブの期間のデータの削除も必要ありそうかな．
        これやるのはget_activetab()を行った場合のみにするか．
        でもグラフでどう表現する？データの削除というより0埋め？でも0だったとグラフで示すのもな…
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

        ※ただし，self.hide_filtered_tab_duration=Trueの場合に，self.filter_tab_durationsに従ってNaN・None埋めする．Falseならmouse・keyboardはactive_tabでフィルタリングされた期間もグラフ描写する．
        '''
        try:
            with open("{dirname}/keyboard.csv".format(dirname=self.dirname), "r", encoding="utf-8") as ft:
                raw_columns = ft.read().split("\n")
                if "Time" in raw_columns[0]:
                    raw_columns.pop(0)
                if len(raw_columns[-1].split(",")) != 2:
                    raw_columns.pop(-1)
                raw_data = []
                for raw_column in raw_columns:
                    splitted_column = raw_column.split(",")
                    if len(splitted_column) != 2:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid count of separating by ',' in 'keyboard.csv'"))
                        exit()
                    # Digit check (If error, catch ValueError)
                    splitted_column[1] = int(splitted_column[1])
                    raw_data.append(splitted_column)
                raw_data = np.array(raw_data, dtype=object)
            print("before: {}".format(raw_data))
        except FileNotFoundError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: 'keyboard.csv' not found."))
            exit()
        except ValueError:
            print(self.strfmr.get_colored_console_log("red",
                "Error: Invalid record in 'keyboard.csv'."))
            exit()