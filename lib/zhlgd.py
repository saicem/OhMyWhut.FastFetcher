import json
import execjs
import requests
import re
import os
from lxml import etree
from urllib import parse
from requests.sessions import Session

# 获取加密代码
def getRsa(username: str, password: str, lt: str) -> str:
    # 读取 js 脚本
    js_path = os.path.dirname(__file__) + "/encode.js"
    encode_js = open(js_path, "r", encoding="utf-8").read()
    # 加载 js 脚本
    ctx = execjs.compile(encode_js)
    # 执行 js 脚本的 strEnc 函数并传入参数
    res = ctx.call("strEnc", username + password + lt, "1", "2", "3")
    return res


def innerUserLogin():
    url = "http://cwsf.whut.edu.cn/innerUserLogin"
    res = requests.get(url)
    return res.cookies.get("JSESSIONID")


# 访问这个网页获取 cookie requests 会自动存储 cookie
def cwsfCasLogin(curSession: Session) -> tuple[str, str]:
    url = "http://cwsf.whut.edu.cn/casLogin"
    res = curSession.get(url)
    # 获取 jsessionid
    jsessionid = res.cookies.get("JSESSIONID")
    return jsessionid, getLt(res.text)


# 获取参数 lt 用于智慧理工大登录 猜测是随机数
# 在访问智慧理工大登录界面 表单中 input 的属性 id="lt"
def getLt(html: str):
    return etree.HTML(html).xpath("//input[@id='lt']/@value")[0]


# 智慧理工大登录
# 发起 post 请求 之后会被重定向至 http://cwsf.whut.edu.cn
# Central Authentication Service
def loginCwsf(
    username: str, password: str, jsessionid: str, lt: str, curSession: Session
) -> str:
    url = "http://zhlgd.whut.edu.cn/tpass/login;jsessionid={}".format(jsessionid)
    # 这里 params 的 service 参数表示重定向的地址 非必要
    # params = {"service": "http%3A%2F%2Fcwsf.whut.edu.cn%2FcasLogin"}
    data = {
        "rsa": getRsa(username, password, lt),
        "ul": len(username),
        "pl": len(password),
        "lt": lt,
        "execution": "e1s1",
        "_eventId": "submit",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = curSession.post(
        url=url,
        headers=headers,
        # params=params,
        data=parse.urlencode(data),
    )
    if re.search("缴费平台", res.text) == None:
        return None
    else:
        return res.text


def login(username: str, password: str, curSession: Session) -> bool:
    url = "http://zhlgd.whut.edu.cn/tpass/login"
    lt = getLt(curSession.get(url).text)
    data = {
        "rsa": getRsa(username, password, lt),
        "ul": len(username),
        "pl": len(password),
        "lt": lt,
        "execution": "e1s1",
        "_eventId": "submit",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    curSession.get(url)
    res = curSession.post(
        url=url,
        headers=headers,
        data=parse.urlencode(data),
    )
    return res.status_code == 200


def getLibRecordList(curSession: Session) -> str:
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
    txt = curSession.post(url=url, headers=headers, data=json.dumps(data)).text
    return txt
