import hard_constraints as hc
import global_variables as gv
import random


def get_random_time_slots():
    """
    :return: two different random time slots, integers
    """
    time_slot_1 = random.randrange(gv.generalInfo.total_course_hours)
    time_slot_2 = random.randrange(gv.generalInfo.total_course_hours)
    while time_slot_1 == time_slot_2:
        time_slot_2 = random.randrange(gv.generalInfo.total_course_hours)
    return time_slot_1, time_slot_2


def get_random_positions():
    """
    :return: two different time table dictionary keys, (fi_number, time_slot)
    """
    position_1 = random.choice(list(gv.time_table))
    position_2 = random.choice(list(gv.time_table))
    while position_1 == position_2:
        position_2 = random.choice(list(gv.time_table))
    return position_1, position_2


def swap_positions(position_1, position_2, feasibility=True):
    """
    :param position_1: (fi_number, time_slot)
    :param position_2: (fi_number, time_slot)
    :param feasibility: boolean that indicates if feasibility should be preserved
    :return:
    """
    event_1 = gv.time_table[position_1]
    room_1 = position_1[0]
    time_slot_1 = position_1[1]
    event_2 = gv.time_table[position_2]
    room_2 = position_2[0]
    time_slot_2 = position_2[1]

    # Check if both events are not None or that they are not equal
    if (event_1 is None and event_2 is None) or event_1 == event_2:
        return False

    # if feasibility should be preserved, the positions only get swapped if the swap is possible for both
    if feasibility:
        # Check if no hard constraints get violated
        if event_1 is not None:
            gv.remove_course_from_position(position_2)
            swap_possible = hc.course_event_fits_into_time_slot(event_1, time_slot_2) and hc.room_capacity_constraint(event_1, room_2)
            gv.assign_course_to_position(event_2, position_2)
            if not swap_possible:
                return False

        if event_2 is not None:
            gv.remove_course_from_position(position_1)
            swap_possible = hc.course_event_fits_into_time_slot(event_2, time_slot_1) and hc.room_capacity_constraint(event_2, room_1)
            gv.assign_course_to_position(event_1, position_1)
            if not swap_possible:
                return False

        # swapping is possible, so the positions of the two events will get swapped
        gv.remove_course_from_position(position_1)
        gv.remove_course_from_position(position_2)
        gv.assign_course_to_position(event_1, position_2)
        gv.assign_course_to_position(event_2, position_1)
        return True

    # if feasibility is false, the swap will occur if no hard constraints are broken for at least one event
    # the other event will get swapped if possible, or get appended the the unplaced_list if not
    gv.remove_course_from_position(position_2)
    gv.remove_course_from_position(position_1)
    if event_1 is not None:
        swap_possible = hc.course_event_fits_into_time_slot(event_1, time_slot_2) and hc.room_capacity_constraint(event_1, room_2)
        if swap_possible:
            gv.assign_course_to_position(event_1, position_2)
        else:
            gv.unplaced_events.append(event_1)
    if event_2 is not None:
        swap_possible = hc.course_event_fits_into_time_slot(event_2, time_slot_1) and hc.room_capacity_constraint(event_2, room_1)
        if swap_possible:
            gv.assign_course_to_position(event_2, position_1)
        else:
            gv.unplaced_events.append(event_2)
    return True
