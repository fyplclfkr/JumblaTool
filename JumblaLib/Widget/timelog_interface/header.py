# -*- coding: utf-8 -*-
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QFrame, QVBoxLayout

from qfluentwidgets import PrimaryToolButton
from qfluentwidgets import FluentIcon as FIF


class Header(QWidget):

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.frame = QFrame()
        self.avatar_label = QLabel()
        self.user_name_label = QLabel('')

        self.clockInLabel = QLabel('上班时间:')
        self.clockInTimeLabel = QLabel('未打卡')

        self.lastLabel = QLabel('最后打卡时间:')
        self.lastTimeLabel = QLabel('未提交')

        self.todayLabel = QLabel('今日工时：')
        self.todayTimeLabel = QLabel('0')

        self.refresh_button = PrimaryToolButton(FIF.SYNC)
        self.spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._init_layout()
        self._init_style()

    def _init_style(self):
        self.avatar_label.setStyleSheet('background: transparent;')

        self.user_name_label.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        self.user_name_label.setStyleSheet('background: transparent;')

        self.clockInLabel.setStyleSheet('background: transparent;'
                                        'font-family: Microsoft YaHei;'
                                        'font-size: 12pt;'
                                        'padding-left: 20;'
                                        )
        self.clockInTimeLabel.setStyleSheet('background: transparent;'
                                            'font-family: Microsoft YaHei;'
                                            'font-size: 10pt;'
                                            'color: red;'
                                            )

        self.lastLabel.setStyleSheet('background: transparent;'
                                     'font-family: Microsoft YaHei;'
                                     'font-size: 12pt;'
                                     'padding-left: 20;'
                                     )
        self.lastTimeLabel.setStyleSheet('background: transparent;'
                                         'font-family: Microsoft YaHei;'
                                         'font-size: 10pt;'
                                         'color: red;'
                                         )

        self.todayLabel.setStyleSheet('background: transparent;'
                                     'font-family: Microsoft YaHei;'
                                     'font-size: 12pt;'
                                     'padding-left: 20;'
                                     )
        self.todayTimeLabel.setStyleSheet('background: transparent;'
                                         'font-family: Microsoft YaHei;'
                                         'font-size: 10pt;'
                                         'color: red;'
                                         )

        self.frame.setStyleSheet("QFrame{background: rgba(51, 51, 51, 0.05)}")
        self.frame.setMinimumHeight(60)

    def _init_layout(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.frame)

        self.frame_layout = QHBoxLayout(self.frame)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(24, 6, 24, 6)

        self.frame_layout.addWidget(self.avatar_label)

        self.frame_layout.addWidget(self.user_name_label)

        self.frame_layout.addWidget(self.clockInLabel)
        self.frame_layout.addWidget(self.clockInTimeLabel)

        self.frame_layout.addWidget(self.lastLabel)
        self.frame_layout.addWidget(self.lastTimeLabel)

        self.frame_layout.addWidget(self.todayLabel)
        self.frame_layout.addWidget(self.todayTimeLabel)

        self.frame_layout.addItem(self.spacer)
        self.frame_layout.addWidget(self.refresh_button)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Header()
    w.show()
    app.exec_()
