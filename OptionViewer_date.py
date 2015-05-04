# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 15:39:17 2015

@author: assa
"""

import calendar
import numpy as np
import datetime as dt

holidays = ['2015-05-05', '2015-05-25', '2015-09-28', '2015-09-29', '2015-10-09',
            '2015-12-25', '2016-01-01', '2016-02-08', '2016-02-09', '2016-03-01', '2016-05-05']

# nowtoday = dt.date.today()


def getoptionexpiredate(nowdate=None):
    if not nowdate:
        nowdate = dt.date.today()
    c1 = calendar.monthcalendar(nowdate.year, nowdate.month)
    if nowdate.month == 12:
        c2 = calendar.monthcalendar(nowdate.year + 1, 1)
        nextyear = nowdate.year + 1
        nextmonth = 1
    else:
        c2 = calendar.monthcalendar(nowdate.year, nowdate.month + 1)
        nextyear = nowdate.year
        nextmonth = nowdate.month + 1

    first_week1 = c1[0]
    second_week1 = c1[1]
    third_week1 = c1[2]

    first_week2 = c2[0]
    second_week2 = c2[1]
    third_week2 = c2[2]

    if first_week1[calendar.THURSDAY]:
        second_thursday1 = second_week1[calendar.THURSDAY]
    else:
        second_thursday1 = third_week1[calendar.THURSDAY]

    if first_week2[calendar.THURSDAY]:
        second_thursday2 = second_week2[calendar.THURSDAY]
    else:
        second_thursday2 = third_week2[calendar.THURSDAY]

    if nowdate.day <= second_thursday1:
        expire_date = dt.date(nowdate.year, nowdate.month, second_thursday1)
    else:
        expire_date = dt.date(nextyear, nextmonth, second_thursday2)

    # print 'front month expire date: ', expire_date
    return expire_date


def getfutureexpiredate(nowdate=None):
    if not nowdate:
        nowdate = dt.date.today()

    if not nowdate.month % 3:
        c1 = calendar.monthcalendar(nowdate.year, nowdate.month)
        if nowdate.month == 12:
            c2 = calendar.monthcalendar(nowdate.year + 1, 3)
            nextyear = nowdate.year + 1
            nextmonth = 3
        else:
            c2 = calendar.monthcalendar(nowdate.year, (nowdate.month / 3 + 1) * 3)
            nextyear = nowdate.year
            nextmonth = (nowdate.month / 3 + 1) * 3

        first_week1 = c1[0]
        second_week1 = c1[1]
        third_week1 = c1[2]

        first_week2 = c2[0]
        second_week2 = c2[1]
        third_week2 = c2[2]

        if first_week1[calendar.THURSDAY]:
            second_thursday1 = second_week1[calendar.THURSDAY]
        else:
            second_thursday1 = third_week1[calendar.THURSDAY]

        if first_week2[calendar.THURSDAY]:
            second_thursday2 = second_week2[calendar.THURSDAY]
        else:
            second_thursday2 = third_week2[calendar.THURSDAY]

        if nowdate.day <= second_thursday1:
            expire_date = dt.date(nowdate.year, nowdate.month, second_thursday1)
        else:
            expire_date = dt.date(nextyear, nextmonth, second_thursday2)

        return expire_date
    else:
        c2 = calendar.monthcalendar(nowdate.year, (nowdate.month / 3 + 1) * 3)
        nextyear = nowdate.year
        nextmonth = (nowdate.month / 3 + 1) * 3

        first_week2 = c2[0]
        second_week2 = c2[1]
        third_week2 = c2[2]

        if first_week2[calendar.THURSDAY]:
            second_thursday2 = second_week2[calendar.THURSDAY]
        else:
            second_thursday2 = third_week2[calendar.THURSDAY]

        expire_date = dt.date(nextyear, nextmonth, second_thursday2)

        return expire_date


def getoptionbusdayttm(nowdate=None):
    if not nowdate:
        nowdate = dt.date.today()
    expire_date = getoptionexpiredate(nowdate)
    days = np.busday_count(nowdate, expire_date, holidays=holidays)    # holidays = []
    # print 'TTM (BD): ', days
    return days


def getfuturebusdayttm(nowdate=None):
    if not nowdate:
        nowdate = dt.date.today()
    expire_date = getfutureexpiredate(nowdate)
    days = np.busday_count(nowdate, expire_date, holidays=holidays)    # holidays = []
    # print 'TTM (BD): ', days
    return days


def getoneyearday(nowdate=None):
    if not nowdate:
        nowdate = dt.date.today()
    oneyearbizdays = np.busday_count(nowdate, dt.date(nowdate.year+1, nowdate.month, nowdate.day), holidays=holidays)
    # print 'OneYearDay: ', oneyearbizdays
    return oneyearbizdays
    
if __name__ == '__main__':
    nowtoday = dt.date(2014, 8, 2)
    print 'NowToday: ', nowtoday
    print
    print 'OptionExpireDate: ', getoptionexpiredate(nowtoday)
    print 'OptionBizDayTTM: ', getoptionbusdayttm(nowtoday)
    print 'OneYearDay: ', getoneyearday(nowtoday)
    print
    print 'FutureExpireDate: ', getfutureexpiredate(nowtoday)
    print 'OptionBizDayTTM: ', getfuturebusdayttm(nowtoday)
    print 'OneYearDay: ', getoneyearday(nowtoday)




