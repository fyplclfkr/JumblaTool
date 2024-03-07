# -*- coding: utf-8 -*-
import json
import shutil
import subprocess

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QApplication

from JumblaLib.Common.setting import VERSION


def calculateWorkingTime(start_time: QTime, end_time: QTime):
    # 计算时间差
    totalSeconds = start_time.secsTo(end_time)

    # 开始时间12点前，结束时间13点后午休扣除1小时
    if start_time.hour() < 12 and end_time.hour() >= 13:
        if end_time.hour() != 13 or end_time.minute() != 0:
            totalSeconds -= 3600
    # 开始时间12点后13点前
    elif start_time.hour() == 12 and start_time.minute() >= 0 and end_time.hour() == 13:
        minutesRemove = (60 - start_time.minute()) + end_time.minute()
        totalSeconds -= minutesRemove * 60

    totalMinutes = totalSeconds // 60
    return totalMinutes


def count_working_hours(clock_in_time: QTime, last_time: QTime, start_time: QTime, end_time: QTime):
    seconds_diff = start_time.secsTo(end_time)
    # 减去休息时间
    if start_time.hour() < 12 and end_time.hour() >= 13:
        seconds_diff -= 3600 
    elif start_time.hour() < 12 and end_time.hour() == 12 and end_time.minute() > 0:
        seconds_diff -= end_time.minute() * 60
    elif start_time.hour() == 12 and end_time.hour() >= 13:
        seconds_diff -= start_time.minute() * 60
    time_diff = QTime(0, 0).addSecs(seconds_diff)
    formatted_time_diff = time_diff.toString('hh:mm')
    return formatted_time_diff


def update():
    try:
        remote_version = get_remote_version()
        print(f'Remote version: {remote_version}')
        if VERSION != remote_version:
            exe_file = f'//nas01/shares/dev/jumbla/jumbla{remote_version}.exe'
            subprocess.Popen(exe_file)
            QApplication.quit()
    except Exception as e:
        print(e)


def get_remote_version():
    try:
        with open(r'\\nas01\shares\dev\jumbla\version.json', 'r', encoding='utf-8') as f:
            remote_version = json.load(f)['VERSION']
            return remote_version
    except Exception as e:
        return e


def get_release_notes():
    try:
        with open(r'\\nas01\shares\dev\jumbla\version.json', 'r', encoding='utf-8') as f:
            release_notes = json.load(f)['ReleaseNotes']
            return release_notes
    except Exception as e:
        return e


if __name__ == '__main__':
    print(get_remote_version())
