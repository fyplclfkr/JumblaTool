# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget


class ProjectTaskList(QWidget):

    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        
        self._init_layout()
        self._init_style()
        self._connectSignalToSlot()
        
    def _init_style(self):
        pass    

    def _init_layout(self):
        pass

    def _connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = ProjectTaskList()
    w.show()
    app.exec_()