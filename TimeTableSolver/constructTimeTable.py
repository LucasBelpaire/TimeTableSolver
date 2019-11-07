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

        # Construct a time table with the remaining events
        events_size = len(processInput.events)
        for index in range(events_size):
            # get an event from the list and look if we can place it on a position
            current_event = processInput.events.pop()
            all_av_positions = order_positions_by_priority(current_event)
            # if this list of positions is empty, than we didn't find a place to put this event
            # so now we change this event from unassigned to unplaced
            if not all_av_positions:
                processInput.unplaced_events.append(current_event)
            else:
                hardConstraints.assign_course_to_position(current_event, all_av_positions[0])

        unplaced_events_size = len(processInput.unplaced_events)

        new_positions = []
        
        # The following lines of code will remove some random events that are already placed in the timetable
        # all the unplaced_events couldn't be assinged to any open position in the timetable
        # so it is necessary to create new open positions by randomly removing events.
        for index in range(unplaced_events_size):
            random_position = random.choice(processInput.forbidden_positions)
            current_random_event = hardConstraints.remove_event_at_position(random_position)
            processInput.forbidden_positions.remove(random_position)
            processInput.events.append(current_random_event)
            new_positions.append(random_position)

        # The next for loop will try to assign some unplaced events in the free timeslot in the timetable
        for index in range(unplaced_events_size):
            current_unplaced_event = processInput.unplaced_events.pop()
            is_assigned = False
            for pos in new_positions:
                if hardConstraints.course_fits_in_to_time_slot(current_unplaced_event, pos[1]):
                    hardConstraints.assign_course_to_position(current_unplaced_event, pos)
                    new_positions.remove(pos)
                    is_assigned = True
                    break
            if not is_assigned:
                processInput.events.append(current_unplaced_event)

    return len(processInput.events)


# This function returns a list of all positions in the timetable that this event can be placed.
def order_positions_by_priority(event):
    # !!!!! pagina 34 voor pseudo code !!!!!

    # Hard_pos is a list that contains positions that don't violate the hard constraints
    hard_pos = []

    # feasible_pos is a list with positions with penalties from the soft constraints
    feasible_pos = []

    # TODO: hoe hervormen we deze functie?
    for position in processInput.empty_positions:
        if softConstraints.does_course_fits_in_position(event, position):
            # TODO:afwerken
            return False
        elif hardConstraints.course_fits_in_to_time_slot(event, position[1]):
            # TODO:afwerken
            return False

    all_possible_pos = hard_pos + feasible_pos
    return all_possible_pos


def compute_amount_of_available_time_slots(course):
    """
    :param course: an instance of course
    :return: the total number of available time slots for the given course
    """
    amount = 0
    for i in range(processInput.number_of_time_slots):
        for room in processInput.class_rooms_dict.values():
            if hardConstraints.course_fits_in_to_time_slot(course, i, room):
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
        course_ranking[course.code].append(1/get_events_ranking1(course, lectures_amount[course.code])
                                           if get_events_ranking1(course, lectures_amount[course.code]) != 0
                                           else 0)
        course_ranking[course.code].append(get_events_ranking2(course, courses))

    courses_sorted = list(courses)
    courses_sorted.sort(key=lambda cr: course_ranking[cr.code])
    for c in courses_sorted:
        print(c.code)

    print(course_ranking['B001352A'])
    print(course_ranking['H002121A'])
    print(course_ranking['H001719A'])
    print(course_ranking['I001035A'])
    print(course_ranking['C003119A'])


order_course_events_by_priority(processInput.courses_dict.values())
