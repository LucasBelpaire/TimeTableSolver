import hard_constraints as hc
import general_info as gi
import random


def get_random_time_slot():
    """
    :return: random time slot
    """
    return random.randrange(gi.total_course_hours)


def get_random_time_slots():
    """
    :return: two different random time slots, integers
    """
    time_slot_1 = random.randrange(gi.total_course_hours)
    time_slot_2 = random.randrange(gi.total_course_hours)
    while time_slot_1 == time_slot_2:
        time_slot_2 = random.randrange(gi.total_course_hours)
    return time_slot_1, time_slot_2


def get_random_positions(timetable):
    """
    :param timetable: instance of Timetable
    :return: two different time table dictionary keys, (fi_number, time_slot)
    """
    if len(timetable.occupied_positions) == 0:
        position_1 = random.choice(list(timetable.timetable))
    else:
        position_1 = random.choice(list(timetable.occupied_positions))  # get an occupied position
    position_2 = random.choice(list(timetable.timetable))
    while position_1 == position_2:
        position_2 = random.choice(list(timetable.timetable))
    return position_1, position_2


def swap_positions(timetable, events, position_1, position_2, feasibility=True):
    """
    :param timetable: instance of Timetable
    :param events: list of courseEvents
    :param position_1: (fi_number, time_slot)
    :param position_2: (fi_number, time_slot)
    :param feasibility: boolean that indicates if feasibility should be preserved
    :return:
    """
    event_1 = timetable.timetable[position_1]
    fi_number_1 = position_1[0]
    room_1 = gi.class_rooms_dict[fi_number_1]
    time_slot_1 = position_1[1]
    event_2 = timetable.timetable[position_2]
    fi_number_2 = position_2[0]
    room_2 = gi.class_rooms_dict[fi_number_2]
    time_slot_2 = position_2[1]
    # Check if both events are not None or that they are not equal
    if (event_1 is None and event_2 is None) or event_1 == event_2:
        return False, timetable, events

    # if feasibility should be preserved, the positions only get swapped if the swap is possible for both
    if feasibility:
        # Check if no hard constraints get violated
        if event_1 is not None:
            timetable.remove_course_from_position(position_2)
            swap_possible = hc.course_event_fits_into_time_slot(event_1, time_slot_2) and hc.room_capacity_constraint(event_1, room_2)
            timetable.assign_course_to_position(event_2, position_2)
            if not swap_possible:
                return False, timetable, events

        if event_2 is not None:
            timetable.remove_course_from_position(position_1)
            swap_possible = hc.course_event_fits_into_time_slot(event_2, time_slot_1) and hc.room_capacity_constraint(event_2, room_1)
            timetable.assign_course_to_position(event_1, position_1)
            if not swap_possible:
                return False, timetable, events

        # swapping is possible, so the positions of the two events will get swapped
        timetable.remove_course_from_position(position_1)
        timetable.remove_course_from_position(position_2)
        timetable.assign_course_to_position(event_1, position_2)
        timetable.assign_course_to_position(event_2, position_1)
        return True, timetable, events

    # if feasibility is false, the swap will occur if no hard constraints are broken for at least one event
    # the other event will get swapped if possible, or get appended the the unplaced_list if not
    timetable.remove_course_from_position(position_2)
    timetable.remove_course_from_position(position_1)
    if event_1 is not None:
        swap_possible = hc.course_event_fits_into_time_slot(event_1, time_slot_2) and hc.room_capacity_constraint(event_1, room_2)
        if swap_possible:
            timetable.assign_course_to_position(event_1, position_2)
        else:
            events.append(event_1)
    if event_2 is not None:
        swap_possible = hc.course_event_fits_into_time_slot(event_2, time_slot_1) and hc.room_capacity_constraint(event_2, room_1)
        if swap_possible:
            timetable.assign_course_to_position(event_2, position_1)
        else:
            events.append(event_2)
    return True, timetable, events


def swap_occupied_for_unplaced_in_time_slot(timetable, events, time_slot):
    """
    This function will look at all occupied places in the timetable for the given time_slot
    and swap an entry with an event in the events list.
    :param timetable: instance of Timetable
    :param events: list of events
    :param time_slot: the time slot that will be checked
    :return: timetable, events
    """

    for occupied_position in timetable.occupied_positions:
        if occupied_position[1] != time_slot:
            continue
        event_back_up = timetable.timetable[occupied_position]
        timetable.remove_course_from_position(occupied_position)
        room = gi.class_rooms_dict[occupied_position[0]]
        time_slot = occupied_position[1]
        found_replacement = False
        for event in events:
            if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                timetable.assign_course_to_position(event, occupied_position)
                found_replacement = True
                break
        if not found_replacement:
            timetable.assign_course_to_position(event_back_up, occupied_position)
            continue
        if found_replacement:
            events.append(event_back_up)
            return True, timetable, events
    return False, timetable, events
