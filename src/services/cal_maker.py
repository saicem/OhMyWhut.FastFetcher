import io
import uuid
from datetime import datetime, timedelta

from services.course_parser import Course

START_TIME_DIC = {
    1: timedelta(hours=8),
    3: timedelta(hours=9, minutes=55),
    6: timedelta(hours=14),
    9: timedelta(hours=16, minutes=45),
    11: timedelta(hours=19),
}

END_TIME_DIC = {
    2: timedelta(hours=9, minutes=35),
    4: timedelta(hours=11, minutes=30),
    5: timedelta(hours=12, minutes=20),
    7: timedelta(hours=15, minutes=35),
    8: timedelta(hours=15, minutes=25),
    12: timedelta(hours=20, minutes=35),
    13: timedelta(hours=21, minutes=25),
}


def compute_start_day(term_start_day: datetime, week: int, dow: int) -> datetime:
    return term_start_day + ((week - 1) * 7 + (6 if dow == 0 else dow - 1)) * timedelta(
        days=1
    )


class IcalWriter:
    def __init__(self, term_start_date: datetime, courses: list[Course]):
        self.ical = io.StringIO()
        self.courses = courses
        self.term_start_date = term_start_date

    def write_event(self, course: Course):
        start_day = compute_start_day(
            self.term_start_date, course.startWeek, course.dayOfWeek
        )
        date_start = (
            start_day + START_TIME_DIC[course.startSection] - timedelta(hours=8)
        )
        date_end = start_day + END_TIME_DIC[course.endSection] - timedelta(hours=8)
        start_day.strftime("%Y%m%dT%H%M%SZ")
        self.ical.write("BEGIN:VEVENT\n")
        self.ical.write(f"UID:{uuid.uuid4()}\n")
        self.ical.write(f"SUMMARY:{course.name}\n")
        self.ical.write(f"LOCATION:{course.room}\n")
        self.ical.write(f"DESCRIPTION:{course.teacher}\n")
        self.ical.write(f"DTSTART:{date_start.strftime('%Y%m%dT%H%M%SZ')}\n")
        self.ical.write(f"DTEND:{date_end.strftime('%Y%m%dT%H%M%SZ')}\n")
        self.ical.write(
            f"RRULE:FREQ=WEEKLY;INTERVAL=1;COUNT={course.endWeek - course.startWeek + 1}\n"
        )
        self.ical.write("END:VEVENT\n")

    def make_ical_from_course(self):
        self.ical = io.StringIO()
        self.ical.write("BEGIN:VCALENDAR\n")
        self.ical.write("VERSION:2.0\n")
        self.ical.write(f"PRODID:{uuid.uuid4()}\n")
        for course in self.courses:
            self.write_event(course)
        self.ical.write("END:VCALENDAR")
        return self.ical
