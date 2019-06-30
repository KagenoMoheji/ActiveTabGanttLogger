'''
●jsonを引数に受け取る
●jsonのid順にログ追記
●受信の場合はenv.jsonを読み込んで環境変数にする
'''
import os
# import threading
import concurrent.futures as confu
from datetime import datetime # 定期間隔書き出しのタイムスタンプ用
# import numpy as np
from collections import deque

class RawDataStore:
    # コメントアウトのJSON構造は単なる配列に置き換える際の参考に．
    # 初期データはid=-1としているので，それでフィルタリングしておく
    # 送信時はJSONに変換してデータ取得時に送る
    # 受信時にリストのインデックス2のidの連番で確認するなりソートするなりしてからファイル書き出しする
    '''
    {
        "uuid": "",
        "tab": {
            "id": -1,
            "appName": "",
            "title": "",
            "startTime": ""
        }
    }
    '''
    raw_tab_data = deque([["", "t", -1, "", "", ""]])
    tab_id = 0
    '''
    {
        "uuid": "",
        "mouse": {
            "id": -1,
            "distance": "",
            "datetime": ""
        }
    }
    '''
    raw_mouse_data = deque([["", "m", -1, "", "", ""]])
    mouse_id = 0
    '''
    {
        "uuid": "",
        "keyboard": {
            "id": -1,
            "count": "",
            "datetime": ""
        }
    }
    '''
    raw_keyboard_data = deque([["", "k", -1, "", "", ""]])
    keyboard_id = 0


class Logger:
    uuid = ""
    def __init__(self, uuid):
        '''
        
        References:
            https://stackoverflow.com/a/12517490
        '''
        self.uuid = uuid

        # ログ・グラフの出力先フォルダ生成
        filename = "{}/README.txt".format(uuid)
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

    def run(self):
        print("Hello, Logger!")

    def receive_json(self):
        # jsonデータを受信してRawDataに格納する
        pass

    def file_logger(self):
        # RawDataの先頭から取り出して(かつ削除して)ファイル書き出し
        # ただしid=-1なら無視
        pass

    def close(self): pass

