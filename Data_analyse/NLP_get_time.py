# coding=gbk
# @Time : 2022/1/16 15:04
# @Author : Sky
# @File : NLPGetTime.py
# @Software : PyCharm

import re
from datetime import datetime, timedelta
from dateutil.parser import parse
import jieba.posseg as psg

UTIL_CN_NUM = {'��': 0, 'һ': 1, '��': 2, '��': 3, '��': 4, '��': 5, '��': 6, '��': 7, '��': 8, '��': 9, '0': 0, '1': 1, '2': 2,
               '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
UTIL_CN_UNIT = {'ʮ': 10, '��': 100, 'ǧ': 1000, '��': 10000}


def get_lastweek(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=7 - day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '��' + str(date_from)[5:7] + '��' + str(date_from)[8:10] + '��'


def get_nextweek(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=-7 - day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '��' + str(date_from)[5:7] + '��' + str(date_from)[8:10] + '��'


def get_week(day=1):
    d = datetime.now()
    dayscount = timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = timedelta(days=-day)
    dayfrom = dayto - sixdays
    date_from = datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    return str(date_from)[0:4] + '��' + str(date_from)[5:7] + '��' + str(date_from)[8:10] + '��'


def check_time_valid(word):
    m = re.match("\d+$", word)
    if m:
        if len(word) <= 6:
            return None
    word1 = re.sub('[��|��]\d+$', '��', word)
    if word1 != word:
        return check_time_valid(word)
    else:
        return word1


def cn2dig(src):
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return rsl


def year2dig(year):
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    m = re.match("\d+", res)
    if m:
        if len(m.group(0)) == 2:
            return int(datetime.today().year / 100) * 100 + int(m.group(0))
        else:
            return int(m.group(0))
    else:
        return None


def parse_datetime(msg):
    tmptime = datetime.today().strftime('%Y{y}%m{m}%d{d}%H{h}%M{m}%S{s}').format(y='��', m='��', d='��', h='ʱ', M='��',
                                                                                 s='��')  # ��ȡ������ʱ����
    if msg is None or len(msg) == 0:
        return None
    try:
        dt = parse(msg, fuzzy=True)
        return dt.strftime('%Y-%m-%d %H:%M:%s')
    except Exception as e:
        m = re.match(
            "([0-9��һ�����������߰˾�ʮ]+��)?([0-9��һ�����������߰˾�ʮ]+��)?([0-9��һ�����������߰˾�ʮ]+[����])?([������������]+)?([0-9��һ�����������߰˾�ʮ��]+["
            "��:ʱ])?([0-9��һ�����������߰˾�ʮ��]+��)?([0-9��һ�����������߰˾�ʮ��]+��)?",
            msg)
        if m.group(0) is not None:
            res = {"year": m.group(1) if m.group(1) is not None else str(tmptime[0:5]),
                   "month": m.group(2) if m.group(2) is not None else str(tmptime[5:8]),
                   "day": m.group(3) if m.group(3) is not None else str(tmptime[8:11]),
                   "hour": m.group(5) if m.group(5) is not None else '00',
                   "minute": m.group(6) if m.group(6) is not None else '00',
                   "second": m.group(7) if m.group(7) is not None else '00', }
            # print("ƥ��",res)
            params = {}
            for name in res:
                if res[name] is not None and len(res[name]) != 0:
                    tmp = None
                    if name == 'year':
                        tmp = year2dig(res[name][:-1])
                    else:  # ʱ���ʽת��
                        tmp = cn2dig(res[name][:-1])
                    if tmp is not None:
                        params[name] = int(tmp)
            # print("----------------------��",params)
            target_date = datetime.today().replace(**params)  # ���µ�ʱ������滻��ǰ��ʱ��
            is_pm = m.group(4)
            if is_pm is not None:
                if is_pm == u'����' or is_pm == u'����' or is_pm == '����':
                    hour = params['hour']
                    if hour < 12:
                        target_date = target_date.replace(hour=hour + 12)
            return target_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None


def time_extract(text):
    time_res = []
    word = ''
    keyDate = {'����': 0, '����': 1, '����': 2, '����': -1, 'ǰ��': -2}
    timedic = ['ʱ', '��', '��']
    tmptext = []
    for k, v in psg.cut(text):
        tmptext.append([k, v])
    for i in range(len(tmptext)):
        k, v = tmptext[i][0], tmptext[i][1]
        if k in keyDate:  # ���졢���졢���졢���졢ǰ�����ʱ����ȡ����
            word = (datetime.today() + timedelta(days=keyDate.get(k, 0))).strftime('%Y{y}%m{m}%d{d}').format(y='��',
                                                                                                             m='��',
                                                                                                             d='��')
        elif k == '��':  # ʱ�����ȡ
            if word != '':
                time_res.append(word)
                word = ''
        elif word != '':
            if v in ['m', 't']:
                try:
                    if tmptext[i + 1][0] in timedic:
                        word = word + k + tmptext[i + 1][0]
                    else:
                        word = word + k
                except:
                    word = word + k
            elif k not in timedic:
                time_res.append(word)
                word = ''
        elif v in ['m', 't']:
            word = k
    if word != '':
        time_res.append(word)
    tmp_time_res = []
    for i in range(len(time_res)):
        if time_res[i][:2] in ['����', '����']:
            if time_res[i][2:3] in UTIL_CN_NUM.keys():
                day = UTIL_CN_NUM[time_res[i][2:3]]
                if time_res[i][:2] == '����':
                    tmp_time_res.append(get_lastweek(day) + time_res[i][3:])
                else:
                    tmp_time_res.append(get_nextweek(day) + time_res[i][3:])
        elif time_res[i][:1] == '��':
            if time_res[i][1:2] in UTIL_CN_NUM.keys():
                day = UTIL_CN_NUM[time_res[i][1:2]]
                if time_res[i][:1] == '��':
                    tmp_time_res.append(get_week(day) + time_res[i][2:])
        else:
            tmp_time_res.append(time_res[i])
    time_res = tmp_time_res
    try:
        return time_res
    except:
        return None


def getTime(text):
    time = []
    for element in time_extract(text):
        if len(element) > 5 and element.endswith('��') and not element.startswith('ͬ��'):
            time.append(element)
    return time
