# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, NavigationItemPosition, qconfig, InfoBarPosition, InfoBar
from qfluentwidgets import FluentIcon as FIF

from JumblaLib.Common.jumblaLib import get_remote_version, update
from JumblaLib.Interface.timelog_interface import TimeLogInterface
from JumblaLib.Interface.setting_interface import SettingInterface
from JumblaLib.Widget import UpdateDialog
from JumblaLib.Common.setting import VERSION, DEBUG
from JumblaLib.Resources import resource


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_window()

        # 定时更新检测
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_update)
        self.timer.start(1800000)

        self.timelogPage = TimeLogInterface()
        self.settingPage = SettingInterface()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.timelogPage, FIF.HISTORY, '工时', pos)
        self.addSubInterface(self.settingPage, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)

    def init_window(self):
        self.setWindowIcon(QIcon(':jumbla/images/logo.png'))
        self.setWindowTitle('嘉伯乐动画')
        self.resize(1024, 768)
        self.navigationInterface.setExpandWidth(128)

        # self.splashScreen = SplashScreen(self.windowIcon(), self)
        # self.splashScreen.setIconSize(QSize(106, 106))
        # self.splashScreen.raise_()

        # 设置主题色
        color = QColor('#2875E8')
        qconfig.set(qconfig.themeColor, color)
        QApplication.processEvents()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def check_update(self):
        if DEBUG:
            return
        if VERSION != get_remote_version():
            print('有更新啦！！！')
            w = UpdateDialog(self.window())
            if w.exec_():
                update()
            else:
                return
        else:
            return
