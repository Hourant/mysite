import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPalette,QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import threading
import time
import sys
import wmi
# 创建 WMI 连接
import psutil
from memory_profiler import profile
import mouse_override
from window_main import Ui_main
from window_water import Ui_water
from  window_help import Ui_help
from window_custom import Ui_custom
#from mouse_override import *

class Window_main(QtWidgets.QWidget,Ui_main):
    # 在需要做性能分析的函数前面加装饰器 @profile
    def __init__(self, parent=None):
        super(Window_main, self).__init__(parent)
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)
        self.ui_custom = Ui_custom()
        self.ui_custom.setupUi(self.page_2)
        self.ui_help = Ui_help()
        self.ui_help.setupUi(self.page_4)
        self.ui_water = Ui_water()
        self.ui_water.setupUi(self.page_3)


        self.btn_custom.clicked.connect(self.display_custom)
        self.btn_water.clicked.connect(self.display_water)
        self.btn_help.clicked.connect(self.display_help)
        self.ui_custom.btn_return.clicked.connect(self.display_main)
        self.ui_help.btn_home.clicked.connect(self.display_main)
        self.ui_water.btn_help.clicked.connect(self.display_help)
        self.ui_water.btn_custom.clicked.connect(self.display_custom)


        QtGui.QFontDatabase.addApplicationFont("./FZZDXJW_0.ttf")
        QtGui.QFontDatabase.addApplicationFont("./FZY3JW.TTF")
        self.flag_btn = 0

#        self.ui_main_init()
        #按钮长按处理
        #print('A：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))


        self.setMyFont()
        self.ui_custom_init()


        self.ui_help_init()


        self.ui_custom.btn_2.setEnabled(False)
        self.ui_custom.btn_3.setEnabled(False)
        self.ui_custom.btn_4.setEnabled(False)
        self.ui_custom.btn_5.setEnabled(False)
        self.ui_custom.btn_6.setEnabled(False)

        self.return_timer = QTimer(self)
        self.return_timer.setInterval(10000)  # 设置时间间隔为10秒（10000毫秒）
        self.return_timer.timeout.connect(self.return_to_main)  # 绑定超时事件到return_to_main方法

        #安装过滤器
        self.page_2.installEventFilter(self)
        self.page_3.installEventFilter(self)
        self.page_4.installEventFilter(self)
        print('A：%.2f MB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))

    def eventFilter(self, obj, event):
        # 过滤所有事件
        if obj in [self.page_2, self.page_3, self.page_4] and event.type() in [QEvent.MouseButtonPress,
                                                                               QEvent.KeyRelease]:
            # 如果在这三个页面上有鼠标点击、键盘按键释放事件，重启定时器
            self.return_timer.start()

        return super().eventFilter(obj, event)


    def return_to_main(self):
        self.display_main()
        self.return_timer.stop()


    def setMyFont(self):
        QtGui.QFontDatabase.addApplicationFont("./font/FZY3JW.TTF")


    def display_main(self):
        self.stackedWidget.setCurrentIndex(0)


    def display_custom(self):
        self.return_timer.start()
        self.stackedWidget.setCurrentIndex(1)


    def display_water(self):
        self.return_timer.start()
        self.stackedWidget.setCurrentIndex(2)


    def display_help(self):
        self.return_timer.start()
        self.stackedWidget.setCurrentIndex(3)

#ui_main
    #def ui_main_init(self):

    def ui_help_init(self):
        self.ui_help.btn_wifi.clicked.connect(self.on_click_wifi)
        self.ui_help.btn_drain.clicked.connect(self.on_click_drain)
        self.ui_help.btn_999.clicked.connect(self.on_click_999)
        self.ui_help.btn_replace.clicked.connect(self.on_click_replace)
        self.ui_help.btn_instructions.clicked.connect(self.on_click_instructions)

        self.ui_help.btn_f_w.clicked.connect(self.close_f_w)

        self.ui_help.btn_guide.clicked.connect(self.on_click_guide)
        self.ui_help.btn_fault.clicked.connect(self.on_click_fault)
        self.ui_help.btn_filter.clicked.connect(self.on_click_filter)

        self.timer_drain = QTimer()
        self.timer_drain.timeout.connect(self.return_water)



    def close_f_w(self):
        self.ui_help.btn_f1.setEnabled(True)
        self.ui_help.btn_f2.setEnabled(True)
        self.ui_help.btn_f3.setEnabled(True)
        self.connect_signals(self.ui_help.btn_f1, self.on_click_f1)
        self.connect_signals(self.ui_help.btn_f2, self.on_click_f2)
        self.connect_signals(self.ui_help.btn_f3, self.on_click_f3)
        self.lower_widgets(self.ui_help.label_f_warn,self.ui_help.btn_f_w)


    def on_click_filter(self):
        self.ui_help.btn_f1.setEnabled(False)
        self.ui_help.btn_f2.setEnabled(False)
        self.ui_help.btn_f3.setEnabled(False)
        self.ui_help.label_filter.setStyleSheet("border-image: url(:/ui/Ui/help/bg_change.png);")
        self.ui_help.label_fault.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.ui_help.label_guide.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.raise_widgets(self.ui_help.label_filter_bg,self.ui_help.label_f1,self.ui_help.label_f2,self.ui_help.label_f3,
                           self.ui_help.label_f_warn,self.ui_help.btn_f_w,self.ui_help.btn_f1,self.ui_help.btn_f2,self.ui_help.btn_f3)


        self.ui_help.label_filter_bg.setStyleSheet("border-image: url(:/filter/Ui/help/1_03.jpg);")


    def replace_warning(self):
        self.raise_widgets(self.ui_help.label_f_replace,self.ui_help.btn_f_re_yes)
        #self.raise_widgets(self.ui_help.label_f_warn,self.ui_help.btn_w_y)
        self.connect_signals(self.ui_help.btn_f_re_yes,self.on_click_reyes)


    def on_click_w_yes(self):
        self.lower_widgets(self.ui_help.label_f_replace,self.ui_help.btn_w_y)


    def on_click_f1(self):
        self.ui_help.label_f_replace.setStyleSheet("border-image: url(:/filter/Ui/help/f_replace.png);")
        self.replace_warning()

        self.ui_help.label_f1.setStyleSheet("border-image: url(:/filter/Ui/help/f1-1.png);")
        self.ui_help.label_f2.setStyleSheet("border-image: url(:/filter/Ui/help/f2.png);")
        self.ui_help.label_f3.setStyleSheet("border-image: url(:/filter/Ui/help/f3.png);")
        self.ui_help.label_filter_bg.setStyleSheet("border-image: url(:/filter/Ui/help/f1_bg.jpg);")


    def on_click_f2(self):
        self.ui_help.label_f_replace.setStyleSheet("border-image: url(:/filter/Ui/help/f_replace.png);")
        self.replace_warning()

        self.ui_help.label_f1.setStyleSheet("border-image: url(:/filter/Ui/help/f1.png);")
        self.ui_help.label_f2.setStyleSheet("border-image: url(:/filter/Ui/help/f2-1.png);")
        self.ui_help.label_f3.setStyleSheet("border-image: url(:/filter/Ui/help/f3.png);")
        self.ui_help.label_filter_bg.setStyleSheet("border-image: url(:/filter/Ui/help/f2_bg.jpg);")


    def on_click_f3(self):
        self.ui_help.label_f_replace.setStyleSheet("border-image: url(:/filter/Ui/help/f_replace.png);")
        self.replace_warning()

        self.ui_help.label_f1.setStyleSheet("border-image: url(:/filter/Ui/help/f1.png);")
        self.ui_help.label_f2.setStyleSheet("border-image: url(:/filter/Ui/help/f2.png);")
        self.ui_help.label_f3.setStyleSheet("border-image: url(:/filter/Ui/help/f3-1.png);")
        self.ui_help.label_filter_bg.setStyleSheet("border-image: url(:/filter/Ui/help/f3_bg.jpg);")


    def on_click_guide(self):
        self.ui_help.label_guide.setStyleSheet("border-image: url(:/ui/Ui/help/bg_change.png);")
        self.ui_help.label_fault.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.ui_help.label_filter.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.lower_widgets(self.ui_help.label_filter_bg,self.ui_help.label_f1,self.ui_help.label_f2,self.ui_help.label_f3,
                           self.ui_help.label_f_warn,self.ui_help.btn_f_w)

        self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")
        self.raise_widgets(self.ui_help.label_bg)
        self.lower_widgets(self.ui_help.label_drain_info)
        self.raise_widgets(self.ui_help.btn_wifi,self.ui_help.btn_drain,self.ui_help.btn_999,self.ui_help.btn_replace,self.ui_help.btn_instructions)
        if self.flag_btn == 0:
            self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")

        if self.flag_btn ==1:
            self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")
            self.lower_widgets(self.ui_help.label_set_wifi, self.ui_help.btn_wifi_reset, self.ui_help.btn_wifi_connect)
            self.lower_widgets(self.ui_help.label_drain_info)

        if self.flag_btn == 3:
            self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")
            self.lower_widgets(self.ui_help.label_dts, self.ui_help.btn_ban, self.ui_help.btn_allow)
            self.lower_widgets( self.ui_help.label_drain_info)

        if self.flag_btn == 4:
            self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")
            self.lower_widgets( self.ui_help.btn_next, self.ui_help.btn_return)
            self.lower_widgets(self.ui_help.label_set_wifi, self.ui_help.btn_wifi_reset, self.ui_help.btn_wifi_connect)
            self.lower_widgets(self.ui_help.label_dts, self.ui_help.btn_ban, self.ui_help.btn_allow)
            self.lower_widgets(self.ui_help.label_drain_info)


    def on_click_fault(self):
        self.ui_help.label_fault.setStyleSheet("border-image: url(:/ui/Ui/help/bg_change.png);")
        self.ui_help.label_guide.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.ui_help.label_filter.setStyleSheet("border-image: url(:/ui/Ui/help/bg.jpg);")
        self.update_fault_page(6)
        self.raise_widgets(self.ui_help.label_bg, self.ui_help.btn_next, self.ui_help.btn_return)


    def on_click_instructions(self):
        self.update_button_style(self.ui_help.btn_wifi, ":/btn/Ui/help/1.png")
        self.update_button_style(self.ui_help.btn_drain, ":/btn/Ui/help/2.png")
        self.update_button_style(self.ui_help.btn_999, ":/btn/Ui/help/3.png")
        self.update_button_style(self.ui_help.btn_replace, ":/btn/Ui/help/4.png")
        self.update_button_style(self.ui_help.btn_instructions, ":/btn/Ui/help/5-5.png")


    def on_click_replace(self):
        #self.lower_widgets(self.ui_help.btn_f1,self.ui_help.btn_f2,self.ui_help.btn_f3)
        self.update_button_style(self.ui_help.btn_wifi, ":/btn/Ui/help/1.png")
        self.update_button_style(self.ui_help.btn_drain, ":/btn/Ui/help/2.png")
        self.update_button_style(self.ui_help.btn_999, ":/btn/Ui/help/3.png")
        self.update_button_style(self.ui_help.btn_replace, ":/btn/Ui/help/4-4.png")
        self.update_button_style(self.ui_help.btn_instructions, ":/btn/Ui/help/5.png")
        self.update_help_page(1)
        self.flag_btn = 4
        self.raise_widgets(self.ui_help.label_bg, self.ui_help.btn_next, self.ui_help.btn_return)

        #self.connect_signals(self.ui_help.btn_guide, self.return_help)
        #self.ui_help.btn_guide.clicked.connect(self.return_help)

    # def return_help(self):
    #     self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg_03.png);")
    #     self.lower_widgets( self.ui_help.label_drain_info)
    #     self.timer_drain.stop()

    def on_click_reyes(self):

        # self.raise_widgets(self.ui_help.btn_f1, self.ui_help.btn_f2, self.ui_help.btn_f3)
        self.raise_widgets(self.ui_help.btn_w_y)
        self.ui_help.label_f_replace.setStyleSheet("border-image: url(:/filter/Ui/help/f_warn2.png);")
        self.connect_signals(self.ui_help.btn_w_y, self.on_click_w_yes)


    def raise_widgets(self, *widgets):
        for widget in widgets:
            widget.raise_()


    def lower_widgets(self, *widgets):
        for widget in widgets:
            widget.lower()


    def connect_signals(self, btn, func):
        try:
            btn.clicked.disconnect()
        except TypeError:
            pass
        btn.clicked.connect(func)


    def update_help_page(self, page_num):
        self.ui_help.label_bg.setStyleSheet(f"border-image: url(:/replace/Ui/help/{page_num}.jpg);")

        if page_num < 5:
            self.connect_signals(self.ui_help.btn_next, lambda: self.update_help_page(page_num + 1))
        if page_num > 1:
            self.connect_signals(self.ui_help.btn_return, lambda: self.update_help_page(page_num - 1))


    def update_fault_page(self, page_num):
        self.ui_help.label_bg.setStyleSheet(f"border-image: url(:/fault/Ui/help/{page_num}.jpg);")

        if page_num < 8:
            self.connect_signals(self.ui_help.btn_next, lambda: self.update_fault_page(page_num + 1))
        if page_num > 6:
            self.connect_signals(self.ui_help.btn_return, lambda: self.update_fault_page(page_num - 1))


    def on_click_999(self):
        self.ui_help.label_bg.setStyleSheet("background-color: rgb(239, 247, 250);")
        self.update_button_style(self.ui_help.btn_wifi, ":/btn/Ui/help/1.png")
        self.update_button_style(self.ui_help.btn_drain, ":/btn/Ui/help/2.png")
        self.update_button_style(self.ui_help.btn_999, ":/btn/Ui/help/3-3.png")
        self.update_button_style(self.ui_help.btn_replace, ":/btn/Ui/help/4.png")
        self.update_button_style(self.ui_help.btn_instructions, ":/btn/Ui/help/5.png")
        self.flag_btn = 3
        self.lower_widgets(self.ui_help.label_set_wifi, self.ui_help.btn_wifi_reset, self.ui_help.btn_wifi_connect)
        self.raise_widgets(self.ui_help.label_dts, self.ui_help.btn_ban, self.ui_help.btn_allow)

        self.connect_signals(self.ui_help.btn_ban, self.on_click_ban)
        self.connect_signals(self.ui_help.btn_allow, self.on_click_allow)


    def on_click_ban(self):
        self.ui_help.label_bg.setStyleSheet("background-color: rgb(239, 247, 250);")
        self.update_button_style(self.ui_help.btn_ban, ":/999/Ui/help/ban_press.png")
        self.update_button_style(self.ui_help.btn_allow, ":/999/Ui/help/allow.png")


    def on_click_allow(self):
        self.ui_help.label_bg.setStyleSheet("background-color: rgb(239, 247, 250);")
        self.update_button_style(self.ui_help.btn_allow, ":/999/Ui/help/allow_press.png")
        self.update_button_style(self.ui_help.btn_ban, ":/999/Ui/help/ban.png")


    def update_button_style(self, btn, style):
        btn.setStyleSheet(f"border-image: url({style});")


    def on_click_drain(self):
        self.update_button_style(self.ui_help.btn_drain, ":/btn/Ui/help/2-2.png")
        self.update_button_style(self.ui_help.btn_wifi, ":/btn/Ui/help/1.png")
        self.update_button_style(self.ui_help.btn_999, ":/btn/Ui/help/3.png")
        self.update_button_style(self.ui_help.btn_replace, ":/btn/Ui/help/4.png")
        self.update_button_style(self.ui_help.btn_instructions, ":/btn/Ui/help/5.png")
        self.ui_help.label_bg.setGeometry(QtCore.QRect(0, 0, 800, 480))
        self.ui_help.label_bg.setStyleSheet("border-image: url(:/drain/Ui/help/bg_water.jpg);")
        self.raise_widgets(self.ui_help.label_bg,self.ui_help.label_drain_info)

        self.timer_drain.start(3000)


    def return_water(self):
        self.timer_drain.stop()
        self.ui_help.label_bg.setGeometry(QtCore.QRect(0, 0, 800, 390))
        self.ui_help.label_bg.setStyleSheet("border-image: url(:/ui/Ui/help/bg.png);")

        self.lower_widgets( self.ui_help.label_drain_info)
        self.raise_widgets(self.ui_help.btn_wifi, self.ui_help.btn_drain, self.ui_help.btn_999,
                           self.ui_help.btn_replace, self.ui_help.btn_instructions)


    def on_click_wifi(self):
        self.ui_help.label_bg.setStyleSheet("background-color: rgb(239, 247, 250);")
        self.update_button_style(self.ui_help.btn_wifi,  ":/btn/Ui/help/1-1.png")
        self.update_button_style(self.ui_help.btn_drain, ":/btn/Ui/help/2.png")
        self.update_button_style(self.ui_help.btn_999, ":/btn/Ui/help/3.png")
        self.update_button_style(self.ui_help.btn_replace, ":/btn/Ui/help/4.png")
        self.update_button_style(self.ui_help.btn_instructions, ":/btn/Ui/help/5.png")
        self.flag_btn = 1
        self.lower_widgets(self.ui_help.label_dts, self.ui_help.btn_ban, self.ui_help.btn_allow)


        self.raise_widgets(self.ui_help.label_set_wifi, self.ui_help.btn_wifi_reset, self.ui_help.btn_wifi_connect)
        self.connect_signals(self.ui_help.btn_wifi_connect, self.set_wifi)
        self.connect_signals(self.ui_help.btn_wifi_reset, self.reset_wifi)


    def reset_wifi(self):
        self.update_button_style(self.ui_help.label_set_wifi, ":/wifi/Ui/help/reset.png")
        self.connect_signals(self.ui_help.btn_wifi_connect, self.on_click_return)


    def set_wifi(self):
        self.update_button_style(self.ui_help.label_set_wifi, ":/wifi/Ui/help/connect.png")
        self.connect_signals(self.ui_help.btn_wifi_connect, self.on_click_return)


    def on_click_return(self):
        self.update_button_style(self.ui_help.label_set_wifi, ":/wifi/Ui/help/set.png")
        self.connect_signals(self.ui_help.btn_wifi_connect, self.set_wifi)

         #ui_custom


    def ui_custom_init(self):

        with open("config.json", "r") as f:
            content = json.load(f)
        configs = {

            "config_num": 0
        }
        content.update(configs)
        with open("config.json", 'w') as f_new:
            json.dump(content, f_new, indent=2)
        self.timer = QTimer()
        self.buttons =[self.ui_custom.btn_1,self.ui_custom.btn_2,self.ui_custom.btn_3,
                       self.ui_custom.btn_4,self.ui_custom.btn_5,self.ui_custom.btn_6]
        self.labels_temp = [self.ui_custom.label_1_temp,self.ui_custom.label_2_temp,self.ui_custom.label_3_temp,
                            self.ui_custom.label_4_temp,self.ui_custom.label_5_temp,self.ui_custom.label_6_temp]
        self.labels_amount = [self.ui_custom.label_1_amount, self.ui_custom.label_2_amount, self.ui_custom.label_3_amount,
                            self.ui_custom.label_4_amount, self.ui_custom.label_5_amount, self.ui_custom.label_6_amount]

        self.labels_splash = [self.ui_custom.label_splash,self.ui_custom.label_splash_2,self.ui_custom.label_splash_3
                              ,self.ui_custom.label_splash_4,self.ui_custom.label_splash_5,self.ui_custom.label_splash_6]

        self.labels_plus = [self.ui_custom.label_plus,self.ui_custom.label_plus_2,self.ui_custom.label_plus_3,self.ui_custom.label_plus_4
                            ,self.ui_custom.label_plus_5,self.ui_custom.label_plus_6]

        self.flag = [0,0,0,0,0,0]

        # self.buttons[1].setEnabled(False)
        # self.buttons[2].setEnabled(False)
        # self.buttons[3].setEnabled(False)
        # self.buttons[4].setEnabled(False)
        # self.buttons[5].setEnabled(False)


        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.longClick)
        self.ui_custom.btn_1.pressed.connect(self.on_press_1)
        self.ui_custom.btn_1.released.connect(self.on_release_1)

        self.ui_custom.btn_2.pressed.connect(self.on_press_2)
        self.ui_custom.btn_2.released.connect(self.on_release_2)

        self.ui_custom.btn_3.pressed.connect(self.on_press_3)
        self.ui_custom.btn_3.released.connect(self.on_release_3)

        self.ui_custom.btn_4.pressed.connect(self.on_press_4)
        self.ui_custom.btn_4.released.connect(self.on_release_4)

        self.ui_custom.btn_5.pressed.connect(self.on_press_5)
        self.ui_custom.btn_5.released.connect(self.on_release_5)

        self.ui_custom.btn_6.pressed.connect(self.on_press_6)
        self.ui_custom.btn_6.released.connect(self.on_release_6)

        self.ui_custom.btn_del_no.clicked.connect(self.del_no)


        self.ui_custom.btn_del_yes.clicked.connect(self.shift_buttons)



        #self.ui_custom.btn_return.clicked.connect(self.display_main)
        self.ui_custom.label_amount.setAlignment(Qt.AlignCenter)#label中字体上下左右居中
        self.ui_custom.label_num.setText("1")

        self.ui_custom.btn_reset.pressed.connect(self.change_pic_reset)
        self.ui_custom.btn_reset.released.connect(self.origin_pic_reset)
        self.ui_custom.btn_reset.clicked.connect(self.custom_reset)

        self.ui_custom.btn_ok.pressed.connect(self.change_pic_ok)
        self.ui_custom.btn_ok.released.connect(self.origin_pic_ok)
        self.ui_custom.btn_ok.clicked.connect(self.onclick_ok)

        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")

        self.ui_custom.label_temp.setText('45')
        self.ui_custom.label_amount.setText('50')
        self.ui_custom.slider_temp.setMaximum(98)
        self.ui_custom.slider_temp.setMinimum(45)
        self.ui_custom.slider_amount.setMaximum(1000)
        self.ui_custom.slider_amount.setMinimum(50)

        self.ui_custom.slider_temp.valueChanged.connect(self.showMsg_temp)
        self.ui_custom.slider_amount.valueChanged.connect(self.showMsg_amount)

        self.ui_custom.slider_temp.setValue(80)
        self.ui_custom.slider_amount.setValue(450)
        self.showMsg_temp()
        self.showMsg_amount()


    #qslider
    def showMsg_temp(self):
        self.ui_custom.label_temp.setText(str(self.ui_custom.slider_temp.value()))
        y = 108
        x = 290 + ((self.ui_custom.slider_temp.value()-self.ui_custom.slider_temp.minimum())/(
                self.ui_custom.slider_temp.maximum()-self.ui_custom.slider_temp.minimum()))*320
        self.ui_custom.label_temp.move(x,y)


    def showMsg_amount(self):
        self.ui_custom.label_amount.setText(str(self.ui_custom.slider_amount.value()))
        self.ui_custom.label_amount.setAlignment(Qt.AlignCenter)
        y= 185
        x = 270 + ((self.ui_custom.slider_amount.value() - self.ui_custom.slider_amount.minimum()) / (
                    self.ui_custom.slider_amount.maximum() - self.ui_custom.slider_amount.minimum())) * 320
        self.ui_custom.label_amount.move(x,y)


    #btn_reset
    def change_pic_reset(self):
        self.ui_custom.label_reset.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_press_reset.png);")


    def origin_pic_reset(self):
        self.ui_custom.label_reset.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_reset.png);")


    def custom_reset(self):
        self.ui_custom.slider_temp.setValue(45)
        self.ui_custom.slider_amount.setValue(50)
        self.showMsg_temp()
        self.showMsg_amount()
    #btn_ok

    def change_pic_ok(self):
        self.ui_custom.label_ok.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_press_ok.png);")


    def origin_pic_ok(self):
        self.ui_custom.label_ok.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_ ok.png);")


    def onclick_ok(self):

        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])




        if self.ui_custom.label_num.text() == "1":
            # if self.buttons[1].isEnabled():

            if self.ui_custom.label_2_temp.text() != "" or self.num > 1:
                self.ui_custom.label_plus_2.lower()
            if self.num <= 1:
                self.ui_custom.label_plus_2.raise_()
                self.ui_custom.btn_2.setEnabled(True)
                self.ui_custom.btn_3.setEnabled(False)
                self.ui_custom.btn_4.setEnabled(False)
                self.ui_custom.btn_5.setEnabled(False)
                self.ui_custom.btn_6.setEnabled(False)

            self.labels_temp[0].raise_()
            self.labels_amount[0].raise_()
            self.ui_custom.label_plus.lower()
            self.ui_custom.label_splash.raise_()

            self.ui_custom.label_1_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_1_amount.setText(str(self.ui_custom.slider_amount.value()))
            #self.buttons[1].setEnabled(True)
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config1_temp": self.ui_custom.label_1_temp.text(),
                "config1_amount": self.ui_custom.label_1_amount.text(),

            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[0] == 0:
            # 将json 数据更新文件中
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {
                    "config_num": 1
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new,indent=2)
                self.flag[0] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()
        if self.ui_custom.label_num.text() == "2":

            if self.ui_custom.label_3_temp.text() != ""or self.num > 2:
                self.ui_custom.label_plus_3.lower()
            if self.num <= 2:
                self.ui_custom.label_plus_3.raise_()
                self.ui_custom.btn_3.setEnabled(True)
                self.ui_custom.btn_4.setEnabled(False)
                self.ui_custom.btn_5.setEnabled(False)
                self.ui_custom.btn_6.setEnabled(False)
            self.labels_temp[1].raise_()
            self.labels_amount[1].raise_()
            self.ui_custom.label_plus_2.lower()
            self.ui_custom.label_splash_2.raise_()
            self.ui_custom.label_2_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_2_amount.setText(str(self.ui_custom.slider_amount.value()))
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config2_temp": self.ui_custom.label_2_temp.text(),
                "config2_amount": self.ui_custom.label_2_amount.text(),

            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[1] == 0:
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {

                    "config_num": 2
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new,indent=2)
                self.flag[1] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()


        if self.ui_custom.label_num.text() == "3":

            if self.ui_custom.label_4_temp.text() != "" or self.num > 3:
                self.ui_custom.label_plus_4.lower()
            if self.num <= 3:
                self.ui_custom.label_plus_4.raise_()
                self.ui_custom.btn_3.setEnabled(True)
                self.ui_custom.btn_4.setEnabled(True)
                self.ui_custom.btn_5.setEnabled(False)
                self.ui_custom.btn_6.setEnabled(False)
            self.labels_temp[2].raise_()
            self.labels_amount[2].raise_()
            self.ui_custom.label_plus_3.lower()
            self.ui_custom.label_splash_3.raise_()
            self.ui_custom.label_3_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_3_amount.setText(str(self.ui_custom.slider_amount.value()))
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config3_temp": self.ui_custom.label_3_temp.text(),
                "config3_amount": self.ui_custom.label_3_amount.text(),
            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[2] == 0:
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {
                    "config_num": 3
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new, indent=2)
                self.flag[2] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()

        if self.ui_custom.label_num.text() == "4":
            if self.ui_custom.label_5_temp.text() != ""or self.num > 4:
                self.ui_custom.label_plus_5.lower()
            if self.num <= 4:
                self.ui_custom.label_plus_5.raise_()
                self.ui_custom.btn_3.setEnabled(True)
                self.ui_custom.btn_4.setEnabled(True)
                self.ui_custom.btn_5.setEnabled(True)
                self.ui_custom.btn_6.setEnabled(False)
            self.labels_temp[3].raise_()
            self.labels_amount[3].raise_()
            self.ui_custom.label_plus_4.lower()
            self.ui_custom.label_splash_4.raise_()
            self.ui_custom.label_4_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_4_amount.setText(str(self.ui_custom.slider_amount.value()))
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config4_temp": self.ui_custom.label_4_temp.text(),
                "config4_amount": self.ui_custom.label_4_amount.text(),
            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[3] == 0:
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {
                    "config_num": 4
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new, indent=2)
                self.flag[3] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()

        if self.ui_custom.label_num.text() == "5":
            if self.ui_custom.label_6_temp.text() != "" or self.num > 5:
                self.ui_custom.label_plus_6.lower()
            if self.num <=5 :
                self.ui_custom.label_plus_6.raise_()
                self.ui_custom.btn_3.setEnabled(True)
                self.ui_custom.btn_4.setEnabled(True)
                self.ui_custom.btn_5.setEnabled(True)
                self.ui_custom.btn_6.setEnabled(True)

            self.labels_temp[4].raise_()
            self.labels_amount[4].raise_()
            self.ui_custom.label_plus_5.lower()
            self.ui_custom.label_splash_5.raise_()
            self.ui_custom.label_5_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_5_amount.setText(str(self.ui_custom.slider_amount.value()))
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config5_temp": self.ui_custom.label_5_temp.text(),
                "config5_amount": self.ui_custom.label_5_amount.text(),

            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[4] == 0:
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {
                    "config_num": 5
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new, indent=2)
                self.flag[4] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()

        if self.ui_custom.label_num.text() == "6":
            self.ui_custom.label_6_amount.raise_()
            self.ui_custom.label_6_temp.raise_()
            self.labels_temp[5].raise_()
            self.labels_amount[5].raise_()
            self.ui_custom.label_plus_6.lower()
            self.ui_custom.label_splash_6.raise_()
            self.ui_custom.label_6_temp.setText(str(self.ui_custom.slider_temp.value()))
            self.ui_custom.label_6_amount.setText(str(self.ui_custom.slider_amount.value()))
            with open("config.json", "r") as f:
                content = json.load(f)
            configs = {
                "config6_temp": self.ui_custom.label_6_temp.text(),
                "config6_amount": self.ui_custom.label_6_amount.text(),
            }
            content.update(configs)

            with open("config.json", 'w') as f_new:
                json.dump(content, f_new, indent=2)
            if self.flag[5] == 0:
                with open("config.json", "r") as f:
                    content = json.load(f)
                configs = {
                    "config_num": 6
                }
                content.update(configs)

                with open("config.json", 'w') as f_new:
                    json.dump(content, f_new, indent=2)
                self.flag[5] = 1
            self.ui_custom.btn_6.raise_()
            self.ui_custom.btn_5.raise_()
            self.ui_custom.btn_4.raise_()
            self.ui_custom.btn_2.raise_()
            self.ui_custom.btn_1.raise_()
            self.ui_custom.btn_3.raise_()



    def longClick(self):


        self.ui_custom.label_delet.raise_()
        self.ui_custom.label_del_num.raise_()
        self.ui_custom.btn_del_yes.raise_()
        self.ui_custom.btn_del_no.raise_()
        self.ui_custom.label_del_num.setText(self.ui_custom.label_num.text())
        self.timer.stop()


    def on_press_1(self):


        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])
        if self.num > 0:
            self.timer.start()
        self.ui_custom.label_num.setText("1")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_1_temp.text() == "" or self.num < 1:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num >= 1:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config1_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config1_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def  on_release_1(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def on_press_2(self):
        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])
        if self.num > 1:
            self.timer.start()
        self.ui_custom.label_num.setText("2")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_2_temp.text() == ""or self.num < 2:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num >= 2:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config2_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config2_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def  on_release_2(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def on_press_3(self):

        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])
        if self.num > 2:
            self.timer.start()
        self.ui_custom.label_num.setText("3")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_3_temp.text() == "" or self.num < 3:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num >= 3:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config3_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config3_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def on_release_3(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def on_press_4(self):
        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])
        if self.num >3:
         self.timer.start()
        self.ui_custom.label_num.setText("4")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_4_temp.text() == ""or self.num < 4:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num >= 4:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config4_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config4_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def on_release_4(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def on_press_5(self):
        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])
        if self.num > 4:
            self.timer.start()
        self.ui_custom.label_num.setText("5")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_5_temp.text() == "" or self.num < 5:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num >= 5:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config5_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config5_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def on_release_5(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def on_press_6(self):
        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])


        if self.num > 5:
         self.timer.start()
        self.ui_custom.label_num.setText("6")
        self.ui_custom.label_6.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac2.jpg);")
        self.ui_custom.label_5.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_4.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_3.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_2.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        self.ui_custom.label_1.setStyleSheet("border-image: url(:/custom/Ui/custom/btn_bac.jpg);")
        if self.ui_custom.label_6_temp.text() == ""or self.num < 6:
            self.ui_custom.slider_temp.setValue(80)
            self.ui_custom.slider_amount.setValue(450)
            self.showMsg_temp()
            self.showMsg_amount()
        if self.num == 6:
            f = open("config.json")
            contents = f.read()
            contents = json.loads(contents)
            f.close()
            self.ui_custom.slider_temp.setValue(int(contents["config6_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config6_amount"]))
            self.showMsg_temp()
            self.showMsg_amount()


    def on_release_6(self):
        if self.timer.remainingTime() >= 0:
            pass
        self.timer.stop()


    def del_no(self):
        self.ui_custom.label_delet.lower()
        self.ui_custom.label_del_num.lower()
        self.ui_custom.btn_del_yes.lower()
        self.ui_custom.btn_del_no.lower()


    def shift_buttons(self):
        self.ui_custom.label_delet.lower()
        self.ui_custom.label_del_num.lower()
        self.ui_custom.btn_del_yes.lower()
        self.ui_custom.btn_del_no.lower()

        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        self.num = int(contents["config_num"])


        b = int(self.ui_custom.label_del_num.text())
        for i in range(b-1, self.num-1 ):
            self.labels_temp[i].setText(self.labels_temp[i + 1].text())
            self.labels_amount[i].setText(self.labels_amount[i + 1].text())

        with open("config.json", "r") as f:
            content = json.load(f)
        configs = {
            "config1_temp": self.ui_custom.label_1_temp.text(),
            "config1_amount": self.ui_custom.label_1_amount.text(),
            "config2_temp": self.ui_custom.label_2_temp.text(),
            "config2_amount": self.ui_custom.label_2_amount.text(),
            "config3_temp": self.ui_custom.label_3_temp.text(),
            "config3_amount": self.ui_custom.label_3_amount.text(),
            "config4_temp": self.ui_custom.label_4_temp.text(),
            "config4_amount": self.ui_custom.label_4_amount.text(),
            "config5_temp": self.ui_custom.label_5_temp.text(),
            "config5_amount": self.ui_custom.label_5_amount.text(),
            "config6_temp": self.ui_custom.label_6_temp.text(),
            "config6_amount": self.ui_custom.label_6_amount.text(),

        }
        content.update(configs)


        with open("config.json", 'w') as f_new:
            json.dump(content, f_new, indent=2)

        f = open("config.json")
        contents = f.read()
        contents = json.loads(contents)
        f.close()
        if self.ui_custom.label_num.text() == "1":
            self.ui_custom.slider_temp.setValue(int(contents["config1_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config1_amount"]))
        elif self.ui_custom.label_num.text() == "2":
            self.ui_custom.slider_temp.setValue(int(contents["config2_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config2_amount"]))
        elif self.ui_custom.label_num.text() == "3":
            self.ui_custom.slider_temp.setValue(int(contents["config3_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config3_amount"]))
        elif self.ui_custom.label_num.text() == "4":
            self.ui_custom.slider_temp.setValue(int(contents["config4_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config4_amount"]))
        elif self.ui_custom.label_num.text() == "5":
            self.ui_custom.slider_temp.setValue(int(contents["config5_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config5_amount"]))
        elif self.ui_custom.label_num.text() == "6":
            self.ui_custom.slider_temp.setValue(int(contents["config6_temp"]))
            self.ui_custom.slider_amount.setValue(int(contents["config6_amount"]))

        self.showMsg_temp()
        self.showMsg_amount()


        for i in range(self.num-1 , 6):
            self.labels_splash[i].lower()
            self.labels_temp[i].lower()
            self.labels_amount[i].lower()
            self.labels_plus[i].lower()
            self.flag[i] = 0

        for i in range(self.num , 6):
            self.buttons[i].setEnabled(False)

        # for i in range(a , 5):

        self.num = self.num - 1


        self.labels_plus[self.num].raise_()
        self.buttons[self.num].raise_()


        with open("config.json", "r") as f:
            content = json.load(f)
        content["config_num"] = self.num
        with open("config.json", "w") as f:
            json.dump(content, f,indent=2)





        # 清除最后一个按钮的文本
        #
        # if self.ui_custom.label_6_temp.text() != "":
        #     self.ui_custom.label_plus_6.raise_()
        #     self.ui_custom.label_splash_6.lower()
        #     self.ui_custom.label_6_temp.lower()
        #     self.ui_custom.label_6_amount.lower()
        #     self.ui_custom.btn_6.raise_()
        #     #self.labels_temp[-1].setText("")

        # if self.ui_custom.label_num.text()=='1':






if __name__ == "__main__":

    App = QApplication(sys.argv)
    main = Window_main()
    main.show()
    # 获取当前进程ID
    pid = QApplication.instance().applicationPid()
    process = psutil.Process(pid)

    # 获取进程的内存信息
    memory_info = process.memory_info()
    memory_usage = memory_info.rss
    memory_mb = memory_usage / (1024 * 1024)

    # 输出内存使用量
    print(f"Memory usage: {memory_mb} MB")

    sys.exit(App.exec_())

