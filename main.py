from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from lib.ias import Ias
from model.apires import BadRes, GoodRes

app = FastAPI()


@app.get("/ping", status_code=200)
@app.get("/")
def ping():
    return "pong"


class ElectricForm(BaseModel):
    username: str
    password: str
    meterId: str
    factoryCode: str


# 马区电费查询
@app.post("/electric")
def electric(form: ElectricForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return BadRes("登录失败,检查账密是否正确！")

    res = ias.fetch_electric_fee(form.meterId, form.factoryCode)

    res_json = res.json()

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


class BooksForm(BaseModel):
    username: str
    password: str


@app.post("/books")
def books(form: BooksForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return BadRes("登录失败,检查账密是否正确！")
    res = ias.fetch_books()
    return GoodRes("图书获取成功", res.json())


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )
