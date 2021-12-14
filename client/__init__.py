import requests

s = requests.session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/96.0.4664.93 "
                  "Safari/537.36 "
                  "Edg/96.0.1054.53",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"})


def get(url: str, headers=None, params=None):
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    ret = s.get(url, headers=headers, params=params)
    return ret


def post(url: str, headers=None, data=None, j=None):
    if headers is None:
        headers = {}
    if data is None:
        data = {}

    ret = s.post(url, headers=headers, data=data, json=j)
    return ret
