from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from src.services.course_parser import Course
from src.services.course_png.util import *


class CourseDrawer:
    def __init__(
            self,
            courses: list[Course],
            week_order: int,
            term_start_day: datetime,
            font: FreeTypeFont = ImageFont.load_default()
    ):
        self.__term_start_day = term_start_day
        self.__image = Image.new("RGBA", (BASE_WIDTH, BASE_HEIGHT), (255, 255, 255))
        self.__image_draw = ImageDraw.Draw(self.__image)
        self.__week_order = week_order
        self.__courses = courses
        self.__font = font

    def __draw_top_bar(self):
        self.__image_draw.text(
            WEEK_ORDER_ANCHOR,
            get_week_order_name(self.__week_order),
            font=self.__font,
            fill=(12, 12, 12),
        )

    def __draw_week_bar(self):
        x0 = MARGIN_LEFT
        y0 = WEEK_BAR_Y
        for idx, name in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            self.__image_draw.text(
                (x0 + DOW_ANCHOR[0], y0 + DOW_ANCHOR[1]),
                name,
                font=self.__font,
                fill=(0, 0, 0),
            )
            self.__image_draw.text(
                (x0 + DATE_ANCHOR[0], y0 + DATE_ANCHOR[1]),
                get_date(self.__week_order, idx + 1, self.__term_start_day),
                font=self.__font,
                fill=(0, 0, 0),
            )
            x0 += COURSE_WIDTH

    # 绘制某个课表格子 起始点 (x,y) 结束点 (x,y)
    def __draw_course(self, course_box_xy: tuple[int, int, int, int], course: Course):
        self.__image_draw.rounded_rectangle(
            xy=course_box_xy,
            radius=COURSE_RADIUS,
            outline=(255, 255, 255),
            fill=get_color(course.DayOfWeek),
            width=2,
        )
        self.__draw_text_course_name(
            course.Name,
            (
                course_box_xy[0] + COURSE_NAME_ANCHOR[0],
                course_box_xy[1] + COURSE_NAME_ANCHOR[1],
            ),
        )
        self.__draw_text_course_place(
            course.Room,
            (
                course_box_xy[0] + COURSE_ROOM_ANCHOR[0],
                course_box_xy[3] + COURSE_ROOM_ANCHOR[1],
            ),
        )

    def __draw_courses(self):
        for course in self.__courses:
            self.__draw_course(
                get_course_coordinate(
                    course.DayOfWeek,
                    course.StartSection,
                    course.EndSection
                ),
                course,
            )

    # 渲染课程名称
    def __draw_text_course_name(
            self, text: str, anchor
    ) -> None:
        draw_text = self.format_text(text)
        self.__image_draw.text(
            (anchor[0], anchor[1]),
            draw_text,
            font=self.__font,
        )

    def format_text(self, text: str) -> str:
        length = len(text)
        if len(text) <= 1:
            return text
        texts = []
        left: int = 0
        right: int = 1
        while 1:
            if right == length:
                texts.append(text[left:right])
                break
            if self.__font.getlength(text[left: right + 1]) > COURSE_TEXT_MAXLEN:
                texts.append(text[left:right])
                left = right
            right += 1
        return "\n".join(texts)

    # https://www.osgeo.cn/pillow/reference/ImageFont.html
    # 上课地点信息格式化
    def __draw_text_course_place(
            self, text: str, anchor
    ) -> None:
        text = self.format_text(text)
        _, compensate_height = self.__font.getsize_multiline(text)
        self.__image_draw.text(
            (anchor[0], anchor[1] - compensate_height),
            text,
            font=self.__font,
        )

    def draw(self) -> Image:
        self.__draw_top_bar()
        self.__draw_week_bar()
        self.__draw_courses()
        return self.__image
