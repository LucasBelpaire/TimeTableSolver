import neighborhood
import global_variables as gv
import hard_constraints as hc
import data
import time
import random
import copy

best_distance = None
last_distance = None
best_feasible_tt = None


def position_swap(tabu_list):
    # all necessary variables
    global last_distance, best_feasible_tt, best_distance
    position_1, position_2 = neighborhood.get_random_positions()

    # check if the moves are already in the tabu list
    # if not, add them to the list
    if (position_1, position_2) in tabu_list or (position_2, position_1) in tabu_list:
        return False
    tabu_list.append((position_1, position_2))
    tabu_list.append((position_2, position_1))

    # make a back up, so a rollback is possible
    events_back_up = copy.copy(gv.events)
    empty_positions_back_up = copy.copy(gv.empty_positions)
    time_table_back_up = copy.copy(gv.time_table)

    success = neighborhood.swap_positions(position_1, position_2, feasibility=False)

    if not success:
        return False

    # shuffle events, and try to place them in a random order
    random.shuffle(gv.events)
    events_copy = copy.copy(gv.events)
    for event in events_copy:
        for position in gv.empty_positions:
            room_fi_number = position[0]
            time_slot = position[1]
            room = gv.class_rooms_dict[room_fi_number]
            if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                gv.assign_course_to_position(event, position)
                break

    distance = len(gv.events)
    delta_e = distance - last_distance

    if delta_e > 0:
        gv.events = events_back_up
        gv.empty_positions = empty_positions_back_up
        gv.time_table = time_table_back_up
        return False

    # Success!
    last_distance = distance
    if distance < best_distance:
        best_feasible_tt = copy.deepcopy(gv.time_table)
        best_distance = distance
    return True


def split_event(tabu_list):
    # sort events by largest student amount
    gv.events.sort(key=lambda ev: ev.student_amount, reverse=True)
    # get the course with the most amount of students
    event = gv.events.pop(0)
    # check if this event is not in the tabu list
    if event in tabu_list:
        return False
    # split the event
    course_code = event.course_code
    lecturers = event.lecturers
    student_amount_1 = event.student_amount / 2
    student_amount_2 = event.student_amount - student_amount_1
    curricula = event.curricula
    event_number = event.event_number
    course = gv.courses_dict[course_code]
    course.course_hours += 1  # because the event is split into two, an extra course hour should be created
    event_1 = data.CourseEvent(course_code=course_code,
                               lecturers=lecturers,
                               student_amount=student_amount_1,
                               curricula=curricula,
                               event_number=event_number)
    event_2 = data.CourseEvent(course_code=course_code,
                               lecturers=lecturers,
                               student_amount=student_amount_2,
                               curricula=curricula,
                               event_number=event_number)
    # add the new events to the tabu list
    tabu_list.append(event_1)
    tabu_list.append(event_2)
    gv.events.append(event_1)
    gv.events.append(event_2)
    random.shuffle(gv.events)

    # check if it is possible to place extra events
    events_copy = copy.copy(gv.events)
    for event in events_copy:
        for position in gv.empty_positions:
            room_fi_number = position[0]
            time_slot = position[1]
            room = gv.class_rooms_dict[room_fi_number]
            if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                gv.assign_course_to_position(event, position)
                break

    return


def tabu_search():
    global best_distance, last_distance, best_feasible_tt
    starting_time = time.clock()
    max_time = 300
    tabu_length = 1000
    tabu_positions = []
    tabu_split = []

    # Add all unplaced events to events
    gv.events += gv.unplaced_events

    best_distance = len(gv.events)
    print(best_distance)
    last_distance = best_distance
    best_feasible_tt = copy.deepcopy(gv.time_table)

    while len(gv.events) > 0 and time.clock() < starting_time + max_time:
        # if tabu list is full, remove the oldest entry
        if len(tabu_positions) == tabu_length:
            tabu_positions.pop(0)
        if len(tabu_split) == tabu_length:
            tabu_split.pop(0)

        # randomly choose an action
        action = random.randrange(101)
        if action < 100:
            position_swap(tabu_positions)
        if action == 100:
            split_event(tabu_split)
    gv.time_table = best_feasible_tt
    return best_distance, best_feasible_tt
