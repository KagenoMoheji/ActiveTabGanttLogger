import os
import sys
import re
import datetime
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as pld
import matplotlib.font_manager as plf
from ganttlogger.modules.Public import StrFormatter

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
        ●With stdin,
        (1)Select output mode. (set_interval/filter_tab/select_data/xaxis_type)
        (2)In each mode, set detail information.
        ・set_interval -> Set a number of seconds interval of data.
        ・fiter_tab -> Set a (text) file of the list of unneccesary tab-text.
        ・select_data -> Set "all" to plot a compiled graph, or select from ('active_tab'|'mouse'|'keyboard'|'mouse-keyboard') to plot each graphs.
        ・xaxis_type -> For x-axis, select "active-start" to set start times of active-tabs, or set a number of seconds to set times of the interval.
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
                        "(1)Select x-axis type for ActiveTab from whether 'active-start' or number of the interval by seconds: "), end="")
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
                        "(2)Select x-axis type for Mouse or Keyboard from whether 'active-start' or number of the interval by seconds: "), end="")
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
        Plot a compiled graph from active-tab, mouse and keyboard dataframe.

        ●We must execute four functions in the following order.
        (1)self.get_activetab()
        (2)self.get_mouse() or self.get_keyboard()
        (3)self.more_reshape_activetab()
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


        fig = plt.figure(figsize=(15, 9))
        # Get range of x axis
        init = self.plot_active_tab[0][0] # pld.date2num(self.plot_active_tab[0][0])
        last = self.plot_active_tab[len(self.plot_active_tab)-1][0] # pld.date2num(self.plot_active_tab[len(self.plot_active_tab)-1][0])

        # Create upper graph(ganttchart)
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.set_xlim(init, last)
        dates = []
        if self.xaxis_type_at == "active-start":
            dates = [t for t in self.plot_active_tab[:-1, 0]]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
        else:
            t = self.plot_active_tab[0][0]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            while (last_t - t).total_seconds() >= 0:
                dates.append(t)
                t += datetime.timedelta(seconds=int(self.xaxis_type_at))
            # print(last_t.second - dates[len(dates) - 1].second)
            # print(dates[len(dates) - 1].second - last_t.second)
        # Add the last time to x-axis
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
        for i, k in enumerate(self.df_active_tab.keys()):
            # Plot ganttchart following the turn of 'self.df_active_tab.keys()'
            ax1.broken_barh(self.df_active_tab[k], (5+i*10, 5), facecolor="red")
        plt.subplots_adjust(top=0.85, bottom=0.15, right=0.95, hspace=0)
        plt.title("SwitchActiveTab(interval: {}s)".format(self.sec_interval))
        ax1.xaxis.tick_top()
        ax1.grid(axis="y")
        

        # Create lower graph(line or bar graph)
        # ax2_1:mouse, ax2_2:keyboard
        ax2_1 = fig.add_subplot(2, 1, 2)
        ax2_2 = ax2_1.twinx()
        ax2_1.set_xlim(init, last)
        dates.clear()
        if self.xaxis_type_mk == "active-start":
            dates = [t for t in self.plot_active_tab[:-1, 0]]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
        else:
            t = self.plot_active_tab[0][0]
            last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            while (last_t - t).total_seconds() >= 0:
                dates.append(t)
                t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
        # Add the last time to x-axis
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


    def run_each(self):
        '''
        Plot each graphs following user-select(self.select_data).
        
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
        
        if "active_tab" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_at == "active-start":
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_at))
            # Add the last time to x-axis
            if (last_t - dates[len(dates) - 1]).total_seconds() > 0:
                dates.append(last_t)
            # datenums = pld.date2num(dates)
            ax.set_xticks(dates) # ax.set_xticks(datenums)
            plt.xlabel("t")
            ax.axes.tick_params(axis="x", labelsize=7, rotation=270)
            ax.xaxis.set_major_formatter(pld.DateFormatter("%Y/%m/%d %H:%M:%S")) # .%f
            fp = plf.FontProperties(fname="{}/../config/font/ipaexg.ttf".format(os.path.dirname(__file__)), size=8)
            y = [7.5 + i * 10 for i in range(len(self.df_active_tab.keys()))]
            y.append(y[len(y) - 1] + 10)
            ax.set_yticks(y)
            ax.set_yticklabels(self.df_active_tab.keys(), fontproperties=fp)
            for i, k in enumerate(self.df_active_tab.keys()):
                # Plot ganttchart following the turn of 'self.df_active_tab.keys()'
                # print(self.df_active_tab[k])
                ax.broken_barh(self.df_active_tab[k], (5+i*10, 5), facecolor="red")
            plt.title("SwitchActiveTab(interval: {}s)".format(self.sec_interval))
            ax.grid(axis="y")
            plt.subplots_adjust(top=0.95, bottom=0.2, right=0.99, left=0.2)
            with open("{dirname}/graphs/output_{datetime}_active_tab.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_active_tab".format(dirname=self.dirname, datetime=filetime))
        
        if "mouse" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_mk == "active-start":
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # Add the last time to x-axis
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
            plt.title("Mouse Distance(interval: {}s)".format(self.sec_interval))
            with open("{dirname}/graphs/output_{datetime}_mouse.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_mouse".format(dirname=self.dirname, datetime=filetime))
        
        if "keyboard" in self.select_data:
            fig = plt.figure(figsize=(15,6))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlim(init, last)
            dates = []
            if self.xaxis_type_mk == "active-start":
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # Add the last time to x-axis
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
                dates = [t for t in self.plot_active_tab[:-1, 0]]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
            else:
                t = self.plot_active_tab[0][0]
                last_t = self.plot_active_tab[len(self.plot_active_tab)-1][0]
                while (last_t - t).total_seconds() >= 0:
                    dates.append(t)
                    t += datetime.timedelta(seconds=int(self.xaxis_type_mk))
            # Add the last time to x-axis
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
            ax2.set_ylim(bottom=0)
            ax2.grid(axis="y")
            plt.title("Mouse and Keyboard(interval: {}s)".format(self.sec_interval))
            plt.subplots_adjust(top=0.95, bottom=0.25)
            with open("{dirname}/graphs/output_{datetime}_mouse-keyboard.pkl".format(dirname=self.dirname, datetime=filetime), "wb") as f:
                pickle.dump(fig, f)
            plt.savefig("{dirname}/graphs/output_{datetime}_mouse-keyboard".format(dirname=self.dirname, datetime=filetime))


    def get_activetab(self):
        '''
        Process data from "active_tab.log", output "self.plot_active_tab".
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
        Process "self.plot_mouse" and "self.plot_keyboard" using "self.plot_active_tab",
        and output updated ones and "self.df_active_tab".
        '''
        new_data = self.plot_active_tab.tolist()
        m_i, k_i = 0, 0
        for i in range(len(self.plot_active_tab) - 1):
            '''
            Get "FinishTime" by finding "Empty term" by judging whether both data of mouse and keyboard are None.
            If they are None, set the start time of "Empty term"(the later? None of mouse or keyboard) as "FinishTime", others, set the start time of next active-tab as "FinishTime".
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
        Process data from "mouse.log", output "self.plot_mouse".
        Process following "set_interval" and "filter_tab" are also here.
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
            while (final_time - current_time).total_seconds() >= 0: # Compare times(h:m:s)
                # Not include micro seconds when comparing string times
                str_current_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
                if str_current_time in raw_data[raw_i][0]: # Better to compare strings(h:m:s)
                    # Not include micro seconds to timestamp
                    new_raw_data.append([current_time, raw_data[raw_i][1]])
                    if raw_i + 1 >= len(raw_data):
                        break
                    if str_current_time in raw_data[raw_i+1][0]: # Better to compare strings(h:m:s)
                        # Rarely, the same seconds duplicates in consecutive two timestamps
                        # print("Duplicated!!!: " + str_current_time)
                        new_raw_data[len(new_raw_data)-1][1] += raw_data[raw_i+1][1]
                        raw_i += 1
                    raw_i += 1
                else:
                    # Not include micro seconds to timestamp
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
        Process data from "keyboard.log", output "self.plot_keyboard".
        Process following "set_interval" and "filter_tab" are also here.
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
            while (final_time - current_time).total_seconds() >= 0: # Compare times(h:m:s)
                # Not include micro seconds when comparing string times
                str_current_time = current_time.strftime("%Y/%m/%d %H:%M:%S")
                if str_current_time in raw_data[raw_i][0]: # Better to compare strings(h:m:s)
                    # Not include micro seconds to timestamp
                    new_raw_data.append([current_time, raw_data[raw_i][1]])
                    if raw_i + 1 >= len(raw_data):
                        break
                    if str_current_time in raw_data[raw_i+1][0]: # Better to compare strings(h:m:s)
                        # Rarely, the same seconds duplicates in consecutive two timestamps
                        # print("Duplicated!!!: " + str_current_time)
                        new_raw_data[len(new_raw_data)-1][1] += raw_data[raw_i+1][1]
                        raw_i += 1
                    raw_i += 1
                else:
                    # Not include micro seconds to timestamp
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
    