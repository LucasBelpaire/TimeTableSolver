import json
import data

path = "datasets/project.json"

# load in the json file
with open(path, 'r') as f:
    project_json = json.load(f)

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
        lecturers.append(new_lecturer)
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
    courses_dict[code] = new_course

# transform all sites into objects and save them into dictionary
# do the same for classrooms
sites_dict = {}
classrooms_dict = {}
for site in project_json['sites']:
    code = site['code']
    name = site['naam']
    x_coord = site['xcoord']
    y_coord = site['ycoord']
    class_rooms = []
    for classroom in site['lokalen']:
        fi_number = classroom['finummer']
        if fi_number not in classrooms_dict:
            classroom_name = classroom['naam']
            capacity = classroom['capaciteit']
            new_classroom = data.ClassRoom(fi_number=fi_number,
                                           name=classroom_name,
                                           capacity=capacity)
        else:
            new_classroom = classrooms_dict[fi_number]
        class_rooms.append(new_classroom)
    new_site = data.Site(code=code,
                         name=name,
                         x_coord=x_coord,
                         y_coord=y_coord,
                         class_rooms=class_rooms)


# TODO: de events nog aanmaken
events = []

# all events that couldn't be placed in the construct phase
unplaced_events = []

# this list will contain all positions that already have been assinged to a event
forbidden_positions = []