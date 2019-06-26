
'''
References
    https://pod.hatenablog.com/entry/2017/02/11/194834
    https://qiita.com/Alice1017/items/0464a38ab335ac3b9336
'''
from setuptools import setup

setup(
    name="ganttlogger",
    version="0.0",
    # description="",
    install_requires=["matplotlib", "numpy"],
    entry_points={
        "console_scripts": [
            "ganttlogger = app:main"
        ]
    }
)