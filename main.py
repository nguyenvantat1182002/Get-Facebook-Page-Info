# from facebook import Page


# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
# p = Page('309540589433788', user_agent)

# print(p.get_name())
# print(p.get_likes())
# print(p.get_address())
# print(p.is_verified())

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

import sys
import os


files = ['user_agents.txt']
for file in files:
    if not os.path.exists(file):
        with open(file, 'x', encoding='utf-8') as _:
            pass

folders = ['output']
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)


app = QApplication(sys.argv)

win = MainWindow()
win.show()

sys.exit(app.exec_())
