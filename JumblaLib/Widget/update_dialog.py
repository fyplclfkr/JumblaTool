# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QFrame, QVBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel, StrongBodyLabel
from JumblaLib.Common.jumblaLib import get_remote_version, get_release_notes


class UpdateDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        remote_version = get_remote_version()
        release_notes = get_release_notes()
        self.titleLabel = SubtitleLabel('发现新版本')

        self.bodyFrame = QFrame()
        self.bodyLayout = QVBoxLayout(self.bodyFrame)

        self.remoteVersionLabel = StrongBodyLabel()
        self.remoteVersionLabel.setText(f'Version:{remote_version}')

        self.releaseNotesLabel = BodyLabel()
        self.releaseNotesLabel.setText(release_notes)
        self.releaseNotesLabel.setWordWrap(True)

        self.yesButton.setText('安装更新')

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.viewLayout.addWidget(self.bodyFrame)

        self.bodyLayout.addWidget(self.remoteVersionLabel)
        self.bodyLayout.addWidget(self.releaseNotesLabel)

        # 设置样式

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)
