"""
生成图片的各种属性配置
"""
import datetime

# border-box
# font
FONT_SIZE = 31
# margin
MARGIN_TOP = 10
MARGIN_RIGHT = 10
MARGIN_BOTTOM = 40
MARGIN_LEFT = 10
# top bar
TOP_BAR_Y = MARGIN_TOP
TOP_BAR_HEIGHT = 40
TOP_BAR_FONT_SIZE = 20
WEEK_ORDER_ANCHOR = (985, 20)
# week bar
WEEK_BAR_Y = TOP_BAR_Y + TOP_BAR_HEIGHT
WEEK_BAR_HEIGHT = 53
WEEK_BAR_FONT_SIZE = 20
DOW_ANCHOR = (56, 8)
DATE_ANCHOR = (52, 29)
# course
COURSE_Y = WEEK_BAR_Y + WEEK_BAR_HEIGHT
COURSE_HEIGHT = 162
COURSE_WIDTH = 150
COURSE_MARGIN = 3
COURSE_RADIUS = 10
COURSE_NAME_ANCHOR = (10, 10)
COURSE_ROOM_ANCHOR = (10, -10)
COURSE_TEXT_MAXLEN = 125
# 三行 (10, -110)
# bottom bar
BOTTOM_Y = COURSE_Y + COURSE_HEIGHT * 13
BOTTOM_HEIGHT = 0
# base
BASE_HEIGHT = BOTTOM_Y + BOTTOM_HEIGHT + MARGIN_BOTTOM
BASE_WIDTH = MARGIN_LEFT + MARGIN_RIGHT + COURSE_WIDTH * 7
# time
WEEK_SPAN = datetime.timedelta(days=7)
DAY_SPAN = datetime.timedelta(days=1)
