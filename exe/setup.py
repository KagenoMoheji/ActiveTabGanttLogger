from setuptools import setup
import platform

'''
[About 'install_requires']
●for both
・matplotlib
・numpy
・psutil
・pynput (or pyautogui)
(・pickle) (standard module?)
●for Windows10-64bit
・pypiwin32
・colorama
●for MacOS Mojave
・pyobjc
・pyobjc-framework-Quartz(included in "pyobjc"...??)
'''

os = platform.platform(terse=True)
install_requires = ["matplotlib", "numpy", "psutil", "pynput"] # "pyautogui"
if "Windows" in os:
    install_requires += [
        'pypiwin32;platform_system=="Windows"',
        'colorama;platform_system=="Windows"'
    ]
elif "Darwin" in os:
    install_requires += [
        "pyobjc",
        "pyobjc-framework-Quartz"
    ]

setup(
    name="ganttlogger",
    version="0.2.2",
    description="This CLI will monitor(active-tab, mouse, keyboard), log, and generate graphs.",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ganttlogger = app:main"
        ]
    },
    author="Goki Sugimura(KagenoMoheji)",
    author_email="shadowmoheji.pd@gmail.com",
    url="https://github.com/KagenoMoheji/GanttLogger",
    licence="MIT"
)