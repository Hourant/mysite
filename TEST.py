import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Button Shift Example")

        # 创建 5 个按钮并设置初始文本
        self.buttons = [QPushButton(str(i+1)) for i in range(5)]

        # 为每个按钮连接一个槽函数
        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, idx=i: self.shift_buttons(idx))

        # 创建布局并添加按钮
        layout = QHBoxLayout()
        for button in self.buttons:
            layout.addWidget(button)

        # 创建一个部件并设置为窗口的布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def shift_buttons(self, index):
        for i in range(index, len(self.buttons) - 1):

            self.buttons[i].setText(self.buttons[i + 1].text())

        # 清除最后一个按钮的文本
        self.buttons[-1].setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
