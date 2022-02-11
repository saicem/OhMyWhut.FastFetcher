from fastapi import FastAPI
from pydantic import BaseModel
from requests.sessions import Session
import uvicorn
import requests
import json
from model.apires import BadRes, GoodRes
from lib.cwsf_ele import Cwsf
from lib import zhlgd

app = FastAPI()


@app.get("/ping")
@app.get("/")
def ping():
    return "pong"


def login2cwsf(curSession: Session, username: str, password: str) -> bool:
    jsessionid, lt = zhlgd.cwsfCasLogin(curSession)
    text = zhlgd.loginCwsf(username, password, jsessionid, lt, curSession)
    return text != None


class EleFeeFormMa(BaseModel):
    username: str
    password: str
    meter_id: str


# 马区电费查询
@app.post("/cwsf/ele/ma")
def ele_ma(form: EleFeeFormMa):
    cur_session = requests.session()
    if not login2cwsf(cur_session, form.username, form.password):
        return BadRes("登录失败,检查账密是否正确！")
    res_json: dict[str] = json.loads(
        Cwsf(cur_session=cur_session).queryReserve(form.meter_id)
    )
    # 剩余电量
    remain_power: str = (
        "{}{}".format(res_json["remainPower"], res_json["remainName"])
        if (
            res_json.__contains__("remainPower") and res_json.__contains__("remainName")
        )
        else "无数据"
    )
    # 剩余电费
    remain_due = res_json.get("meterOverdue", "无数据")
    return GoodRes("查询成功", "剩余电量: {}\n剩余电费: {}".format(remain_power, remain_due))


class EleFeeFormYu(BaseModel):
    username: str
    password: str
    roomno: str


# 余区电费查询
@app.post("/cwsf/ele/yu")
def ele_yu(form: EleFeeFormYu):
    cur_session = requests.session()
    if not login2cwsf(cur_session, form.username, form.password):
        return BadRes("登录失败,检查账密是否正确！")
    res_json: dict[str, str] = json.loads(
        Cwsf(cur_session=cur_session).querySydl(form.roomno)
    )
    if not res_json.__contains__("roomlist"):
        return BadRes("查询失败")
    room_list: dict[str] = res_json["roomlist"]
    remain_power = (
        "剩余{}: {}".format(room_list["remainName"], room_list["remainPower"])
        if room_list.__contains__("remainName")
        and room_list.__contains__("remainPower")
        else "无数据"
    )
    read_time = "查表时间: {}".format(room_list.get("readTime", "无数据"))
    return GoodRes("获取成功", "{}\n{}".format(remain_power, read_time))


class ZhlgdForm(BaseModel):
    username: str
    password: str


@app.post("/zhlgd/lib/record")
def libRecord(form: ZhlgdForm):
    curSession = requests.session()
    zhlgd.login(form.username, form.password, curSession)
    res = zhlgd.getLibRecordList(curSession)
    return GoodRes("获取成功", res)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )
