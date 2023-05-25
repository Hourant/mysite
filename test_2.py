from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QVBoxLayout, QWidget, QPushButton, \
    QHBoxLayout
from PyQt5.QtCore import QTimer, QEvent, Qt


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # 创建一个定时器，设定超时时间为10秒
        self.timer = QTimer(self)
        self.timer.setInterval(2000)  # 设置时间间隔为10秒（10000毫秒）
        self.timer.timeout.connect(self.return_to_main)  # 绑定超时事件到return_to_main方法

        # 创建StackedWidget
        self.stacked_widget = QStackedWidget(self)

        # 创建主界面，并添加一个按钮用于切换到次界面
        self.main_widget = QWidget(self)
        layout = QVBoxLayout(self.main_widget)
        self.main_label = QLabel("主界面", self.main_widget)
        self.main_label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("切换到次界面", self.main_widget)
        self.button.clicked.connect(self.show_sub)
        layout.addWidget(self.main_label)
        layout.addWidget(self.button)

        # 创建次界面
        self.sub_widget = QWidget(self)
        layout = QVBoxLayout(self.sub_widget)
        self.sub_label = QLabel("次界面，10秒无操作自动返回主界面", self.sub_widget)
        self.sub_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sub_label)

        # 将主界面和次界面添加到StackedWidget
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.sub_widget)

        # 设置主窗口的中心窗口
        self.setCentralWidget(self.stacked_widget)

        # 安装事件过滤器到次界面
        self.sub_widget.installEventFilter(self)

    def show_sub(self):
        # 显示次界面，并启动定时器
        self.stacked_widget.setCurrentWidget(self.sub_widget)
        self.timer.start()

    def return_to_main(self):
        # 显示主界面，并停止定时器
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.timer.stop()

    def eventFilter(self, obj, event):
        # 过滤所有事件
        if obj == self.sub_widget and event.type() in [QEvent.MouseButtonPress, QEvent.KeyRelease]:
            # 如果在次界面上有鼠标点击、键盘按键释放或鼠标移动事件，重启定时器
            self.timer.start()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
