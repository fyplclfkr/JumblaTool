# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QApplication, QSizePolicy


class TaskInfoCard(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(12)
        self.setLayout(self.layout)

        self.label1 = QLabel('项目名称')
        self.label1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.label11 = QLabel('|')
        self.label11.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.project_name_label = QLabel(' ')

        self.label2 = QLabel('任务名称')
        self.label22 = QLabel('|')
        self.task_name_label = QLabel(' ')

        self.label3 = QLabel('任务状态')
        self.label33 = QLabel('|')
        self.task_statu_label = QLabel(' ')

        self.label4 = QLabel('预计工时')
        self.label44 = QLabel('|')
        self.expected_time_label = QLabel(' ')

        self.label5 = QLabel('已用工时')
        self.label55 = QLabel('|')
        self.use_time_label = QLabel(' ')

        self.label6 = QLabel('剩余工时')
        self.label66 = QLabel('|')
        self.residue_time_label = QLabel(' ')

        self.layout.addWidget(self.label1, 0, 0)
        self.layout.addWidget(self.label11, 0, 1)
        self.layout.addWidget(self.project_name_label, 0, 2)

        self.layout.addWidget(self.label2, 1, 0)
        self.layout.addWidget(self.label22, 1, 1)
        self.layout.addWidget(self.task_name_label, 1, 2)

        self.layout.addWidget(self.label3, 2, 0)
        self.layout.addWidget(self.label33, 2, 1)
        self.layout.addWidget(self.task_statu_label, 2, 2)

        self.layout.addWidget(self.label4, 3, 0)
        self.layout.addWidget(self.label44, 3, 1)
        self.layout.addWidget(self.expected_time_label, 3, 2)

        self.layout.addWidget(self.label5, 4, 0)
        self.layout.addWidget(self.label55, 4, 1)
        self.layout.addWidget(self.use_time_label, 4, 2)

        self.layout.addWidget(self.label6, 5, 0)
        self.layout.addWidget(self.label66, 5, 1)
        self.layout.addWidget(self.residue_time_label, 5, 2)

        self._init_style()

    def _init_style(self):
        style = """
        QLabel {
            color: rgba(51, 51, 51, 0.5);
        }
        """
        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskInfoCard()
    window.show()
    sys.exit(app.exec_())
