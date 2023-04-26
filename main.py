# -*- coding: utf-8 -*-
import datetime
import json
import sys

import pytz
import requests

ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;zfsoft'
null = None
true = True


def login(xgh: str, password: str):
    url = 'https://xssw.zjgsu.edu.cn/api/v1/login'
    data = {
        'xgh': xgh,
        'password': password,
        'unionid': null
    }
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': ua
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


def getCookies(access_token: str):
    url = 'https://xssw.zjgsu.edu.cn/counsellor/h5/app?path=pages/application/checkin/index&_sid=' + access_token
    headers = {
        'User-Agent': ua
    }
    s = requests.session()
    res = s.get(url=url, headers=headers, allow_redirects=False)
    return res.cookies


def getUserScheduling(first_access_token: str):
    url = 'https://xssw.zjgsu.edu.cn/counsellor/api/v1/clockIn/scheduling/getUserScheduling'
    data = {
    }
    headers = {
        'User-Agent': ua,
        'Authorization': 'Bearer ' + first_access_token
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


def userCheckIn(first_access_token: str, id: str, add: str, info: dict):
    url = 'https://xssw.zjgsu.edu.cn/counsellor/api/v1/clockIn/scheduling/userCheckIn'
    data = {
        'address': add,
        'word_id': id,
        'info': info,
        'exception_type': null,
        'exceptions': null
    }
    headers = {
        'User-Agent': ua,
        'Authorization': 'Bearer ' + first_access_token
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


if __name__ == '__main__':
    with open('app-user.json', encoding='utf-8') as f:
        users = json.load(f)
    for u in users:
        at = login(u['xgh'], u['password'])['data']['access_token']
        fat = requests.utils.dict_from_cookiejar(getCookies(at))['first_access_token']
        us = getUserScheduling(fat)
        i = us['data']['scheduling']['id']
        st = us['data']['scheduling']['start_time']
        et = us['data']['scheduling']['end_time']
        today = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d')
        st = datetime.datetime.strptime(f'{today} {st}', '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=pytz.timezone('Asia/Shanghai'))
        et = datetime.datetime.strptime(f'{today} {et}', '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=pytz.timezone('Asia/Shanghai'))
        n = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        if st < n < et or '-force' in sys.argv:
            if us['data']['lasterrow'] is None or '-force' in sys.argv:
                uci = userCheckIn(fat, i, u['address'], u['info'])
                t = uci['data']['sign_at']
                m = uci['msg']
                print(t, 'xgh: ' + u['xgh'], 'id: ' + i, m)
            else:
                t = datetime.datetime.strptime(us['data']['lasterrow']['sign_at'], '%Y-%m-%d %H:%M:%S').strftime(
                    '%H:%M:%S')
                n = n.strftime('%Y-%m-%d %H:%M:%S')
                print(n, 'xgh: ' + u['xgh'], 'id: ' + i, f'{t}に手動でチェックインしました。「-force」パラメータで強制チェックインをします（リスクある）')
        else:
            n = n.strftime('%Y-%m-%d %H:%M:%S')
            print(n, 'xgh: ' + u['xgh'], 'id: ' + i, 'チェックインすべき時間の範囲外です。「-force」パラメータで強制チェックインをします（リスクある）')
