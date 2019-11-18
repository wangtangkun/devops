#！/usr/bin/env python
#-*- coding:utf-8 -*-

class Cron_time():
    # 定义 分 时 日 月 周 传给前端用来显示、选择
    def min(self):
        # 定义分钟：
        min = []
        for i in range(60):
            min.append(i)
            min.append("*/{}".format(i))
        return min

    # # #定义小时:
    def hour(self):
        hour = []
        for i in range(24):
            hour.append(i)
        return hour
    #
    # # 定义日:
    def day(self):
        day = []
        for i in range(1, 32):
            day.append(i)
        return day
    #
    # # 定义月：
    def mouth(self):
        mouth = []
        for i in range(1, 13):
            mouth.append(i)
        return mouth
    #
    # # 定义周:
    def week(self):
        week = []
        for i in range(7):
            week.append(i)
        return week

