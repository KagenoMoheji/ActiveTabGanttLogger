from collections import deque

'''
Variables work for managing a flag whether observers's threads should exit.
'''
# Whether pause children threads?
is_switched_to_exit = False
# Whether thread-loop exit because of error catch?
is_threadloop_error = False
# Whether threads 'Observer' and 'Logger' exited?
all_thread_exited = False


'''

'''
# コメントアウトのJSON構造は単なる配列に置き換える際の参考に．
# 初期データはid=-1としているので，それでフィルタリングしておく
# 送信時はJSONに変換してデータ取得時に送る
# 受信時にリストのインデックス2のidの連番で確認するなりソートするなりしてからファイル書き出しする
'''
{
    "uuid": "",
    "type": "t",
    "id": -1,
    "activeName": "",
    "tabText": "",
    "startTime": ""
}
'''
tab_queue = deque([])
tab_id = -1

'''
{
    "uuid": "",
    "type": "m",
    "id": -1,
    "distance": "",
    "time": ""
}
'''
mouse_queue = deque([])
mouse_id = -1

'''
{
    "uuid": "",
    "type": "k",
    "id": -1,
    "count": "",
    "time": ""
}
'''
keyboard_queue = deque([])
keyboard_id = -1