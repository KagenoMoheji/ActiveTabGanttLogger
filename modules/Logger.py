'''
●jsonを引数に受け取る
●jsonのid順にログ追記
●受信の場合はenv.jsonを読み込んで環境変数にする
'''
# import threading
import concurrent.futures as confu
from datetime import datetime # 定期間隔書き出しのタイムスタンプ用
import numpy as np

class RawDataStore:
    # コメントアウトのJSON構造は単なる配列に置き換える際の参考に．
    # 初期データはid=-1としているので，それでフィルタリングしておく
    # 送信時はJSONに変換してデータ取得時に送る
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
    raw_tab_data = np.array([["", "t", -1, "", "", ""]])
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
    raw_mouse_data = np.array([["", "m", -1, "", "", ""]])
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
    raw_keyboard_data = np.array([["", "k", -1, "", "", ""]])


class Logger:
    def __init__(self, uuid=""):
        if uuid:
            self.uuid = uuid
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

