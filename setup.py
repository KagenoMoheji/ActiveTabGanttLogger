
'''
References
    https://pod.hatenablog.com/entry/2017/02/11/194834
    https://qiita.com/Alice1017/items/0464a38ab335ac3b9336
'''
from setuptools import setup
import platform

'''
[About 'install_requires']
●for Windows10-64bit
・pypiwin32
●for MacOS Mojave
・pyobjc
・pyobjc-framework-Quartz(included in "pyobjc"...??)
'''

os = platform.platform(terse=True)
install_requires = ["matplotlib", "numpy", "psutil", "pynput"] # "pyautogui"
if "Windows" in os:
    install_requires += [
        "pypiwin32"
    ]
elif "Darwin" in os:
    install_requires += [
        "pyobjc",
        "pyobjc-framework-Quartz"
    ]

setup(
    name="ganttlogger",
    version="0.0",
    # description="",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ganttlogger = app:main"
        ]
    }
)