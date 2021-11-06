from fastapi import FastAPI
from pydantic import BaseModel
from requests.sessions import Session
from cwsf_ele import Cwsf
import uvicorn
import requests
import zhlgd
import json

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


@app.post("/ele/fee")
def ele_fee(form: EleFeeForm):
    cur_session = requests.session()
    if not login2cwsf(cur_session, form.username, form.password):
        return "查询失败"
    return json.loads(Cwsf(cur_session=cur_session).queryReserve(form.meter_id))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )
