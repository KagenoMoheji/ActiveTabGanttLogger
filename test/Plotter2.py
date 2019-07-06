'''
●ログファイルを読み込んでガントチャート生成・出力
・ファイル名にタイムスタンプつけとく
'''
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from modules.Public import StrFormatter

'''
本番のPlotter.pyと違い，2の冪和を用いたパーミッション(rwx)と同様の手法を条件分岐に用いている．
しかしうまく動作できず断念．本番ではBool型のフラグを使用．

References:
    http://ailaby.com/matplotlib_fig/#id4_1
    https://qiita.com/fujiy/items/f738aa9d0bb7427e07a4#%E8%A7%A3%E6%B1%BA%E7%AD%96
    https://www.haya-programming.com/entry/2018/05/26/031355
    https://note.nkmk.me/python-list-common/
    https://github.com/spyder-ide/spyder/issues/5401
    https://note.nkmk.me/python-check-int-float/
    https://pythondatascience.plavox.info/numpy/%E6%95%B0%E5%AD%A6%E7%B3%BB%E3%81%AE%E9%96%A2%E6%95%B0
    https://yukun.info/python-file/
'''

class Plotter:
    uuid = "" # If empty, this variable is unused
    dirname = ""
    sec_interval = 1 # The minimum interval is value is 1 second
    filter_tab_list = []
    select_data = ["all"]
    strfmr = None
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
        self.select_data = ["all"]

    def start(self):
        '''
        ●標準入力で
        (1)出力モードの選択(filter_tab/set_interval)
        (2)出力モードに合わせた必須項目への回答
        ※2の冪の部分和を分岐条件にする -> []内がそれ．1,2,4,8...的な
        [1]set_interval -> デルタtの数値指定(単位は秒)
        [2]fiter_tab -> 不要なタブ名(ログからコピペ)をまとめたテキストファイルの指定
        [4]select_data -> 3つのデータをサブプロットでまとめて出力するか，選択したデータで独立のプロットを出力するか(例えば，"all"なら1つの出力に3つのサブプロットが入っているが，一方3つのデータを選択した入力なら3つの出力が出る)
        '''
        try:
            # Set valid plot types here([1,2,4,8,...])
            plot_types_labels = set(["set_interval", "filter_tab", "select_data"])
            sum_powers_of_two = 0

            print(self.strfmr.get_colored_console_log("yellow", "[select plot types]"))
            print("""\
'set_interval': Set interval by seconds.
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
            # Get a sum of powers of 2 like permission(rwx)
            for plot_type in plot_types:
                if plot_type == "set_interval":
                    sum_powers_of_two += 1
                elif plot_type == "filter_tab":
                    sum_powers_of_two += 2
                elif plot_type == "select_data":
                    sum_powers_of_two += 4
            # Get arguments from stdin following the sum of powers of 2 below
            if sum_powers_of_two % 2 != 0:
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "[set_interval]\nSet the number of interval by seconds: "), end="")
                    self.sec_interval = input().strip()
                    if re.compile(r'^[0-9]+$').match(self.sec_interval):
                        break
                    else:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: Invalid input.\n(Example)If you want set 2 seconds for the interval, input '2'."))
            if sum_powers_of_two - 2 == 0 or \
                ((sum_powers_of_two - 2 > 0) and (np.log2(sum_powers_of_two - 2)).is_integer()):
                while True:
                    try:
                        print(self.strfmr.get_colored_console_log("yellow",
                        "[filter_tab]\nInput a file name written a list of tab text you want to filter.: "), end="")
                        txtname = "{dirname}/{filename}".format(dirname=self.dirname, filename=input().strip())
                        with open(txtname, "r", encoding="utf-8") as f:
                            self.filter_tab_list = f.read().split("\n")
                            break
                    except FileNotFoundError:
                        print(self.strfmr.get_colored_console_log("red",
                            "Error: File not found."))
                # print(self.filter_tab_list)
            if sum_powers_of_two - 4 == 0 or \
                ((sum_powers_of_two - 4 > 0) and (np.log2(sum_powers_of_two - 4)).is_integer()):
                while True:
                    print(self.strfmr.get_colored_console_log("yellow",
                        "[select_data]\nSelect 'all' or list separated by ',' with some csv file names like 'active_tab'.: "), end="")
                    self.select_data = list(map(lambda s: s.strip(), (input().strip()).split(",")))
                    if "all" in self.select_data: 
                        if len(self.select_data) == 1:
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: Too many select despite 'all'."))
                            continue
                    else:
                        select_data_labels = set(["active_tab", "mouse", "keyboard"])
                        xor_select_data = set(self.select_data) ^ select_data_labels
                        if len(xor_select_data) == 0 or \
                            all(x in select_data_labels for x in xor_select_data):
                            break
                        else:
                            print(self.strfmr.get_colored_console_log("red",
                                "Error: There are some Invalid names of csv files."))
            # if sum_powers_of_two - 8 == 0 or \
            #     ((sum_powers_of_two - 8 > 0) and (np.log2(sum_powers_of_two - 8)).is_integer()):

            print("sum_powers_of_two: {}".format(sum_powers_of_two))
            print("sec_interval: {}".format(self.sec_interval))
            print("")
            if self.select_data[0] == "all":
                self.run()
            else:
                self.run_each()
        except KeyboardInterrupt:
            print("Exit")
            exit()

    def run(self): # plot(self)
        '''
        ●plot_activetab，plot_mouse，plot_keyboardの全部を行う．
        ●plotで3つのサブプロットを用意するとして，どうやってサブプロットを
        上記3つの関数に渡すのか？？？？
        ●上記3つの関数でファイル読み込み・データ加工したリストを用意して，ここで
        サブプロットにプロット？
        '''
        print("Run, Plotter!")

    def run_each(self): # plot_each(self)
        '''
        ●run()が3つのサブプロットで1つのファイル出力をするのに対し，run_each()は
        1つのプロットで1つのファイル出力をする，つまり独立した出力をする関数．
        ●各出力ファイル名に日時を追加する．
        '''
        print("Run, Plotter-Each!")

    def get_activetab(self):
        # ファイル読み込み・データ加工をここで行う
        with open("{}/active_tab.csv".format(self.dirname), "r", encoding="utf-8") as f:
            pass
    
    def get_mouse(self):
        with open("{}/mouse.csv".format(self.dirname), "r", encoding="utf-8") as f:
            pass

    def get_keyboard(self):
        with open("{}/keyboard.csv".format(self.dirname), "r", encoding="utf-8") as f:
            pass