import re

from lxml import etree
from lxml.etree import _Element

from models.course import Course


def parse_courses_from_main_page(html: str) -> list[Course]:
    root = etree.HTML(html)
    courses: list[Course] = []
    # 5*7个 5为5个大节 7为7天
    tds: list[_Element] = root.xpath('//*[@id="weekTable"]/tbody/tr/td[@id]')
    for idx, td in enumerate(tds):
        # 需要更多的样本来处理、验证解析是否正确、如解析错误请发起 issue，并提供源 html
        # 形势与政策(第10-13周6-7节,王珺老师,东教-合一)
        match = re.match("(.+?)\\(第(\\d+)-(\\d+)周(\\d+)-(\\d+)节,(.+)老师,(.+)\\)", re.sub('\\s', '', td.text))
        if match is None:
            continue
        courses.append(Course(
            name=match.group(1),
            start_week=int(match.group(2)),
            end_week=int(match.group(3)),
            start_section=int(match.group(4)),
            end_section=int(match.group(5)),
            teacher=match.group(6),
            room=match.group(7),
            day_of_week=(idx + 1) % 7,
        ))
    return courses
