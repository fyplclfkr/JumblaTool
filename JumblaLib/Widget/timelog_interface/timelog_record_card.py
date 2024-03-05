# -*- coding: utf-8 -*-
# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget


class TimelogRecordCard(QWidget):

    def __init__(self):
        super().__init__()

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        pass

    def __connectSignalToSlot(self):
        pass
        


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = TimelogRecordCard()
    w.show()
    app.exec_()