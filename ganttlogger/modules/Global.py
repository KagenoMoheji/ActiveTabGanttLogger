from collections import deque

'''
Variables work for managing a flag whether observers's threads should exit.
'''
# Whether pausing children threads? (But actually, working in the backend)
is_sleeping = False
# Whether thread-loop exit because of error catch?
is_threadloop_error = False
# Whether threads 'Observer' and 'Logger' exited?
cli_exit = False
# Whether 'Logger' has finished all logging?
finish_logging = False


# Data structure is based on JSON.
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