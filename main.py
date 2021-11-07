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


@app.get("/")
def ping():
    return "pong"


class EleFeeForm(BaseModel):
    username: str
    password: str
    meter_id: str


def login2cwsf(cur_session: Session, username: str, password: str) -> bool:
    jsessionid, lt = zhlgd.cas_login(cur_session)
    text = zhlgd.post_cas_login(username, password, jsessionid, lt, cur_session)
    return text != None


@app.post("/cwsf/ele/fee")
def ele_fee(form: EleFeeForm):
    cur_session = requests.session()
    if not login2cwsf(cur_session, form.username, form.password):
        return BadRes("查询失败")
    return GoodRes(
        "查询成功", json.loads(Cwsf(cur_session=cur_session).queryReserve(form.meter_id))
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )
