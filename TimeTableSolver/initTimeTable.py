import processInput
import data

"""
    This script initializes all variables that are needed to construct the time table.
    The value of variables depend on the input that gets processed by the processInput script.
    :return: events_type1, events_type2, time_table, empty_positions, courses_type_1, courses_type_2
    """
events_type_1 = []  # All course events with courses that have more than or equal to 2 course hours per week
courses_type_1 = set()  # All courses with more than 2 course hours per week
events_type_2 = []  # course events with courses that have less than 2 course hours per week
courses_type_2 = set()  # All courses with less than 2 course hours per week
for course in processInput.courses_dict.values():
    course_events = []
    for i in range(int(course.course_hours)):
        course_event = data.CourseEvent(course_code=course.code,
                                        lecturers=course.lecturers,
                                        student_amount=course.student_amount,
                                        curricula=course.curricula,
                                        event_number=i)
        course_events.append(course_event)
    if len(course_events) >= 2:
        events_type_1 += course_events
        courses_type_1.add(course)
        continue
    events_type_2 += course_events
    courses_type_2.add(course)

number_of_time_slots = 40  # amount of possible course hours per week
time_table = {}
empty_positions = []
for room in processInput.class_rooms_dict.values():
    for time_slot in range(number_of_time_slots):
        room_fi_number = room.fi_number
        empty_positions.append((room, time_slot))
        time_table[(room_fi_number, time_slot)] = None
