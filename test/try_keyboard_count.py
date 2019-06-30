from msvcrt import getch

while True:
    try:
        print(ord(getch()))
    except KeyboardInterrupt:
        print("Exit")