# -*- coding: utf-8 -*-
from datetime import date, datetime
from importlib import reload
from PyQt5.QtCore import Qt, QTime, QDateTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QSpacerItem, QSizePolicy, QFrame
from qfluentwidgets import ListWidget, InfoBar, InfoBarPosition, setStyleSheet, setCustomStyleSheet, MessageBox

from JumblaLib.Common.thread import GetProjectThread, GetTasksThread
from JumblaLib.Widget.timelog_interface import TaskInfoCard, SubTimelogCard, Header, ConfirmTimelogDialog
from JumblaLib.Common import cgtwapi
from JumblaLib.Common.jumblaLib import count_working_hours


class TimeLogInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.get_project_thread = GetProjectThread()

        self._init_ui()

        self.set_data()

    def _init_ui(self):
        self.setObjectName('TimeLogPage')

        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.VLine)

        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.VLine)

        # HEADER
        self.header = Header()
        # BODY-LEFT
        self.chose_task_Label = QLabel('选择打卡任务')
        self.project_Label = QLabel('     项目列表')
        self.project_Label.setMinimumHeight(30)
        self.project_ListWidget = ListWidget()
        self.task_Label = QLabel('     任务列表')
        self.task_Label.setMinimumHeight(30)
        self.task_ListWidget = ListWidget()
        # BODY-MIDDLE
        self.task_info_label = QLabel('当前任务信息')
        self.task_info_card = TaskInfoCard()

        self.chose_time_label = QLabel('选择打卡时间')
        self.chose_time_card = SubTimelogCard()

        self.body_Spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self._init_layout()
        self._init_style()
        self._connect_signal()

    def _init_layout(self):
        # HEADER

        # BODY
        self.project_Layout = QVBoxLayout()
        self.project_Layout.setSpacing(0)
        self.project_Layout.addWidget(self.project_Label)
        self.project_Layout.addWidget(self.project_ListWidget)

        self.task_Layout = QVBoxLayout()
        self.task_Layout.setSpacing(0)
        self.task_Layout.addWidget(self.task_Label)
        self.task_Layout.addWidget(self.task_ListWidget)

        self.project_task_Layout = QHBoxLayout()
        self.project_task_Layout.setSpacing(1)
        self.project_task_Layout.addLayout(self.project_Layout)
        self.project_task_Layout.addLayout(self.task_Layout)

        self.body_left_Layout = QVBoxLayout()
        self.body_left_Layout.setSpacing(24)
        self.body_left_Layout.setContentsMargins(24, 24, 24, 24)
        self.body_left_Layout.addWidget(self.chose_task_Label)
        self.body_left_Layout.addLayout(self.project_task_Layout)

        self.body_middle_Layout = QVBoxLayout()
        self.body_middle_Layout.setSpacing(24)
        self.body_middle_Layout.setContentsMargins(24, 24, 24, 24)
        self.body_middle_Layout.addWidget(self.task_info_label)
        self.body_middle_Layout.addWidget(self.task_info_card)
        self.body_middle_Layout.addWidget(self.chose_time_label)
        self.body_middle_Layout.addWidget(self.chose_time_card)

        self.body_Layout = QHBoxLayout()
        self.body_Layout.addLayout(self.body_left_Layout)
        self.body_Layout.addWidget(self.line1)
        self.body_Layout.addLayout(self.body_middle_Layout)
        self.body_Layout.addWidget(self.line2)
        self.body_Layout.addItem(self.body_Spacer)

        # MAIN
        self.main_Layout = QVBoxLayout(self)
        self.main_Layout.setSpacing(0)
        self.main_Layout.setContentsMargins(0, 0, 0, 0)
        self.main_Layout.addWidget(self.header)
        self.main_Layout.addLayout(self.body_Layout)

    def _connect_signal(self):
        self.task_ListWidget.itemClicked.connect(self.set_task_info)
        self.project_ListWidget.itemClicked.connect(self.get_task_thread)
        self.header.refresh_button.clicked.connect(self.set_data)
        self.chose_time_card.submit_button.clicked.connect(self.on_submit_button_clicked)

    def _init_style(self):
        self.chose_task_Label.setStyleSheet('font-family: Microsoft YaHei;'
                                            'font-size: 14pt;'
                                            'font-weight: bold;')

        self.task_info_label.setStyleSheet('font-family: Microsoft YaHei;'
                                           'font-size: 14pt;'
                                           'font-weight: bold;')

        self.chose_time_label.setStyleSheet('font-family: Microsoft YaHei;'
                                            'font-size: 14pt;'
                                            'font-weight: bold;')

        self.project_Label.setStyleSheet('background: rgba(51, 51, 51, 0.1);'
                                         'border-top-left-radius: 5px;'
                                         'font-family: Microsoft YaHei;'
                                         'font-size: 9pt;'
                                         'font-weight: bold;')

        self.task_Label.setStyleSheet('background: rgba(51, 51, 51, 0.1);'
                                      'border-top-right-radius:5px;'
                                      'font-family: Microsoft YaHei;'
                                      'font-size: 9pt;'
                                      'font-weight: bold;')
        setCustomStyleSheet(self.project_ListWidget, "ListWidget{background: rgba(51, 51, 51, 0.05);"
                                                     "border-bottom-left-radius:5px}",
                            "ListWidget{background: rgba(51, 51, 51, 0.05);"
                            "border-bottom-left-radius:5px}")
        setCustomStyleSheet(self.task_ListWidget, "ListWidget{background: rgba(51, 51, 51, 0.05);"
                                                  "border-bottom-right-radius:5px}",
                            "ListWidget{background: rgba(51, 51, 51, 0.05);"
                            "border-bottom-right-radius:5px}")
        self.line1.setStyleSheet('color:rgba(51, 51, 51, 0.1)')
        self.line2.setStyleSheet('color:rgba(51, 51, 51, 0.1)')

    def set_project_list(self):
        self.get_project_thread.getProjectFinished.connect(self.on_get_project_finished)
        self.get_project_thread.start()

    def on_get_project_finished(self, project_list):
        self.project_ListWidget.clear()
        if not project_list:
            InfoBar.error(
                title='请先登录CGTeamWork  登陆后点击刷新',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
        for project in project_list:
            list_item = QListWidgetItem(project['project.full_name'])
            list_item.setData(Qt.UserRole, project)
            self.project_ListWidget.addItem(list_item)

    # def get_project_thread(self):
    #     self.get_project_thread = GetProjectThread()
    #     self.get_project_thread.getProjectFinished.connect(self.get_project_finished)
    #     self.get_project_thread.start()

    def get_task_finished(self, task_list):
        self.task_ListWidget.clear()
        for task in task_list:
            list_item = QListWidgetItem(task['task.url'])
            list_item.setData(Qt.UserRole, task)
            self.task_ListWidget.addItem(list_item)

    def get_task_thread(self):
        # 清除当前任务信息
        self.on_project_clicked()
        # 获取任务列表
        try:
            _db = self.project_ListWidget.currentItem().data(Qt.UserRole)['project.database']
        except:
            print('没有数据库')
            return
        self.get_tasks_thread = GetTasksThread(_db)
        self.get_tasks_thread.getTaskFinished.connect(self.get_task_finished)
        self.get_tasks_thread.start()

    def set_task_info(self):
        if self.task_ListWidget.currentItem().data(Qt.UserRole)['task.expected_time']:
            _expectedly = float(self.task_ListWidget.currentItem().data(Qt.UserRole)['task.expected_time'])
        else:
            _expectedly = 0
        if self.task_ListWidget.currentItem().data(Qt.UserRole)['task.total_use_time']:
            _usetime = float(self.task_ListWidget.currentItem().data(Qt.UserRole)['task.total_use_time'])
        else:
            _usetime = 0
        _residue = _expectedly - _usetime
        if _residue < 0:
            self.task_info_card.residue_time_label.setStyleSheet('color: red;')
        else:
            self.task_info_card.residue_time_label.setStyleSheet('color: rgba(51, 51, 51, 0.5);')

        self.task_info_card.project_name_label.setText(self.project_ListWidget.currentItem().text())
        self.task_info_card.task_name_label.setText(self.task_ListWidget.currentItem().data(Qt.UserRole)['task.url'])
        self.task_info_card.task_statu_label.setText(
            self.task_ListWidget.currentItem().data(Qt.UserRole)['task.status'])
        self.task_info_card.expected_time_label.setText(str(_expectedly))
        self.task_info_card.use_time_label.setText(str(_usetime))
        self.task_info_card.residue_time_label.setText(str(_residue))

    def set_time_picker(self):
        # 设置时间选择器
        _clock_in_time = cgtwapi.get_clock_in_time(cgtwapi.ACCOUNT_LIST.get('account.name'))  # 获取当天打卡时间
        _daily_timelog = cgtwapi.get_daily_timelog(date.today().strftime("%Y-%m-%d"))  # 当日工时记录
        print(f'上班时间: {_clock_in_time} {_daily_timelog}')
        # 上班打卡，未提交当日工时，开始时间设置成当天打卡时间
        if _clock_in_time and not _daily_timelog:
            self.header.clockInTimeLabel.setText(_clock_in_time)
            self.chose_time_card.start_time_picker.setTime(QTime.fromString(_clock_in_time, 'hh:mm'))
            self.set_chose_time_card_statu(True)
            self.chose_time_card.submit_button.setToolTip('')
            self.chose_time_card.end_time_picker.setTime(self.chose_time_card.start_time_picker.getTime())
        # 当日已提交过工时，开始时间设置成上一个工时结束时间
        elif _clock_in_time and _daily_timelog:
            # 获取最后一个打卡记录的结束时间字符串
            _end_time_str = _daily_timelog[-1]['end_time']
            # 将字符串转换为QDateTime对象
            _end_time_dt = QDateTime.fromString(_end_time_str, 'yyyy-MM-dd HH:mm:ss')
            # 提取QTime只保留小时分钟
            _time_only = _end_time_dt.time()
            _end_time = QTime(_time_only.hour(), _time_only.minute())
            self.header.clockInTimeLabel.setText(_clock_in_time)
            self.header.lastTimeLabel.setText(_end_time.toString('HH:mm'))
            self.chose_time_card.start_time_picker.setTime(_end_time)
            self.set_chose_time_card_statu(True)
            self.chose_time_card.submit_button.setToolTip('')
            self.chose_time_card.end_time_picker.setTime(self.chose_time_card.start_time_picker.getTime())
            _today_use_time = 0
            # 获取当天总工时
            for item in _daily_timelog:
                _today_use_time += int(item['use_time'])
            self.header.todayTimeLabel.setText("{:.1f}".format(_today_use_time / 3600))
        else:
            self.header.clockInTimeLabel.setText('未打卡')
            self.set_chose_time_card_statu(False)
            self.chose_time_card.submit_button.setToolTip('无法提交请刷新')
            InfoBar.error(
                title='未打卡或打卡记录未上传，请打卡后联系IT',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )

    def set_time_slider(self):
        _start = self.chose_time_card.start_time_picker.getTime()
        _end = self.chose_time_card.end_time_picker.getTime()
        self.chose_time_card.time_slider.setMinimum(_start.hour() * 60 + _start.minute())
        self.chose_time_card.time_slider.setMaximum(1439)
        self.chose_time_card.time_slider.setValue(_end.hour() * 60 + _end.minute())

    def set_chose_time_card_statu(self, statu):
        if statu:
            self.chose_time_card.submit_button.setEnabled(True)
            self.chose_time_card.now_button.setEnabled(True)
            self.chose_time_card.add_30min_button.setEnabled(True)
            self.chose_time_card.add_1H_button.setEnabled(True)
            self.chose_time_card.add_2H_button.setEnabled(True)
            self.chose_time_card.time_slider.setEnabled(True)
        elif not statu:
            self.chose_time_card.submit_button.setEnabled(False)
            self.chose_time_card.now_button.setEnabled(False)
            self.chose_time_card.add_30min_button.setEnabled(False)
            self.chose_time_card.add_1H_button.setEnabled(False)
            self.chose_time_card.add_2H_button.setEnabled(False)
            self.chose_time_card.time_slider.setEnabled(False)

    def on_project_clicked(self):
        # 清除任务信息
        self.task_info_card.project_name_label.setText(' ')
        self.task_info_card.task_name_label.setText(' ')
        self.task_info_card.task_statu_label.setText(' ')
        self.task_info_card.expected_time_label.setText(' ')
        self.task_info_card.use_time_label.setText(' ')
        self.task_info_card.residue_time_label.setText(' ')

    def on_submit_button_clicked(self):
        _last_time = QTime()
        _clock_in_time = QTime.fromString(self.header.clockInTimeLabel.text(), 'HH:mm')
        if self.header.lastTimeLabel.text() != '未提交':
            _last_time = QTime.fromString(self.header.lastTimeLabel.text(), 'HH:mm')
        _start = self.chose_time_card.start_time_picker.getTime()
        _end = self.chose_time_card.end_time_picker.getTime()
        _now = QDateTime.currentDateTime().time()
        print(_start, _end, _last_time)
        if _end > _now:
            InfoBar.error(
                title='结束时间未到，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start >= _end:
            InfoBar.error(
                title='结束时间小于等于开始时间，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start < _clock_in_time:
            InfoBar.error(
                title='开始时间小于上班时间，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start < _last_time:
            InfoBar.error(
                title='开始时间小于最后打卡时间，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start >= QTime(12, 0) and _end <= QTime(13, 0):
            InfoBar.error(
                title='休息时间禁止提交工时',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start >= QTime(18, 30) and _end <= QTime(19, 0):
            InfoBar.error(
                title='休息时间禁止提交工时',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        try:
            _db = self.project_ListWidget.currentItem().data(Qt.UserRole)['project.database']
        except:
            _db = ''
        try:
            _module = self.task_ListWidget.currentItem().data(Qt.UserRole)['task.module']
        except:
            _module = ''
        _module_type = 'task'
        try:
            _link_id = self.task_ListWidget.currentItem().data(Qt.UserRole)['task.id']
        except:
            _link_id = ''
        # 计算本次工时
        # seconds_diff = _start.secsTo(_end)
        # time_diff = QTime(0, 0).addSecs(seconds_diff)
        # formatted_time_diff = time_diff.toString('hh:mm')
        formatted_time_diff = count_working_hours(_clock_in_time, _last_time, _start, _end)
        # 格式化起始时间
        _start_time = datetime.combine(datetime.now(), _start.toPyTime()).strftime("%Y-%m-%d %H:%M:%S")
        _end_time = datetime.combine(datetime.now(), _end.toPyTime()).strftime("%Y-%m-%d %H:%M:%S")
        # _text = f'start_time: {_start_time}\nend_time: {_end_time}'
        _dict = {'db': _db, 'link_id': _link_id,
                 'module': _module, 'module_type': _module_type,
                 'use_time': formatted_time_diff,
                 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'start_time': _start_time, 'end_time': _end_time, 'text': '项目工时'}
        if any(value == '' for value in _dict.values()):
            InfoBar.warning(
                title='请先选择项目|任务|打卡时间',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        else:
            _projectName = self.project_ListWidget.currentItem().data(Qt.UserRole)['project.full_name']
            _taskName = self.task_ListWidget.currentItem().data(Qt.UserRole)['task.url']
            w = ConfirmTimelogDialog(_projectName, _taskName, _start_time, _end_time, formatted_time_diff,
                                     self.window())
            if w.exec_():
                # 提交工时
                _dict['text'] = w.textLineEdit.toPlainText()
                print(cgtwapi.sub_time_log(_dict))
                InfoBar.success(
                    title='工时提交成功',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                # 刷新任务信息，总工时
                task = cgtwapi.reload_task_info(_db, _module, _link_id.split())[0]
                print(task)
                if task['task.expected_time']:
                    _expectedtime = float(task['task.expected_time'])
                else:
                    _expectedtime = 0
                if task['task.total_use_time']:
                    _usetime = float(task['task.total_use_time'])
                else:
                    _usetime = 0

                _residuetime = _expectedtime - _usetime
                if _residuetime < 0:
                    self.task_info_card.residue_time_label.setStyleSheet('color: red;')
                else:
                    self.task_info_card.residue_time_label.setStyleSheet('color: rgba(51, 51, 51, 0.5);')
                self.task_info_card.project_name_label.setText(self.project_ListWidget.currentItem().text())
                self.task_info_card.task_name_label.setText(self.task_ListWidget.currentItem().data(Qt.UserRole)['task.url'])
                self.task_info_card.task_statu_label.setText(self.task_ListWidget.currentItem().data(Qt.UserRole)['task.status'])
                self.task_info_card.expected_time_label.setText(str(_expectedtime))
                self.task_info_card.use_time_label.setText(str(_usetime))
                self.task_info_card.residue_time_label.setText(str(_residuetime))
                self.task_ListWidget.currentItem().setData(Qt.UserRole, task)
                self.set_time_picker()
                self.set_time_slider()
            else:
                # print(w.textLineEdit.toPlainText())
                InfoBar.info(
                    title='取消提交',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

    def set_header(self):
        # 设置头像
        # self.load_avatar = ImageLoader()
        # self.load_avatar.image_loaded.connect(lambda pixmap: self.header.avatar_label.setPixmap(pixmap))
        # self.load_avatar.loadImage(cgtwapi.AVATAR_URL)
        # 设置姓名
        self.header.user_name_label.setText(cgtwapi.ACCOUNT_LIST.get('account.name'))

    def set_data(self):
        reload(cgtwapi)
        self.project_ListWidget.clear()
        self.task_ListWidget.clear()
        self.on_project_clicked()
        self.set_project_list()
        self.set_time_picker()
        self.set_time_slider()
        self.set_header()
