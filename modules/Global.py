from collections import deque

'''
Variables work for managing a flag whether observers's threads should exit.
'''
# Whether pause children threads?
is_switched_to_exit = False


'''

'''
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