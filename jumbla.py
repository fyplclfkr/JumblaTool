# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication

from JumblaLib.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    w = MainWindow()
    w.show()
    app.exec_()