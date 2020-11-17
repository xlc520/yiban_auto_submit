import datetime
import time


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def get_time_no_second():
    return time.strftime("%Y-%m-%d %H:%M", time.localtime())

def get_7_day_ago():
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-7)
    n_days = now + delta
    return n_days.strftime('%Y-%m-%d')


def get_today():
    return time.strftime("%Y-%m-%d", time.localtime())


def desc_sort(array, key="FeedbackTime"):
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j][key] < array[j + 1][key]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array
