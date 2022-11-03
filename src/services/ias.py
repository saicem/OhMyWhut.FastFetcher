import json
from urllib.parse import urlencode

import requests
from lxml import etree
from requests import Response

import config
from services.js_reader import des3


class Ias:
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password
        self.session = requests.session()
        self.session.headers.setdefault("user-agent", config.USER_AGENT)

    def login(self) -> bool:
        res = self.session.get("http://zhlgd.whut.edu.cn/tpass/login")
        lt = etree.HTML(res.text).xpath("//input[@id='lt']/@value")[0]
        res = self.session.post(
            "http://zhlgd.whut.edu.cn/tpass/login?service=http%3A%2F%2Fzhlgd.whut.edu.cn%2Ftp_up%2F",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            },
            data=urlencode({
                "rsa": des3(self.__username, self.__password, lt),
                "ul": len(self.__username),
                "pl": len(self.__password),
                "lt": lt,
                "execution": "e1s1",
                "_eventId": "submit",
            }))

        return res.url.startswith("http://zhlgd.whut.edu.cn/tp_up/view")

    def fetch_electric_fee(self, meter_id: str, factory_code: str) -> Response:
        self.session.get("http://cwsf.whut.edu.cn/casLogin")
        return self.session.post(
            url="http://cwsf.whut.edu.cn/queryReserve",
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
        data = {
            "draw": 1,
            "pageNum": 1,
            "pageSize": 50,
            "start": 0,
            "length": 50,
            "appointTime": "",
        }
        headers = {"Content-Type": "application/json"}
        return self.session.post(url=url, headers=headers, data=json.dumps(data))

    def fetch_jwc_main_page(self) -> Response:
        res = self.session.get(
            "http://zhlgd.whut.edu.cn/tpass/login?service=http%3A%2F%2Fsso.jwc.whut.edu.cn%2FCertification%2Findex2.jsp")
        if not res.url.startswith("http://sso.jwc.whut.edu.cn/Certification/index2.jsp"):
            raise Exception("登录教务处失败")

        res = self.session.get("http://sso.jwc.whut.edu.cn/Certification/casindex.do", headers={"Referrer": res.url})
        if not res.url.startswith("http://sso.jwc.whut.edu.cn/Certification/toIndex.do"):
            raise Exception("登录教务处失败")

        self.session.get("http://218.197.102.183/Course")
        res = self.session.get("http://218.197.102.183/Course/grkbList.do")

        return res

    def fetch_card_money(self) -> Response:
        """
        获取校园卡余额，单位（分）
        """
        return self.session.post(url="http://zhlgd.whut.edu.cn/tp_up/up/sysintegration/getCardMoney",
                                 headers={"Content-Type": "application/json"},
                                 data="{}")
