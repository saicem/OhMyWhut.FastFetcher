class Course:
    def __init__(
            self,
            name: str,
            room: str,
            teacher: str,
            start_week: int,
            end_week: int,
            start_section: int,
            end_section: int,
            day_of_week: int,
    ):
        """
        课程实例
        :param name: course name
        :param room: course room
        :param start_section: 1,3,6,9,11
        :param end_section: 2,4,5,7,8,10,12,13
        :param day_of_week: 0~6
        """
        self.name: str = name
        self.room: str = room
        self.teacher: str = teacher
        self.startWeek: int = start_week
        self.endWeek: int = end_week
        self.startSection: int = start_section
        self.endSection: int = end_section
        self.dayOfWeek: int = day_of_week
