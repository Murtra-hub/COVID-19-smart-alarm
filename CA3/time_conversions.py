""" This module modifies the date and the time so that alarms can be schedualed
and  so that alarms and notifications titles can print the current time"""

import time

def current_time():
    """ This functions returns a string with the current date and time """

    day = str(time.localtime().tm_mday)
    month = str(time.localtime().tm_mon) + "-"
    year = str(time.localtime().tm_year) + "-"

    date = year + month + day
    hour = str(time.localtime().tm_hour) + ":" + str(time.gmtime().tm_min)

    return date + " at " + hour

def alarm_to_time(alarm: str):
    """ This function converts the time when the alarm is setted into seconds """
    time_alarm = time.strptime(alarm + ":00", "%Y-%m-%dT%H:%M:%S")
    return time.mktime(time_alarm)
