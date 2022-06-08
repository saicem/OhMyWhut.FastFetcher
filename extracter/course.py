# 访问 http://202.114.50.130/DailyMgt/jsList.do
from copy import copy
import re
from regex import Match

# 源html文件 用于解析出课程及教室
htmlName = "20212.html"
courseCsv = "course.csv"
roomCsv = "room.csv"


def ParseClassRoom(教室: str):
    res = re.search(r"(.+?)\((.+?)\)-(\d+)", 教室)
    if res is None:
        # return "", "", ""
        return None
    return res, res.group(2), res.group(3)


def getRegion(room: str) -> str:
    if not "(" in room:
        return "其他"
    if "鉴" in room:
        return "鉴湖"
    if "博学" in room:
        return "南湖"
    if "航" in room:
        return "余家头"
    # if "东配楼" in room:
    #     return "余家头"
    if "余" in room:
        return "余家头"
    if "珞樱" in room:
        return "西院"
    if "致远" in room:
        return "东院"
    if "弘毅" in room:
        return "东院"
    return "其他"


class Course:
    def __init__(self) -> None:
        self.选课课号 = ""
        self.开课学院 = ""
        self.课程名称 = ""
        self.课程代码 = ""
        self.教师姓名 = ""
        self.周次 = ""
        self.补选审核 = ""
        self.退选审核 = ""
        self.QQ群号 = ""
        self.学年学期 = ""
        self.周次 = int
        self.开始节 = int
        self.结束节 = int
        self.开始周 = int
        self.结束周 = int
        self.教室号 = ""
        self.教室 = ""
        self.教学楼 = ""
        self.教学楼原名 = ""
        self.校区 = ""


weekDic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}


def ParseCourse(tds: list[Match[str]]) -> Course:
    course = Course()
    course.选课课号 = tds[0]
    course.开课学院 = tds[1]
    course.课程名称 = tds[2]
    course.课程代码 = tds[3]
    course.教师姓名 = re.search(">(.+?)<", tds[4]).group(1)
    course.周次 = tds[5]
    上课时间 = re.findall(".+?<br>", tds[6])
    上课地点 = re.findall(".+?<br>", tds[7])
    course.补选审核 = tds[8]
    course.退选审核 = tds[9]
    course.QQ群号 = tds[10]
    for i in range(len(上课地点)):
        # 过滤不需要的课程
        course.教室 = 上课地点[i].rstrip("<br>")
        course.校区 = getRegion(course.教室)
        if course.校区 == "其他":
            continue
        # 周二第1-2节{第01-02周}<br>
        # 20211-09430
        course.教学楼原名, course.教学楼, course.教室号 = ParseClassRoom(上课地点[i])
        course.学年学期 = re.search("(.+?)-.+?", course.选课课号).group(1)
        时间地点 = re.search("周(.+?)第(.+?)-(.+?)节\{第(.+?)-(.+?)周\}", 上课时间[i])
        course.周次 = weekDic[时间地点.group(1)]
        course.开始节 = int(时间地点.group(2))
        course.结束节 = int(时间地点.group(3))
        course.开始周 = int(时间地点.group(4))
        course.结束周 = int(时间地点.group(5))

        yield copy(course)


def WriteCourseCsv(html: str):
    courses: list[Course] = []
    csvCourse = open(courseCsv, "w", encoding="utf-8")
    trs = re.findall("<tr.+?>(.+?)</tr>", html, re.S)
    for tr in trs:
        tds = re.findall("<td.*?>(.*?)</td>", tr, re.S)
        courses += list(ParseCourse(tds))

    csvCourse.write("课程代码,课程名称,教师姓名,教室,开始周,结束周,开始节,结束节,周次,学年学期\n")

    for course in courses:
        csvCourse.write(
            "{},{},{},{},{},{},{},{},{},{}\n".format(
                course.课程代码,
                course.课程名称,
                course.教师姓名,
                course.教室,
                course.开始周,
                course.结束周,
                course.开始节,
                course.结束节,
                course.周次,
                course.学年学期,
            )
        )

    csvCourse.close()
    return courses


def WriteRoomCsv(courses: list[Course]):
    csvRoom = open(roomCsv, "w", encoding="utf-8")
    csvRoom.write("校区,教学楼原名,教学楼新名,楼层,教室号,全称\n")
    for course in courses:
        csvRoom.write(
            "{},{},{},{},{},{}\n".format(
                course.校区,
                course.教学楼原名,
                course.教学楼,
                course.教室号[0],
                course.教室号,
                course.教室,
            )
        )
    csvRoom.close()


if __name__ == "__main__":
    html = open(htmlName, "r", encoding="utf-8").read()
    html = html.replace("\n", "")
    html = re.sub("\s+", " ", html)
    courses = WriteCourseCsv(html)
    WriteRoomCsv(courses)
