import execjs
import requests
import re
from lxml import etree
from urllib import parse
from requests.sessions import Session

# 获取加密代码
def get_rsa(username: str, password: str, lt: str) -> str:
    # 读取 js 脚本
    encode_js = open("encode.js", "r", encoding="utf-8").read()
    # 加载 js 脚本
    ctx = execjs.compile(encode_js)
    # 执行 js 脚本的 strEnc 函数并传入参数
    res = ctx.call("strEnc", username + password + lt, "1", "2", "3")
    return res


def inner_user_login():
    url = "http://cwsf.whut.edu.cn/innerUserLogin"
    res = requests.get(url)
    return res.cookies.get("JSESSIONID")


# 访问这个网页获取 cookie requests 会自动存储 cookie
def cas_login(asession: Session) -> tuple[str, str]:
    url = "http://cwsf.whut.edu.cn/casLogin"
    res = asession.get(url)
    # 获取 jsessionid
    jsessionid = res.cookies.get("JSESSIONID")
    # 获取 lt 参数 这个应该是随机数
    html = etree.HTML(res.text)
    lt = html.xpath("//input[@id='lt']/@value")[0]
    return jsessionid, lt


# 发起 post 请求 之后会被重定向至 http://cwsf.whut.edu.cn
def post_cas_login(
    username: str, password: str, jsessionid: str, lt: str, asession: Session
) -> str:
    url = "http://zhlgd.whut.edu.cn/tpass/login;jsessionid={}?service=http%3A%2F%2Fcwsf.whut.edu.cn%2FcasLogin".format(
        jsessionid
    )
    params = {"service": "http%3A%2F%2Fcwsf.whut.edu.cn%2FcasLogin"}
    data = {
        "rsa": get_rsa(username, password, lt),
        "ul": len(username),
        "pl": len(password),
        "lt": lt,
        "execution": "e1s1",
        "_eventId": "submit",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = asession.post(
        url=url,
        headers=headers,
        params=params,
        data=parse.urlencode(data),
    )
    if re.search("缴费平台", res.text) == None:
        return None
    else:
        return res.text
