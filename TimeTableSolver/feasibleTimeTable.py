import neighborhood
import initTimeTable
import hardConstraints
import constructTimeTable
import time
import random
import copy

best_distance = len(initTimeTable.events_type_1)
last_distance = best_distance
best_feasible_tt = copy.deepcopy(initTimeTable.time_table)


def position_swap(tabu_list):
    # all necessary variables
    global last_distance, best_feasible_tt, best_distance
    position_1, position_2 = neighborhood.get_random_positions()
    events = initTimeTable.events_type_1
    empty_positions = initTimeTable.empty_positions
    time_table = initTimeTable.time_table

    # check if the moves are already in the tabu list
    # if not, add them to the list
    if (position_1, position_2) in tabu_list or (position_2, position_1) in tabu_list:
        return False
    tabu_list.append((position_1, position_2))
    tabu_list.append((position_2, position_1))

    # make a back up, so a rollback is possible
    events_back_up = copy.copy(events)
    empty_positions_back_up = copy.copy(empty_positions)
    time_table_back_up = copy.copy(time_table)

    success = neighborhood.swap_positions(position_1, position_2, feasibility=False)

    if not success:
        return False

    # shuffle events, and try to place them in a random order
    random.shuffle(events)
    events_temp_back_up = copy.copy(events)

    for event in events:
        for position in empty_positions:
            room = position[0]
            time_slot = position[1]
            if hardConstraints.course_event_fits_in_to_time_slot(event, time_slot) and hardConstraints.room_capacity_constraint(event, room):
                constructTimeTable.assign_course_to_position(event, position)
                events_temp_back_up.remove(event)
                break

    events = events_temp_back_up
    distance = len(events)
    delta_e = distance - last_distance

    if delta_e > 0:
        initTimeTable.events_type_1 = events_back_up
        initTimeTable.empty_positions = empty_positions_back_up
        initTimeTable.time_table = time_table_back_up
        return False

    # Success!
    last_distance = distance
    if distance < best_distance:
        best_feasible_tt = copy.deepcopy(initTimeTable.time_table)
        best_distance = distance
    return True


def split_event(tabu_list):
    return


def tabu_search():
    starting_time = time.clock()
    max_time = 90
    tabu_length = 500
    tabu_positions = []
    tabu_split = []

    best_result = len(initTimeTable.courses_type_1)

    while best_result > 0 and time.clock() > starting_time + max_time:
        # if tabu list is full, remove the oldest entry
        if len(tabu_positions) == tabu_length:
            tabu_positions.pop(0)
        if len(tabu_split) == tabu_length:
            tabu_split.pop(0)

        # randomly choose an action
        action = random.randrange(2)
        if action == 0:
            position_swap(tabu_positions)
        if action == 1:
            split_event(tabu_split)

    return best_distance, best_feasible_tt
