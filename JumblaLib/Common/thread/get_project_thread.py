# coding: utf-8

from PyQt5.QtCore import QThread, pyqtSignal

from JumblaLib.Common.cgtwapi import *


class GetProjectThread(QThread):
    getProjectFinished = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        project_list = []
        project_list = get_project_list()
        self.getProjectFinished.emit(project_list)
