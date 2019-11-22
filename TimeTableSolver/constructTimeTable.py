import time
import data  # TODO: nog veranderen naar de jusite klasse, waar zit de lijst van alle events?
import hardConstraints
import random
import processInput
import softConstraints
import math


# This function will constructs a feasible solution or a partially feasible solution
# it will also terminate when no solution is found in a specific time span
def construct_time_table():

    # we hold the starting time while processing a time table
    start_construct = time.clock()

    # TODO: de tijd wordt nu hard gecodeerd, dit moet nog veranderen!!!!
    while (len(processInput.events) > 0 or len(processInput.unplaced_events) > 0) and time.clock()-start_construct < 90:

      sorted_courses = order_course_events_by_priority(processInput.courses_dict.values())
      for index, course in enumerate(sorted_courses):
            available_positions = []
            for room, time_slot in processInput.empty_positions:
                fits = hardConstraints.course_fits_in_to_time_slot(course, time_slot) and hardConstraints.room_capacity_constraint(course, room)
                if fits:
                    available_positions.append((room, time_slot))

            #sort available positions
            sorted_positions = order_positions_by_priority(available_positions, course)
            #TODO: nog nagaan of de lijst niet leeg is
            perfect_position = sorted_positions.pop()
            hardConstraints.assign_course_to_position(course, perfect_position)


    return


# This function returns a list of all positions in the timetable that this event can be placed.
def order_positions_by_priority(positions, course):
    positions_ranking = {}

    for room, time_slot in positions:
        positions_ranking[room.fi_number] = []

    for room, time_slot in positions:
        rank1 = get_positions_ranking1(room, course)
        positions_ranking[room.fi_number].append(rank1)
        rank2 = get_positions_ranking2(room, course)
        positions_ranking[room.fi_number].append(rank2)


    sorted_positions = positions
    sorted_positions.sort(key=lambda room, time_slot: positions_ranking[room.fi_number], reverse=False)

    return sorted_positions

def get_positions_ranking2(room, course):
    return softConstraints.return_not_home_penalty(room, course)


def get_positions_ranking1(room, course):
    return room.capacity - course.student_amount


def compute_amount_of_available_time_slots(course):
    """
    :param course: an instance of course
    :return: the total number of available time slots for the given course
    """
    amount = 0
    for i in range(processInput.number_of_time_slots):
        if hardConstraints.course_fits_in_to_time_slot(course, i):
            amount += 1
    return amount


def get_events_ranking1(course, amount_of_events):
    """
    Returns priority based on courses which consist of many lectures,
    but have only a small number of available time slots.
    A smaller value means a higher priority.
    :param course: an instance of course
    :param amount_of_events: number of events that will take place for the given course
    :return: the rank of the given course
    """
    total_number_of_available_time_slots = compute_amount_of_available_time_slots(course)
    rank = total_number_of_available_time_slots / math.sqrt(amount_of_events)
    return rank


def have_common_lecturers(course_a, course_b):
    """
    Checks if the two courses have a common lecturer.
    :param course_a: instance of course
    :param course_b: instance of course
    :return: True if there is at least one common lecturer, False otherwise
    """
    for lecturer in course_a.lecturers:
        if lecturer in course_b.lecturers:
            return True
    return False


def have_common_curricula(course_a, course_b):
    """
    Checks if two courses have a common curriculum
    :param course_a: instance of course
    :param course_b: instance of course
    :return: True if there is at least one common curriculum, False otherwise
    """
    for curriculum in course_a.curricula:
        if curriculum in course_b.curricula:
            return True
    return False


def get_events_ranking2(course, courses):
    """
    Order priority by conflict, a conflict is a course_event with has the same lecturer as another event,
    or is part of the same curriculum of another event.
    :param course: an instance of course
    :param courses: all courses
    :return: the rank of the given course
    """
    amount = 0
    for curr_course in courses:
        if course != curr_course:
            if have_common_lecturers(course, curr_course) or have_common_curricula(course, curr_course):
                amount += 1
    rank = amount
    return rank


def count_lectures_per_course(courses):
    """
    Get the amount of lectures per course.
    :param: a list of courses
    :return: a dictionary containing the amount of course events per course
    """
    lectures_amount = {}
    for course in courses:
        code = course.code
        amount = len(course.course_events)
        lectures_amount[code] = amount
    return lectures_amount


def order_course_events_by_priority(courses):
    """
    Orders the course events by priority,
    events with a higher priority should be scheduled first.
    :return:
    """
    course_ranking = {}

    for course in courses:
        course_ranking[course.code] = []

    lectures_amount = count_lectures_per_course(courses)

    # fill the ranking array with all rankings in descending priority
    for course in courses:
        # highest priority
        # we invert the solution, because the lowest value has the highest priority
        # and we want to order from biggest priority value to smallest
        rank1 = get_events_ranking1(course, lectures_amount[course.code])
        course_ranking[course.code].append(1/rank1
                                           if rank1 != 0
                                           else 0)
        course_ranking[course.code].append(get_events_ranking2(course, courses))

    courses_sorted = list(courses)
    courses_sorted.sort(key=lambda cr: course_ranking[cr.code], reverse=True)
    return courses_sorted



construct_time_table()
#print(len(processInput.courses_dict))
print(processInput.time_table)