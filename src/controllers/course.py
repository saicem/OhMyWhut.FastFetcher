import io
import uuid
from datetime import datetime

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import PlainTextResponse, StreamingResponse, JSONResponse, HTMLResponse

import config
from config import TERM_START_DATE, IMAGE_TTF
from models.course import Course
from models.form import LoginForm, CoursePngForm, CourseHtmlForm
from services.cal_maker import IcalWriter
from services.course_parser import parse_courses_from_main_page
from services.course_png.picgen import CourseDrawer
from services.ias import Ias
from services.lru_dict import LruDict

router = APIRouter(
    prefix='/course',
    tags=['course']
)

course_jar = LruDict(128)


def fetch_courses(username: str, password: str):
    ias = Ias(username, password)
    if not ias.login():
        return None

    res = ias.fetch_jwc_main_page()
    return parse_courses_from_main_page(res.text)


@router.post("/json", response_class=JSONResponse)
async def course_json(form: LoginForm):
    courses = fetch_courses(form.username, form.password)
    if courses is None:
        return PlainTextResponse(content="登录失败,检查账密是否正确！", status_code=401)

    cache_id = str(uuid.uuid4())
    course_jar.add(cache_id, courses)
    return JSONResponse(content=jsonable_encoder(
        {
            "data": {"courses": courses},
            "cacheId": cache_id,
        }
    ))


def get_current_week():
    return (datetime.date(datetime.now()) - config.TERM_START_DATE).days // 7 + 1


@router.post("/png", response_class=StreamingResponse)
async def course_png(form: CoursePngForm):
    courses = fetch_courses(form.username, form.password)
    if courses is None:
        return PlainTextResponse(content="获取课表失败", status_code=400)

    # 根据开学时间计算当前周
    if form.week == 0:
        form.week = get_current_week()

    if not 1 <= form.week <= 20:
        return PlainTextResponse(content="周次应该在 1~20", status_code=400)

    png = CourseDrawer(
        courses=[course for course in courses if course.startWeek <= form.week <= course.endWeek],
        week_order=form.week,
        term_start_day=TERM_START_DATE,
        font=IMAGE_TTF
    ).draw()
    buf = io.BytesIO()
    png.save(buf, format='png')
    buf.seek(0)
    return StreamingResponse(content=buf, media_type="image/png")


@router.get("/png/{cache_id}", response_class=StreamingResponse)
async def course_png(cache_id: str, week: int):
    courses = course_jar.get(cache_id)
    if courses is None:
        return PlainTextResponse(content="缓存失效", status_code=410)

    # 根据开学时间计算当前周
    if week == 0:
        week = get_current_week()

    if not 1 <= week <= 20:
        return PlainTextResponse(content="周次应该在 1~20", status_code=400)

    png = CourseDrawer(
        courses=[course for course in courses if course.startWeek <= week <= course.endWeek],
        week_order=week,
        term_start_day=TERM_START_DATE,
        font=IMAGE_TTF
    ).draw()
    buf = io.BytesIO()
    png.save(buf, format='png')
    buf.seek(0)
    return StreamingResponse(content=buf, media_type="image/png")


@router.post("/cal", response_class=StreamingResponse)
async def course_cal_post(form: LoginForm):
    courses = fetch_courses(form.username, form.password)
    if courses is None:
        return PlainTextResponse(content="获取课表失败", status_code=400)
    cal = IcalWriter(TERM_START_DATE, courses).make_ical_from_course()
    cal.seek(0)
    return StreamingResponse(content=cal, media_type="text/calendar",
                             headers={'Content-Disposition': 'attachment; filename="courses.ics"'})


@router.get("/cal/{cache_id}", response_class=StreamingResponse)
async def course_cal(cache_id: str):
    courses = course_jar.get(cache_id)
    if courses is None:
        return PlainTextResponse(content="缓存失效", status_code=410)
    cal = IcalWriter(TERM_START_DATE, courses).make_ical_from_course()
    cal.seek(0)
    return StreamingResponse(content=cal, media_type="text/calendar",
                             headers={'Content-Disposition': 'attachment; filename="courses.ics"'})


templates = {'basic'}


def render_course_html(template: str, courses: list[Course], week: int):
    content = open(f'{config.APP_FOLDER_PATH}/data/templates/{template}.html').read()
    content += f"""<script>
        data = {jsonable_encoder(
        {
            "courses": courses,
            "week": week,
            "termStartDate": config.TERM_START_DATE.strftime("%Y-%m-%d"),
        }
    )}
        render(data)
        </script>
        """
    return content


@router.post("/html", response_class=HTMLResponse)
async def course_html_post(form: CourseHtmlForm):
    courses = fetch_courses(form.username, form.password)
    if courses is None:
        return PlainTextResponse(content="获取课表失败", status_code=400)

    if not 0 <= form.week <= 20:
        return PlainTextResponse(content="周次应该在 1~20", status_code=400)

    if form.template not in templates:
        return PlainTextResponse(content="不存在此模板", status_code=400)

    return HTMLResponse(content=render_course_html(form.template, courses, form.week))


@router.get("/html/{cache_id}", response_class=HTMLResponse)
async def course_html(cache_id: str, week: int = 0, template: str = 'basic'):
    courses = course_jar.get(cache_id)
    if courses is None:
        return PlainTextResponse(content="缓存失效", status_code=410)

    if not 0 <= week <= 20:
        return PlainTextResponse(content="周次应该在 1~20", status_code=400)

    if template not in templates:
        return PlainTextResponse(content="不存在此模板", status_code=400)

    return HTMLResponse(content=render_course_html(template, courses, week))
