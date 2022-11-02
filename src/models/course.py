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