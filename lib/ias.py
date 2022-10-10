import json
from urllib.parse import urlencode

import requests
from lxml import etree
from requests import Response

from lib.js_reader import des3


class Ias:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self) -> bool:
        res = self.session.get("http://zhlgd.whut.edu.cn/tpass/login")

        lt = etree.HTML(res.text).xpath("//input[@id='lt']/@value")[0]

        res = self.session.post(
            "http://zhlgd.whut.edu.cn/tpass/login?service=http%3A%2F%2Fzhlgd.whut.edu.cn%2Ftp_up%2F",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=urlencode({
                "rsa": des3(self.username, self.password, lt),
                "ul": len(self.username),
                "pl": len(self.password),
                "lt": lt,
                "execution": "e1s1",
                "_eventId": "submit",
            }))

        return res.url.startswith("http://zhlgd.whut.edu.cn/tp_up/view")

    def fetch_electric_fee(self, meter_id: str, factory_code: str) -> Response:
        self.session.get("http://cwsf.whut.edu.cn/casLogin")
        return self.session.post(
            "http://cwsf.whut.edu.cn/queryReserve",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=urlencode({
                "meterId": meter_id,
                "factorycode": factory_code
            })
        )

    def fetch_books(self) -> Response:
        url = "http://zhlgd.whut.edu.cn/tp_up/up/sysintegration/getlibraryRecordList"
        # {"draw":1,"order":[],"pageNum":1,"pageSize":10,"start":0,"length":10,"appointTime":"","dateSearch":"","startDate":"","endDate":""}
        data = {
            "draw": 1,
            "order": [],
            "pageNum": 1,
            "pageSize": 50,
            "start": 0,
            "length": 10,
            "appointTime": "",
            "dateSearch": "",
            "startDate": "",
            "endDate": "",
        }
        headers = {"Content-Type": "application/json"}
        return self.session.post(url=url, headers=headers, data=json.dumps(data))
