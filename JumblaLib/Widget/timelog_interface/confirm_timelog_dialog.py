# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QFrame
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, StrongBodyLabel


class ConfirmTimelogDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, projectName: str, taskName: str, startTime: str, endTime: str, useTime: str, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('确认打卡内容')
        self.bodyFrame = QFrame()

        self.bodyLayout = QGridLayout(self.bodyFrame)

        self.projectLabel = StrongBodyLabel('项目名称：')
        self.projectNameLabel = BodyLabel(projectName)

        self.taskLabel = StrongBodyLabel('任务名称：')
        self.taskNameLabel = BodyLabel(taskName)

        self.startLabel = StrongBodyLabel('开始时间：')
        self.startTimeLabel = BodyLabel(startTime)

        self.endLabel = StrongBodyLabel('结束时间：')
        self.endTimeLabel = BodyLabel(endTime)

        self.timeLabel = StrongBodyLabel('本次用时：')
        self.useTimeLabel = BodyLabel(useTime)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.viewLayout.addWidget(self.bodyFrame)

        self.bodyLayout.addWidget(self.projectLabel, 0, 0)
        self.bodyLayout.addWidget(self.projectNameLabel, 0, 1)
        self.bodyLayout.addWidget(self.taskLabel, 1, 0)
        self.bodyLayout.addWidget(self.taskNameLabel, 1, 1)
        self.bodyLayout.addWidget(self.startLabel, 2, 0)
        self.bodyLayout.addWidget(self.startTimeLabel, 2, 1)
        self.bodyLayout.addWidget(self.endLabel, 3, 0)
        self.bodyLayout.addWidget(self.endTimeLabel, 3, 1)
        self.bodyLayout.addWidget(self.timeLabel, 4, 0)
        self.bodyLayout.addWidget(self.useTimeLabel, 4, 1)

        # 设置样式
        # self.titleLabel.setStyleSheet('background: blue')
        # self.bodyFrame.setStyleSheet('background: rgba(51, 51, 51, 0.03)')
        # self.projectLabel.setStyleSheet('background: transparent')
        # self.projectNameLabel.setStyleSheet('background: transparent')
        # self.taskLabel.setStyleSheet('background: transparent')
        # self.taskNameLabel.setStyleSheet('background: transparent')
        # self.startLabel.setStyleSheet('background: transparent')
        # self.startTimeLabel.setStyleSheet('background: transparent')
        # self.endLabel.setStyleSheet('background: transparent')
        # self.endTimeLabel.setStyleSheet('background: transparent')
        # self.timeLabel.setStyleSheet('background: transparent')
        # self.useTimeLabel.setStyleSheet('background: transparent')

        # 设置对话框的最小宽度
        # self.widget.setMinimumWidth(350)
