class GeneralInfo:
    def __init__(self, academy_year, semester, kilometer_penalty,
                 late_hours_penalty, not_home_penalty, min_amount_students):
        self.academy_year = academy_year
        self.semester = semester
        self.kilometer_penalty = kilometer_penalty
        self.late_hour_penalty = late_hours_penalty
        self.not_home_penalty = not_home_penalty
        self.min_amount_students = min_amount_students
        self.course_hours = {1: "08u30-10u00",
                             2: "10u00-11u30",
                             3: "11u30-13u00",
                             4: "13u00-14u30",
                             5: "14u30-16u00",
                             6: "16u00-17u30",
                             7: "17u30-19u00",
                             8: "19u00-20u30"}
        self.weeks = 13


class Course:
    def __init__(self, code, name, student_amount, contact_hours, lecturers, curricula):
        self.code = code
        self.name = name
        self.student_amount = student_amount
        self.contact_hours = contact_hours
        self.real_hours = contact_hours*0.8
        self.lecturers = lecturers
        self.curricula = curricula


class Lecturer:
    def __init__(self, ugent_id, first_name, last_name):
        self.ugent_id = ugent_id
        self.first_name = first_name
        self.last_name = last_name


class Curriculum:
    def __init__(self, code, mt1, home_site):
        self.code = code
        self.mt1 = mt1
        self.home_site = home_site


class Site:
    def __init__(self, code, name, x_coord, y_coord, class_rooms):
        self.code = code
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.class_rooms = class_rooms


class ClassRoom:
    def __init__(self, fi_number, name, capacity):
        self.fi_number = fi_number
        self.name = name
        self.capacity = capacity


class CourseEvent:
    def __init__(self, course, course_hours, class_room, days, weeks):
        self.course = course
        self.course_hours = course_hours
        self.class_room = class_room
        self.days = days
        self.weeks = weeks
