from setuptools import setup, find_packages
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
(・pywin32)
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
        "pypiwin32",
        "colorama"
    ]
elif "Darwin" in os:
    install_requires += [
        "pyobjc",
        "pyobjc-framework-Quartz"
    ]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="ganttlogger",
    version="0.1.6",
    description="This CLI will monitor(active-tab, mouse, keyboard), log, and plot graphs.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Goki Sugimura(KagenoMoheji)",
    author_email="shadowmoheji.pd@gmail.com",
    url="https://github.com/KagenoMoheji/GanttLogger",
    licence="MIT",
    packages=find_packages(),
    include_package_data=True,
    keywords=[
        "gantt",
        "log",
        "graph",
        "plot",
        "keyboard",
        "mouse",
        "active tab",
        "monitor",
        "ganttlogger"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "ganttlogger = ganttlogger.app:main"
        ]
    },
)