# coding: utf-8
r"""Fetch 聊天女仆.

https://api.sc2h.cn/
https://api.sc2h.cn/api/94api.php?type=sc&msg=

https://api.sc2h.cn/api/yiyan.php?data=类型
0（随机一言）
例：https://api.sc2h.cn/api/yiyan.php?data=0

1（动画一言）
2（漫画一言）
3（游戏一言）
4（小说一言）
 https://api.sc2h.cn/api/yiyan.php?data=4
5（原创一言）
6（网络一言）
7（其他一言）

In [183]: url_str
Out[183]: 'http://api.sc2h.cn/api/maid.php?data=0&sign=user&msg=你好啊'

http://api.sc2h.cn/api/maid.php?data=0&sign=user&msg=%E4%BD%A0%E5%A5%BD%E5%95%8A

pytest --doctest-modules maiden_chat.py

In [184]: resp = requests.get(url_str, headers={'User-agent': UA})

>>> resp = maiden_chat('你')
>>> print(resp) # doctest: +SKIP
[...] # doctest: +ELLIPSIS does not work when ... at the beginning
>>> any(map(lambda x: x in resp, ['你', '一句话', '我', '问题', '大家']))
True
"""
# pylint: disable=broad-except

import urllib
import requests

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"  # pylint: disable=line-too-long
HEADERS = {"User-agent": UA}
URL = "http://api.sc2h.cn/api/maid.php"


def maiden_chat(query, timeout=(55, 66)):
    """Get a response."""
    data = {"data": 0, "sign": "user", "msg": query}

    try:
        # resp = requests.post(URL, data=data, headers=HEADERS)
        resp = requests.get(
            f"{URL}?{urllib.parse.urlencode(data)}", headers=HEADERS, timeout=timeout,
        )
        resp.raise_for_status()
    except Exception as exc:
        return str(exc)

    return resp.text
