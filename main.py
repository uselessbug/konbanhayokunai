# -*- coding: utf-8 -*-
import datetime
import json

import requests

ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;zfsoft'


def login(xgh: str, password: str):
    url = "https://xssw.zjgsu.edu.cn/api/v1/login"
    data = {
        "xgh": xgh,
        "password": password,
        "unionid": None
    }
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': ua
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


def get_cookies(access_token: str):
    url = "https://xssw.zjgsu.edu.cn/counsellor/h5/app?path=pages/home/signin/index&_sid=" + access_token
    headers = {
        'User-Agent': ua
    }
    s = requests.session()
    res = s.get(url=url, headers=headers, allow_redirects=False)
    return res.cookies


def get_list(first_access_token: str, type: str):
    url = "https://xssw.zjgsu.edu.cn/counsellor//api/v1/clockIn/task/getList"
    data = {
        type: True
    }
    headers = {
        'User-Agent': ua,
        'Authorization': "Bearer " + first_access_token
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


def signin(first_access_token: str, id: str, lon: float, la: float):
    url = "https://xssw.zjgsu.edu.cn/counsellor//api/v1/clockIn/task/signin"
    data = {
        "id": id,
        "info": {
            "longitude": lon,
            "latitude": la
        }
    }
    headers = {
        'User-Agent': ua,
        'Authorization': "Bearer " + first_access_token
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


if __name__ == '__main__':
    with open('app-user.json', encoding='utf-8') as f:
        users = json.load(f)
    for u in users:
        at = login(u["xgh"], u["password"])['data']['access_token']
        fat = requests.utils.dict_from_cookiejar(get_cookies(at))['first_access_token']
        for i in get_list(fat, "today")['data']:
            t = datetime.datetime.now().strftime('%Y-%m-%d')
            m = signin(fat, i['id'], u["longitude"], u["latitude"])['msg']
            print(t, "id: " + i['id'], m)
