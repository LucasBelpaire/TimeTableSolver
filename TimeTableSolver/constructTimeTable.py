import time
import data
import hardConstraints
import random
import processInput
import softConstraints
import math
import initTimeTable


# This function will constructs a feasible solution or a partially feasible solution
# it will also terminate when no solution is found in a specific time span
def construct_time_table():

    unplaced_events = []  # all events that couldn't be placed in the construct phase
    forbidden_positions = []  # this list will contain all positions that already have been assigned to a event

    # TODO: de tijd wordt nu hard gecodeerd, dit moet nog veranderen!!!!
    start_construct = time.clock()

    while time.clock() - start_construct < 10:

        sorted_events = order_course_events_by_priority(initTimeTable.events_type_1, initTimeTable.courses_type_1)
        for index, course_event in enumerate(sorted_events):
            available_positions = []

            for room, time_slot in initTimeTable.empty_positions:
                fits = hardConstraints.course_event_fits_in_to_time_slot(course_event, time_slot) \
                       and hardConstraints.room_capacity_constraint(course_event, room)
                if fits:
                    available_positions.append((room, time_slot))


            # printing some info of the current course_event
            #print(course_event.course_code)
            #print(processInput.courses_dict[course_event.course_code].course_hours)
            # sort available positions
            sorted_positions = order_positions_by_priority(available_positions, course_event)

            if len(sorted_positions) == 0:
                print("new unplaced course:" + course_event.course_code)
                unplaced_events.append(course_event)
                if int(course_event.student_amount) > processInput.biggest_room_capacity:
                    print("To many students, no room large enough")
                    #TODO: dit event opsplitsen in twee
                else:
                    print("Hard constraint violation")
                continue
            perfect_position = sorted_positions.pop(0)
            assign_course_to_position(course_event, perfect_position)

    return unplaced_events

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


def get_positions_ranking1(room, course_event):
    return softConstraints.return_not_home_penalty(room, course_event)


def get_positions_ranking2(room, course_event):
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
        amount = processInput.courses_dict[code].course_hours
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
        course_events_ranking[event.course_code] = []

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

    courses_sorted = list(course_events)
    courses_sorted.sort(key=lambda cr: course_events_ranking[cr.course_code], reverse=True)
    return courses_sorted



def assign_course_to_position(course_event, position):
    '''
    This function will assign a course_event to a specific position in the time table
    :param course_event: the fist parameter is the course_event we want to schedule
    :param position: the second is the specific place inside the time table
    :return: we return true if successful otherwise false
    '''

    initTimeTable.time_table[position] = course_event
    course = processInput.courses_dict[course_event.course_code]

    for curriculum in course.curricula:
        #adding the time_slot to the list of occupied time_slots
        curriculum.add_occupied_time_slot(position[1])

    assigned_lecturer_count_time_slots = 100000
    assigned_lecturer = None
    #the lecturer with the fewest time_slots will be assigned the course_event
    for lecturer in course.lecturers:
        #adding the time_slot to the list of occupied time_slots
        if len(lecturer.occupied_time_slots) <= assigned_lecturer_count_time_slots:
            assigned_lecturer = lecturer
    #assing the the time_slot to the lecturer we picked above
    assigned_lecturer.add_occupied_time_slot(position[1])
    #for this course_event we assignt the above lecturer
    course_event.set_assigned_lecturer(assigned_lecturer)

    course.course_hours -= 1
    initTimeTable.events_type_1.remove(course_event)
    initTimeTable.empty_positions.remove(position)


def remove_course_from_position(course_event, position):
    '''
    This function will remove a course from the specific position
    :param course_event: the course we want to remove
    :param position: the position we want to clear out
    :return: it will return True if the remove operation was successfully otherwise false
    '''

    if initTimeTable.time_table[position] == course_event:
        # this time_slot will be free again in the time table
        initTimeTable.time_table[position] = None
        initTimeTable.empty_positions.append(position)

        course = processInput.courses_dict[course_event.course_code]
        course.course_hours += 1

        # remove the time_slot from the occupied time_sot list from every curriculum
        for curriculum in course.curricula:
            curriculum.remove_occupied_time_slot(position[1])

        assigned_lecturer = course_event.assigned_lecturer
        assigned_lecturer.remove_occupied_time_slot(position[1])
        course_event.remove_assigned_lecturer()

        return True

    return False
