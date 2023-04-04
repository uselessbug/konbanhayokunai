import requests
import json

ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;zfsoft'


def login(xgh: str, password: str):
    global ua
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


def get_list(token: str):
    global ua
    url = "https://xssw.zjgsu.edu.cn/counsellor/h5/app?path=pages/home/signin/index&_sid=" + token
    headers = {
        'User-Agent': ua
    }
    '''print(url)'''
    s = requests.session()
    res = s.get(url=url, headers=headers, allow_redirects=False)
    url = "https://xssw.zjgsu.edu.cn/counsellor//api/v1/clockIn/task/getList"
    data = {
        "today": True,
        "history": False,
        "future": False
    }
    global authorizations
    authorizations = headers['Authorization'] = "Bearer " + requests.utils.dict_from_cookiejar(res.cookies)['first_access_token']
    res = s.post(url=url, headers=headers, json=data)
    return res.json()


def signin(authorization: str, id: str, lon: float, la: float):
    global ua
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
        'Authorization': authorization
    }
    s = requests.session()
    res = s.post(url=url, headers=headers, json=data)
    return res.json()

if __name__ == '__main__':
    with open('app-user.json', encoding='utf-8') as f:
        u = json.load(f)
    t = login(u[0]["xgh"], u[0]["password"])['data']['access_token']
    for i in get_list(t)['data']:
        print(signin(authorizations, i['id'], u[0]["longitude"], u[0]["latitude"])['msg'])

