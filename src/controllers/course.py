import io
from datetime import datetime

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import PlainTextResponse, StreamingResponse, JSONResponse

from src import config
from src.config import TERM_START_DAY, IMAGE_TTF
from src.models.form import CoursePngForm, LoginForm
from src.services.cal_maker import IcalWriter
from src.services.course_parser import parse_courses_from_main_page
from src.services.course_png.picgen import CourseDrawer
from src.services.ias import Ias

router = APIRouter(
    prefix='/course',
    tags=['course']
)


@router.post("/png")
async def course_png(form: CoursePngForm):
    # 根据开学时间计算当前周
    if form.week == 0:
        form.week = (datetime.date(datetime.now()) - config.TERM_START_DAY).days // 7 + 1

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


@router.post("/course/json")
async def course_json(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_jwc_main_page()
    courses = parse_courses_from_main_page(res.text)
    return JSONResponse(content=jsonable_encoder({"data": {"courses": courses}}))


@router.post("/course/cal")
async def course_ical(form: LoginForm):
    ias = Ias(form.username, form.password)
    if not ias.login():
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)
    res = ias.fetch_jwc_main_page()
    courses = parse_courses_from_main_page(res.text)
    cal = IcalWriter(TERM_START_DAY, courses).make_ical_from_course()
    cal.seek(0)
    return StreamingResponse(content=cal, media_type="text/calendar",
                             headers={'Content-Disposition': 'attachment; filename="courses.ics"'})
