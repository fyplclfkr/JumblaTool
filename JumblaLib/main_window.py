# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QSplashScreen
from qfluentwidgets import FluentWindow, NavigationItemPosition, SplashScreen, qconfig
from qfluentwidgets import FluentIcon as FIF

from JumblaLib.Interface.timelog_interface import TimeLogInterface


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_window()

        self.timelogPage = TimeLogInterface()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.timelogPage, FIF.HISTORY, '工时', pos)

    def init_window(self):
        self.setWindowTitle('嘉伯乐动画')
        self.resize(1024, 768)

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
