import io

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
import uvicorn

from config import *

from lib.course.course import parse_courses_from_main_page
from lib.course.ical_maker import IcalWriter
from lib.course.picgen import CourseDrawer
from lib.ias import Ias

app = FastAPI()


@app.get("/ping", status_code=200)
@app.get("/")
def ping():
    return "pong"


class LoginForm(BaseModel):
    username: str
    password: str


class ElectricForm(LoginForm):
    meterId: str
    factoryCode: str


class CoursePngForm(LoginForm):
    week: int


# 马区电费查询
@app.post("/electric")
def electric(form: ElectricForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)

    res = ias.fetch_electric_fee(form.meterId, form.factoryCode)
    res_json = res.json()

    remain_power: str = (
        "{}{}".format(res_json["remainPower"], res_json["remainName"])
        if (
                res_json.__contains__("remainPower") and res_json.__contains__("remainName")
        )
        else "无数据"
    )
    remain_fee = res_json.get("meterOverdue", "无数据")

    return JSONResponse(content=jsonable_encoder({"remainPower": remain_power, "remainFee": remain_fee}))


@app.post("/books")
def books(form: LoginForm):
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
    return JSONResponse(content=jsonable_encoder({"books": cooked_books}))


@app.post("/course/png")
def course_png(form: CoursePngForm):
    if not 1 <= form.week <= 20:
        return PlainTextResponse(content="周次应该在 1~20", status_code=400)

    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)

    res = ias.fetch_jwc_main_page()
    courses = parse_courses_from_main_page(res.text)
    png = CourseDrawer(
        courses=[course for course in courses if course.StartWeek <= form.week <= course.EndWeek],
        week_order=form.week,
        term_start_day=TERM_START_DAY,
        font=IMAGE_TTF
    ).draw()
    buf = io.BytesIO()
    png.save(buf, format='png')
    buf.seek(0)
    return StreamingResponse(content=buf, media_type="image/png")


@app.post("/course/json")
def course_json(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_jwc_main_page()
    courses = parse_courses_from_main_page(res.text)
    return JSONResponse(content=jsonable_encoder({"data": courses}))


@app.post("/course/ical")
def course_ical(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_jwc_main_page()
    courses = parse_courses_from_main_page(res.text)
    cal = IcalWriter(TERM_START_DAY, courses).make_ical_from_course()
    cal.seek(0)
    return StreamingResponse(content=cal, media_type="text/calendar",
                             headers={'Content-Disposition': 'attachment; filename="courses.ics"'})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True,
        log_level="info",
    )
