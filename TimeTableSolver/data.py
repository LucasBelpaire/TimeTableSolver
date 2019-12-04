import math
import copy


class GeneralInfo:
    def __init__(self, academy_year, semester, kilometer_penalty,
                 late_hours_penalty, not_home_penalty, min_amount_students, biggest_room_capacity):
        self.academy_year = academy_year
        self.semester = semester
        self.kilometer_penalty = kilometer_penalty
        self.late_hour_penalty = late_hours_penalty
        self.not_home_penalty = not_home_penalty
        self.min_amount_students = min_amount_students
        self.biggest_room_capacity = biggest_room_capacity
        self.total_course_hours = 40
        self.weeks = 13


class Course:
    def __init__(self, code, name, student_amount, contact_hours, lecturers, curricula):
        self.code = code
        self.name = name
        self.student_amount = int(student_amount)
        self.contact_hours = contact_hours
        self.course_hours = math.ceil(contact_hours*0.8 / 12)
        self.lecturers = lecturers
        self.curricula = curricula
        self.course_events = []


class Lecturer:
    def __init__(self, ugent_id, first_name, last_name):
        self.ugent_id = ugent_id
        self.first_name = first_name
        self.last_name = last_name
        self.occupied_time_slots = []

    def add_occupied_time_slot(self, time_slot_number):
        if time_slot_number in self.occupied_time_slots:
            return False
        self.occupied_time_slots.append(time_slot_number)
        return True

    def remove_occupied_time_slot(self, time_slot_number):
        try:
            self.occupied_time_slots.remove(time_slot_number)
            return True
        except ValueError:
            return False

    def contains_time_slot(self, time_slot_number):
        return time_slot_number in self.occupied_time_slots


class Curriculum:
    def __init__(self, code, mt1, home_site):
        self.code = code
        self.mt1 = mt1
        self.home_site = home_site
        self.occupied_time_slots = []

    def add_occupied_time_slot(self, time_slot_number):
        if time_slot_number in self.occupied_time_slots:
            return False
        self.occupied_time_slots.append(time_slot_number)
        return True

    def remove_occupied_time_slot(self, time_slot_number):
        try:
            self.occupied_time_slots.remove(time_slot_number)
            return True
        except ValueError:
            return False

    def contains_time_slot(self, time_slot_number):
        return time_slot_number in self.occupied_time_slots


class Site:
    def __init__(self, code, name, x_coord, y_coord, class_rooms):
        self.code = code
        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.class_rooms = class_rooms


class ClassRoom:
    def __init__(self, fi_number, name, capacity, site_id):
        self.fi_number = fi_number
        self.name = name
        self.capacity = int(capacity)
        self.site_id = site_id


class CourseEvent:
    def __init__(self, course_code, lecturers, student_amount, curricula, event_number):
        self.course_code = course_code
        self.lecturers = lecturers
        self.student_amount = student_amount
        self.curricula = curricula
        self.event_number = event_number
        self.assigned_lecturer = None

    def set_assigned_lecturer(self, ugent_id):
        if self.assigned_lecturer is None:
            self.assigned_lecturer = copy.deepcopy(ugent_id)
            return True
        return False

    def remove_assigned_lecturer(self):
        self.assigned_lecturer = None
