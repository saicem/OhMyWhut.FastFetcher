import textwrap

from PIL.ImageFont import FreeTypeFont

from lib.course.config import *


# 获取要绘制的课表格子的坐标
def get_course_coordinate(
        day_of_week: int, start_section: int, end_section: int
) -> tuple[int, int, int, int]:
    # 周日为 0 但周日要排在最后
    x0 = MARGIN_LEFT + COURSE_WIDTH * (6 if day_of_week == 0 else day_of_week - 1)
    y0 = COURSE_Y + COURSE_HEIGHT * (start_section - 1)
    x1 = x0 + COURSE_WIDTH
    y1 = y0 + (end_section - start_section + 1) * COURSE_HEIGHT
    # 课表格子间取间距
    x0 += COURSE_MARGIN
    y0 += COURSE_MARGIN
    x1 -= COURSE_MARGIN
    y1 -= COURSE_MARGIN
    return x0, y0, x1, y1





def get_week_order_name(week_order: int):
    dic = {
        1: "第一周",
        2: "第二周",
        3: "第三周",
        4: "第四周",
        5: "第五周",
        6: "第六周",
        7: "第七周",
        8: "第八周",
        9: "第九周",
        10: "第十周",
        11: "第十一周",
        12: "第十二周",
        13: "第十三周",
        14: "第十四周",
        15: "第十五周",
        16: "第十六周",
        17: "第十七周",
        18: "第十八周",
        19: "第十九周",
        20: "第二十周",
    }
    return dic[week_order]


def get_date(week: int, dow_order: int, term_start_day: datetime):
    """
    依据 周 和 星期来计算日期
    :param term_start_day: 开学第一天
    :param week: 开学第几周
    :param dow_order: 周几 1-7
    :return: 日期字符串
    """
    target_date = term_start_day + (week - 1) * WEEK_SPAN + (dow_order - 1) * DAY_SPAN
    return "{}-{}".format(target_date.month, target_date.day)


def name_format(text: str, n: int) -> str:
    return textwrap.fill(text, width=n)


# 获取颜色:
def get_color(i: int):
    color_ls = [
        (255, 168, 64, 255),
        (57, 211, 169, 255),
        (254, 134, 147, 255),
        (111, 137, 226, 255),
        # (239, 130, 109, 255),
        (99, 186, 255, 255),
        (254, 212, 64, 255),
        (184, 150, 230, 255),
        (169, 213, 59, 255),
    ]
    return color_ls[i]
