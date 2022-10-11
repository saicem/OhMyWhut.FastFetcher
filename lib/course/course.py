import re

from lxml import etree
from lxml.etree import _Element


class Course:
    def __init__(self,
                 name: str,
                 room: str,
                 teacher: str,
                 start_week: int,
                 end_week: int,
                 start_section: int,
                 end_section: int,
                 day_of_week: int):
        """
        课程实例
        :param name: course name
        :param room: course room
        :param start_section: 1,3,6,9,11
        :param end_section: 2,4,5,7,8,10,12,13
        :param day_of_week: 0~6
        """
        self.Name: str = name
        self.Room: str = room
        self.Teacher: str = teacher
        self.StartWeek: int = start_week
        self.EndWeek: int = end_week
        self.StartSection: int = start_section
        self.EndSection: int = end_section
        self.DayOfWeek: int = day_of_week


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
