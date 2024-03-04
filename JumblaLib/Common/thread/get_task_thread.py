# coding: utf-8

from PyQt5.QtCore import QThread, pyqtSignal

from JumblaLib.Common.cgtwapi import *


class GetTasksThread(QThread):
    getTaskFinished = pyqtSignal(list)

    def __init__(self, project_db):
        super().__init__()
        self.project_db = project_db

    def run(self):
        task_list = get_my_task(self.project_db)
        self.getTaskFinished.emit(task_list)
