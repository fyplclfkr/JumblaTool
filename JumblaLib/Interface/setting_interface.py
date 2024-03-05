# -*- coding: utf-8 -*-
import sys
import json
import subprocess
import os
import shutil
import tempfile
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QUrl

from JumblaLib.Common.setting import VERSION
from JumblaLib.Common.jumblaLib import update, get_remote_version
from JumblaLib.Widget import UpdateDialog


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.toolsGroup = SettingCardGroup('工具', self.scrollWidget)
        self.attendanceCard = PrimaryPushSettingCard(
            '选择文件',
            FIF.FOLDER,
            '上传打卡记录',
            '把execl格式的打卡记录转换成json上传到服务器',
            self.toolsGroup
        )
        self.toolsGroup.addSettingCard(self.attendanceCard)

        self.aboutGroup = SettingCardGroup('关于', self.scrollWidget)
        self.aboutCard = PrimaryPushSettingCard(
            '检查更新',
            FIF.INFO,
            '关于',
            '当前版本' + " " + VERSION,
            self.aboutGroup
        )
        self.aboutGroup.addSettingCard(self.aboutCard)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.toolsGroup)
        self.expandLayout.addWidget(self.aboutGroup)

        self.initWidget()
        self.connectSignalToSlot()

    def initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        self.setStyleSheet("#scrollWidget{background-color: transparent;}"
                           "QScrollArea{background-color: transparent;border: none;}")

    def connectSignalToSlot(self):
        self.aboutCard.clicked.connect(self.onAboutCardClicked)
        self.attendanceCard.clicked.connect(self.excel_to_json)

    def excel_to_json(self):
        initial_directory = QUrl.fromLocalFile(os.getcwd())
        file_urls, _ = QFileDialog.getOpenFileUrls(self,
                                                   '选择文件',
                                                   initial_directory,
                                                   'ExcelFiles(*.xls *.xlsx)')
        if file_urls:
            for url in file_urls:
                print(url.toLocalFile())

    def onAboutCardClicked(self):
        if VERSION != get_remote_version():
            w = UpdateDialog(self.window())
            if w.exec_():
                update()
            else:
                InfoBar.info(
                    title='取消更新',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self.window()
                )
        else:
            InfoBar.info(
                title='没有更新',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
