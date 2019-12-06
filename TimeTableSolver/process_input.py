import json
import data
import copy
import math
import general_info as gi


path = "datasets/project.json"

# load in the json file
with open(path, 'r') as f:
    project_json = json.load(f)

number_of_time_slots = 40
# get general info out of the json file
academy_year = project_json['academiejaar']
semester = project_json['semester']
not_home_penalty = project_json['nothomepenalty']
kilometer_penalty = project_json['kilometerpenalty']
late_hours_penalty = project_json['lateurenkost']
min_amount_student = project_json['minimaalStudentenaantal']

# transform all courses into course objects and save them into a dictionary
# do the same for the lecturers and curricula
courses_dict = {}
lecturers_dict = {}
curricula_dict = {}
for course in project_json['vakken']:
    code = course['code']
    name = course['cursusnaam']
    student_amounts = int(course['studenten'])

    contact_hours = course['contacturen']
    if contact_hours >= 75 or contact_hours is 0:
        continue
    if student_amounts < int(min_amount_student):
        student_amounts = int(min_amount_student)
    lecturers = []
    for lecturer in course['lesgevers']:
        ugent_id = lecturer['UGentid']
        if ugent_id not in lecturers_dict:
            first_name = lecturer['voornaam']
            last_name = lecturer['naam']
            new_lecturer = data.Lecturer(ugent_id=ugent_id,
                                         first_name=first_name,
                                         last_name=last_name)
            lecturers_dict[ugent_id] = new_lecturer
        else:
            new_lecturer = lecturers_dict[ugent_id]
        lecturers.append(ugent_id)
    curricula = []
    for curriculum in course['programmas']:
        curriculum_code = curriculum['code']
        if curriculum_code not in curricula_dict:
            mt1 = curriculum['mt1']
            home_site = curriculum['homesite']
            new_curriculum = data.Curriculum(code=curriculum_code,
                                             mt1=mt1,
                                             home_site=home_site)
            curricula_dict[curriculum_code] = new_curriculum
        else:
            new_curriculum = curricula_dict[curriculum_code]
        curricula.append(new_curriculum)
    new_course = data.Course(code=code,
                             name=name,
                             student_amount=student_amounts,
                             contact_hours=contact_hours,
                             lecturers=lecturers,
                             curricula=curricula)
    if len(curricula) == 0:
        continue
    courses_dict[code] = new_course

# transform all sites into objects and save them into dictionary
# do the same for classrooms
sites_dict = {}
class_rooms_dict = {}
biggest_room_capacity = 0
for site in project_json['sites']:
    code = site['code']
    name = site['naam']
    x_coord = site['xcoord']
    y_coord = site['ycoord']
    class_rooms = []
    for classroom in site['lokalen']:
        fi_number = classroom['finummer']
        if fi_number not in class_rooms_dict:
            classroom_name = classroom['naam']
            capacity = classroom['capaciteit']
            if int(capacity) > biggest_room_capacity:
                biggest_room_capacity = int(capacity)
            new_classroom = data.ClassRoom(fi_number=fi_number,
                                           name=classroom_name,
                                           capacity=capacity,
                                           site_id=code)
            class_rooms_dict[fi_number] = new_classroom
        else:
            new_classroom = class_rooms_dict[fi_number]
        class_rooms.append(new_classroom)
    new_site = data.Site(code=code,
                         name=name,
                         x_coord=x_coord,
                         y_coord=y_coord,
                         class_rooms=class_rooms)
    if new_site not in sites_dict:
        sites_dict[new_site.code] = new_site


def create_course_events(c):
    course_events = []
    for i in range(int(c.course_hours)):
        course_event = data.CourseEvent(course_code=c.code,
                                        lecturers=c.lecturers,
                                        student_amount=c.student_amount,
                                        curricula=c.curricula,
                                        event_number=i)
        course_events.append(course_event)
    return course_events


courses_set = set()


def create_initial_events_lists():
    events_type_1 = []
    events_type_2 = []
    events_type_3 = []
    events_type_4 = []
    for c in courses_dict.values():
        courses_set.add(c)
        course_hours = c.course_hours

        if c.course_hours / 12 >= 1:
            c.course_hours = math.ceil(course_hours/12)
            events = create_course_events(c)
            events_type_1 += events
        elif c.course_hours / 6 >= 1:
            c.course_hours = math.ceil(course_hours / 6)
            events = create_course_events(c)
            events_type_2 += events
        elif c.course_hours / 3 >= 1:
            c.course_hours = math.ceil(course_hours / 3)
            events = create_course_events(c)
            events_type_3 += events
        elif c.course_hours / 1 >= 1:
            c.course_hours = math.ceil(course_hours / 1)
            events = create_course_events(c)
            events_type_4 += events

    return events_type_1, events_type_2, events_type_3, events_type_4


def create_initial_timetable():
    time_table = {}
    empty_positions = []
    for room in class_rooms_dict.values():
        for time_slot in range(number_of_time_slots):
            room_fi_number = room.fi_number
            empty_positions.append((room_fi_number, time_slot))
            time_table[(room_fi_number, time_slot)] = None
    timetable = data.TimeTable(timetable=time_table,
                               occupied_positions=[],
                               empty_positions=empty_positions)
    return timetable


def init_general_info():
    """
    this method will set the value of all variables in the generalInfo module.
    These values depend on the input processed in this module.
    """
    gi.academy_year = academy_year
    gi.semester = semester
    gi.kilometer_penalty = float(kilometer_penalty)
    gi.late_hour_penalty = float(late_hours_penalty)
    gi.not_home_penalty = float(not_home_penalty)
    gi.min_amount_students = int(min_amount_student)
    gi.biggest_room_capacity = int(biggest_room_capacity)

    gi.courses_set = courses_set
    gi.courses_dict = courses_dict
    gi.lecturers_dict = lecturers_dict
    gi.curricula_dict = curricula_dict
    gi.sites_dict = sites_dict
    gi.class_rooms_dict = class_rooms_dict

