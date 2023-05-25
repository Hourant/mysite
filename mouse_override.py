from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QTimer, pyqtSignal
import sys

class LongClickButton(QPushButton):

    def __init__(self, text: str, parent):
        super().__init__(text, parent)
        self.timer = QTimer()
        # timer超时后执行longClick()
        self.timer.timeout.connect(self.longClick)

    # 重写mousePressEvent方法，开启timer
    def mousePressEvent(self, e):
        print('Press')
        # 超时时间是2秒
        self.timer.start(2000)

    # 重写mouseReleaseEvent方法，关闭timer
    def mouseReleaseEvent(self, e):
        print('Release')
        self.timer.stop()

    # 长按后要执行的操作
    def longClick(self):
        print("Long Click")
        # 这里必须也调用一次stop，因为有些场景下mouseReleaseEvent不会执行，
        # 比如调用了QMessageBox弹框时
        self.timer.stop()

