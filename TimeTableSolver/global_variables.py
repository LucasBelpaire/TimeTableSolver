import random
"""
    This module holds all variables which the different parts of the program need.
"""

# Variables:
events = []  # events is a list of all course events
courses_set = set()  # a set containing all course objects
time_table = {}  # the TT is represented by a dictionary. key: (room_fi_number, time_slot)
number_of_time_slots = None  # amount of possible course hours per week
empty_positions = []  # holds all empty positions, consists of (room_fi_number, time_slot)
unplaced_events = []  # will hold all events that could not be placed.
generalInfo = None  # Object that will hold all general/meta information
initial_construct_time = 90

# Mappings:
courses_dict = {}  # key: (course)code. value: course object
lecturers_dict = {}  # key: ugent_id, value: lecturer object
curricula_dict = {}  # key: (curriculum)code. value: curriculum object
sites_dict = {}  # key: site_id. value: site object
class_rooms_dict = {}  # key: fi_number. value: class_room object


"""
Functions that will alter the time table.
"""


def assign_course_to_position(course_event, position):
    """
    This function will assign a course_event to a specific position in the time table.
    :param course_event: instance of CourseEvent, the course event that will be scheduled.
    :param position: (fi_number, time_slot)
    :return: True if the event is successfully scheduled, False otherwise
    """

    time_table[position] = course_event
    course = courses_dict[course_event.course_code]
    room_fi_number = position[0]
    time_slot = position[1]

    for curriculum in course.curricula:
        # adding the time_slot to the list of occupied time_slots
        curriculum.add_occupied_time_slot(time_slot)

    lecturers = course.lecturers
    random.shuffle(lecturers)
    chosen_lecturer = lecturers[0]

    chosen_lecturer.add_occupied_time_slot(time_slot)
    course_event.set_assigned_lecturer(chosen_lecturer)

    course.course_hours -= 1
    events.remove(course_event)
    empty_positions.remove(position)


def remove_course_from_position(position):
    """
    This function will remove a courseEvent from the timetable.
    :param position: (fi_number, time_slot)
    :return: True if the removal is successful, False otherwise
    """
    fi_number = position[0]
    time_slot = position[1]
    if time_table[position] is not None:
        course_event = time_table[position]
        time_table[position] = None
        empty_positions.append(position)

        course = courses_dict[course_event.course_code]
        course.course_hours += 1

        # remove the time_slot from the occupied time_sot list from every curriculum
        for curriculum in course.curricula:
            curriculum.remove_occupied_time_slot(time_slot)

        assigned_lecturer = course_event.assigned_lecturer
        assigned_lecturer.remove_occupied_time_slot(time_slot)
        course_event.remove_assigned_lecturer()

        return True

    return False
