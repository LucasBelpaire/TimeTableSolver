import time
import data  # TODO: nog veranderen naar de jusite klasse, waar zit de lijst van alle events?
import hardConstraints
import random
import processInput
import softConstraints
import math


def initialize_time_table_variables():
    """
    This function initializes all variables that are needed to construct the time table.
    The value of variables depend on the input that gets processed by the processInput script.
    :return: events_type1, events_type2, time_table, empty_positions, courses_type_1, courses_type_2
    """
    events_type_1 = []  # All course events with courses that have more than or equal to 2 course hours per week
    courses_type_1 = set() # All courses with more than 2 course hours per week
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
    return events_type_1, events_type_2, time_table, empty_positions, courses_type_1, courses_type_2


# This function will constructs a feasible solution or a partially feasible solution
# it will also terminate when no solution is found in a specific time span
def construct_time_table():
    events_type1, events_type2, time_table, empty_positions, \
                                courses_type_1, courses_type_2 = initialize_time_table_variables()
    unplaced_events = []  # all events that couldn't be placed in the construct phase
    forbidden_positions = []  # this list will contain all positions that already have been assigned to a event

    # TODO: de tijd wordt nu hard gecodeerd, dit moet nog veranderen!!!!
    start_construct = time.clock()
    while time.clock() - start_construct < 10000:
        sorted_events = order_course_events_by_priority(events_type1, courses_type_1)
        for index, course_event in enumerate(sorted_events):
            available_positions = []

            for room, time_slot in empty_positions:
                fits = hardConstraints.course_event_fits_in_to_time_slot(course_event, time_slot) \
                       and hardConstraints.room_capacity_constraint(course_event, room)
                if fits:
                    available_positions.append((room, time_slot))
            print(len(available_positions))
            # sort available positions
            sorted_positions = order_positions_by_priority(available_positions, course_event)
            # TODO: nog nagaan of de lijst niet leeg is
            if len(sorted_positions) == 0:
                print("new unplaced course:" + course_event.code)
                unplaced_events.append(course_event)
                continue
            perfect_position = sorted_positions.pop()
            assign_course_to_position(course_event, perfect_position)


# This function returns a list of all positions in the timetable that this event can be placed.
def order_positions_by_priority(positions, course_event):
    positions_ranking = {}

    for room, time_slot in positions:
        positions_ranking[room.fi_number] = []

    for room, time_slot in positions:
        rank1 = get_positions_ranking1(room, course_event)
        positions_ranking[room.fi_number].append(rank1)
        rank2 = get_positions_ranking2(room, course_event)
        positions_ranking[room.fi_number].append(rank2)

    sorted_positions = positions
    sorted_positions.sort(key=lambda tup: positions_ranking[tup[0].fi_number], reverse=False)

    return sorted_positions


def get_positions_ranking2(room, course_event):
    return softConstraints.return_not_home_penalty(room, course_event)


def get_positions_ranking1(room, course_event):
    return room.capacity - course_event.student_amount


def compute_amount_of_available_time_slots(course_event):
    """
    :param course_event: an instance of course event
    :return: the total number of available time slots for the given course
    """
    amount = 0
    for i in range(40):
        if hardConstraints.course_event_fits_in_to_time_slot(course_event, i):
            amount += 1
    return amount


def get_events_ranking1(course_event, amount_of_events):
    """
    Returns priority based on courses which consist of many lectures,
    but have only a small number of available time slots.
    A smaller value means a higher priority.
    :param course_event: an instance of course event
    :param amount_of_events: number of events that will take place for the given course
    :return: the rank of the given course
    """
    total_number_of_available_time_slots = compute_amount_of_available_time_slots(course_event)
    rank = total_number_of_available_time_slots / math.sqrt(amount_of_events)
    return rank


def have_common_lecturers(course_event, course):
    """
    Checks if the two courses have a common lecturer.
    :param course_event: instance of course
    :param course: instance of course
    :return: True if there is at least one common lecturer, False otherwise
    """
    for lecturer in course_event.lecturers:
        if lecturer in course.lecturers:
            return True
    return False


def have_common_curricula(course_event, course):
    """
    Checks if two courses have a common curriculum
    :param course_event: instance of course event
    :param course: instance of course
    :return: True if there is at least one common curriculum, False otherwise
    """
    for curriculum in course_event.curricula:
        if curriculum in course.curricula:
            return True
    return False


def get_events_ranking2(course_event, courses):
    """
    Order priority by conflict, a conflict is a course_event with has the same lecturer as another event,
    or is part of the same curriculum of another event.
    :param course_event: an instance of course event
    :param courses: all courses
    :return: the rank of the given course
    """
    amount = 0
    for curr_course in courses:
        if course_event.course_code != curr_course.code:
            if have_common_lecturers(course_event, curr_course) or have_common_curricula(course_event, curr_course):
                amount += 1
    rank = amount
    return rank


def count_lectures_per_course(course_events):
    """
    Get the amount of lectures per course.
    :param: a list of course events
    :return: a dictionary containing the amount of course events per course
    """
    lectures_amount = {}
    for course_event in course_events:
        code = course_event.course_code
        amount = len(processInput.courses_dict[code].course_events)
        lectures_amount[code] = amount
    return lectures_amount


def order_course_events_by_priority(course_events, courses):
    """
    Orders the course events by priority,
    events with a higher priority should be scheduled first.
    :return: the sorted list of events
    """
    course_events_ranking = {}

    for event in course_events:
        course_events_ranking[event.code] = []

    lectures_amount = count_lectures_per_course(course_events)

    # fill the ranking array with all rankings in descending priority
    for course_event in course_events:
        # highest priority
        # we invert the solution, because the lowest value has the highest priority
        # and we want to order from biggest priority value to smallest
        rank1 = get_events_ranking1(course_event, lectures_amount[course_event.course_code])
        course_events_ranking[course_event.course_code].append(1/rank1
                                           if rank1 != 0
                                           else 0)
        course_events_ranking[course_event.course_code].append(get_events_ranking2(course_event, list(courses)))

    courses_sorted = list(courses)
    courses_sorted.sort(key=lambda cr: course_events_ranking[cr.code], reverse=True)
    return courses_sorted



construct_time_table()
#print(len(processInput.courses_dict))
count = 0
for key, value in processInput.time_table.items():
    if value is not None:
        print(key[0].fi_number, key[1], value.code)
        count += 1

print(count)
print(len(processInput.unplaced_events))