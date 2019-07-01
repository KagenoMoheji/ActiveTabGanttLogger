import datetime
import psutil
from AppKit import NSWorkspace as nsw
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)

class ActiveTabObserver:
    def __init__(self):
        pass
    
    def run(self):
        recent_active_tab_text = "START!"

    def close(self):
        pass





'''
class MouseObserver:
    pass
class KeyboardObserver:
    pass
'''