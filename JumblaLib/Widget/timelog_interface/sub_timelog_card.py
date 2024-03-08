# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QTime, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PrimaryPushButton, TitleLabel, TimePicker, SubtitleLabel, BodyLabel, Slider


class SubTimelogCard(QWidget):

    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):

        self.start_time_label = BodyLabel()
        self.start_time_label.setText('开始时间')
        self.start_time_picker = TimePicker()
        self.start_time_picker.setEnabled(False)

        self.end_time_label = BodyLabel()
        self.end_time_label.setText('结束时间')
        self.end_time_picker = TimePicker()
        # self.end_time_picker.setEnabled(False)

        self.now_button = PrimaryPushButton('NOW')
        self.add_30min_button = PrimaryPushButton('+30M')
        self.add_1H_button = PrimaryPushButton('+1H')
        self.add_2H_button = PrimaryPushButton('+2H')

        self.time_slider = Slider(Qt.Horizontal)

        self.submit_button = PrimaryPushButton()
        self.submit_button.setText('提交工时')
        self.submit_button.setMinimumHeight(40)

        self.spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self._init_layout()
        self._init_style()
        self._connect_slot()

    def _init_style(self):
        pass

    def _init_layout(self):
        self.layout = QGridLayout(self)
        self.layout.setVerticalSpacing(12)
        self.layout.setHorizontalSpacing(12)

        self.layout.addWidget(self.start_time_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.start_time_picker, self.layout.rowCount()-1, 1, 1, self.layout.columnCount())

        self.layout.addWidget(self.end_time_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.end_time_picker, self.layout.rowCount()-1, 1)

        self.add_button_layout = QHBoxLayout()
        self.add_button_layout.addWidget(self.now_button)
        self.add_button_layout.addWidget(self.add_30min_button)
        self.add_button_layout.addWidget(self.add_1H_button)
        self.add_button_layout.addWidget(self.add_2H_button)
        self.layout.addLayout(self.add_button_layout, self.layout.rowCount(), 0, 1, self.layout.columnCount())

        self.layout.addWidget(self.time_slider, self.layout.rowCount(), 0, 1, self.layout.columnCount())

        self.layout.addWidget(self.submit_button, self.layout.rowCount(), 0, 1, self.layout.columnCount())
        self.layout.addItem(self.spacer, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def _connect_slot(self):
        self.now_button.clicked.connect(self.on_now_button_clicked)
        self.add_30min_button.clicked.connect(self.on_add_30min_button_clicked)
        self.add_1H_button.clicked.connect(self.on_add_1H_button_clicked)
        self.add_2H_button.clicked.connect(self.on_add_2H_button_clicked)
        self.time_slider.valueChanged.connect(self.on_slider_changed)
        self.end_time_picker.timeChanged.connect(self.on_end_time_changed)

    def on_now_button_clicked(self):
        _time = QTime(QTime.currentTime().hour(), QTime.currentTime().minute())
        self.end_time_picker.setTime(_time)
        self.time_slider.setValue(_time.hour() * 60 + _time.minute())

    def on_add_30min_button_clicked(self):
        _time = self.end_time_picker.getTime()
        print('+30M')
        self.end_time_picker.setTime(_time.addSecs(1800))
        self.time_slider.setValue(self.time_slider.value() + 30)

    def on_add_1H_button_clicked(self):
        _time = self.end_time_picker.getTime()
        print('+1H')
        self.end_time_picker.setTime(_time.addSecs(3600))
        self.time_slider.setValue(self.time_slider.value() + 60)

    def on_add_2H_button_clicked(self):
        _time = self.end_time_picker.getTime()
        print('+2H')
        self.end_time_picker.setTime(_time.addSecs(7200))
        self.time_slider.setValue(self.time_slider.value() + 120)

    def on_slider_changed(self, value):
        total_minutes = value
        hours = total_minutes // 60
        minutes = total_minutes % 60
        time = QTime(hours, minutes)
        self.end_time_picker.setTime(time)

    def on_end_time_changed(self, time: QTime):
        total_minutes = time.hour() * 60 + time.minute()
        self.time_slider.setValue(total_minutes)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = SubTimelogCard()
    w.show()
    app.exec_()
