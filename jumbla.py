# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from JumblaLib.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
