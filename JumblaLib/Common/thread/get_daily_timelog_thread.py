# coding: utf-8
from PyQt5.QtCore import QThread, pyqtSignal

from JumblaLib.Common.cgtwapi import *


class GetDailyTimelogThread(QThread):
    getTimelogFinished = pyqtSignal(list)

    def __init__(self, _data):
        super().__init__()
        self._data = _data

    def run(self):
        _daily_timelog = get_daily_timelog(self._data)
        self.getTimelogFinished.emit(_daily_timelog)
