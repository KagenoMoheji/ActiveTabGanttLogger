'''
●jsonを引数に受け取る
●jsonのid順にログ追記
●受信の場合はenv.jsonを読み込んで環境変数にする
'''
import os
from datetime import datetime
# import numpy as np
import modules.Global as global_v

class Logger:
    uuid = ""
    def __init__(self, uuid):
        '''
        
        References:
            https://stackoverflow.com/a/12517490
        '''
        self.uuid = uuid

        # ログ・グラフの出力先フォルダ生成
        filename = "ganttlogger_logs/{}/README.txt".format(uuid)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            startdate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            text = """\
UUID       : {uuid}
StartDate  : {startdate}
Supervisor : 
Target User: 
""".format(uuid=uuid, startdate=startdate)
            f.write(text)

        # データ受け取り・定期間隔でのファイル書き出しの並列処理なので最大2？
        pass

    def run_alone(self):
        print("Hello, Logger!")

    def run_logger(self):
        print("Hello, Logger!")

    def receive_json(self):
        # jsonデータを受信してRawDataに格納する
        pass

    def file_output(self):
        # RawDataの先頭から取り出して(かつ削除して)ファイル書き出し
        # ただしid=-1なら無視
        pass

    def close(self): pass

