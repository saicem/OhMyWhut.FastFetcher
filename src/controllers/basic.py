from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, PlainTextResponse

from src.services.ias import Ias
from src.models.form import LoginForm, ElectricForm

router = APIRouter()


@router.post("/electric")
async def electric(form: ElectricForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)

    res = ias.fetch_electric_fee(form.meterId, form.factoryCode)
    res_json = res.json()

    remain_power = (
        f"{res_json['remainPower']}{res_json['remainName']}"
        if "remainPower" in res_json and "remainName" in res_json
        else "无数据"
    )
    remain_fee = (
        f"{res_json['meterOverdue']}元"
        if "meterOverdue" in res_json
        else "无数据"
    )
    total_power = (
        f"{res_json['ZVlaue']}{res_json['unit']}"
        if "ZVlaue" in res_json and "unit" in res_json
        else "无数据"
    )

    return JSONResponse(content=jsonable_encoder(
        {
            "data": {
                "remainPower": remain_power,
                "totalPower": total_power,
                "remainFee": remain_fee,
            }
        }
    ))


@router.post("/books")
async def books(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_books()
    raw_books = res.json()['list']

    def filter_book(book: {}):
        return {
            "name": book['ZBT'],
            "expire": book['DQRQ'],
            "borrow": book['JYRQ'],
        }

    cooked_books = [filter_book(book) for book in raw_books]
    return JSONResponse(content=jsonable_encoder({"data": {"books": cooked_books}}))


@router.post("/card/money")
async def get_card_money(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_card_money()
    money = int(res.json()['KHYE'])
    return JSONResponse(content=jsonable_encoder({"data": {"cardMoney": f"{money // 100}.{money % 100}元"}}))
