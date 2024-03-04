# -*- coding: utf-8 -*-
from PyQt5.QtCore import QTime


def calculateWorkingTime(startTime:QTime, endTime:QTime):
    # 计算时间差
    totalSeconds = startTime.secsTo(endTime)

    # 开始时间12点前，结束时间13点后午休扣除1小时
    if startTime.hour() < 12 and endTime.hour() >= 13:
        if endTime.hour() != 13 or endTime.minute() != 0:
            totalSeconds -= 3600
    # 开始时间12点后13点前
    elif startTime.hour() == 12 and startTime.minute() > 0 and endTime.hour() == 13:
        minutesRemove = (60 - startTime.minute()) + endTime.minute()
        totalSeconds -= minutesRemove * 60

    totalMinutes = totalSeconds // 60
    return totalMinutes


if __name__ == '__main__':
    startTime = QTime(12, 30)
    endTime = QTime(13, 30)
    print(calculateWorkingTime(startTime, endTime))

