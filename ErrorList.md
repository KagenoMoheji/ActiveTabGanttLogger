matplotlib,numpy,psutil,pynput,pypiwin32,colorama,pyobjc,pyobjc-framework-Quartz


# 未解決エラーリスト
- `ipaexg.ttf`をどうにか吸わせられないかなぁ…
    - Plotter.pyでの`__file__`が問題そう．
- たまに出る
```
Traceback (most recent call last):
  File "app.py", line 77, in <module>
  File "app.py", line 40, in main
  File "modules\Alone.py", line 40, in run
  File "modules\Plotter.py", line 254, in run
  File "modules\Plotter.py", line 675, in get_mouse
IndexError: list index out of range
[11764] Failed to execute script app
```

- exeにしたら出た．何これ？
```
C:\Users\reegg\git\test\dist\ganttlogger\modules\Plotter.py:308: UserWarning: Attempting to set identical left == right == 737254.0309270591 results in singular transformations; automatically expanding.
C:\Users\reegg\git\test\dist\ganttlogger\modules\Plotter.py:346: UserWarning: Attempting to set identical left == right == 737254.0309270591 results in singular transformations; automatically expanding.
```
