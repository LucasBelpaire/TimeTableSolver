import processInput
import initTimeTable
import hardConstraints
import constructTimeTable
import random


def get_random_time_slots():
    """
    :return: two different random time slots, integers
    """
    time_slot_1 = random.randrange(processInput.generalInfo.total_course_hours)
    time_slot_2 = random.randrange(processInput.generalInfo.total_course_hours)
    while time_slot_1 == time_slot_2:
        time_slot_2 = random.randrange(processInput.generalInfo.total_course_hours)
    return time_slot_1, time_slot_2


def swap_time_slots(time_slot_1, time_slot_2, feasibility=True):
    """

    :param time_slot_1: integer which indicates the time slot
    :param time_slot_2: integer which indicates the time slot
    :param feasibility: bool, if true feasibility should be preserved, otherwise feasibility is not preserved
    :return: bool, indicates if feasibility is preserved
             back up of events in the first time slot
             back up of events in the second time slot
    """
    room_fi_numbers = processInput.class_rooms_dict.values().fi_number
    events_time_slot_1 = []
    events_time_slot_2 = []
    for fi_number in room_fi_numbers:
        events_time_slot_1.append(initTimeTable.time_table[fi_number, time_slot_1])
        events_time_slot_2.append(initTimeTable.time_table[fi_number, time_slot_2])

    # check if no hard constrain gets violated
    # only the teacher constraint can be a problem
    # if feasibility:
    #    for event in events_time_slot_1:
    #       if event is not None:
    #           if hard


def swap_positions(position_1, position_2, feasibility=True):
    """
    :param position_1: (fi_number, time_slot)
    :param position_2: (fi_number, time_slot)
    :param feasibility: boolean that indicates if feasibility should be preserved
    :return:
    """
    event_1 = initTimeTable.time_table[position_1]
    room_1 = position_1[0]
    time_slot_1 = position_1[1]
    event_2 = initTimeTable.time_table[position_2]
    room_2 = position_2[0]
    time_slot_2 = position_2[1]

    # Check if both events are not None or that they are not equal
    if (event_1 is None and event_2 is None) or event_1 == event_2:
        return False

    # if feasibility should be preserved, the positions only get swapped if the swap is possible for both
    if feasibility:
        # Check if no hard constraints get violated
        if event_1 is not None:
            constructTimeTable.remove_course_from_position(position_2)
            swap_possible = hardConstraints.course_event_fits_in_to_time_slot(event_1, time_slot_2) and hardConstraints.room_capacity_constraint(event_1, room_2)
            initTimeTable.time_table[position_2] = event_2
            if not swap_possible:
                return False

        if event_2 is not None:
            constructTimeTable.remove_course_from_position(position_1)
            swap_possible = hardConstraints.course_event_fits_in_to_time_slot(event_2, time_slot_1) and hardConstraints.room_capacity_constraint(event_2, room_1)
            initTimeTable.time_table[position_1] = event_1
            if not swap_possible:
                return False

        # swapping is possible, so the positions of the two events will get swapped
        constructTimeTable.remove_course_from_position(position_1)
        constructTimeTable.remove_course_from_position(position_2)
        constructTimeTable.assign_course_to_position(event_1, position_2)
        constructTimeTable.assign_course_to_position(event_2, position_1)
        return True

    # if feasibility is false, the swap will occur if no hardconstraints are broken for at least one event
    # the other event will get swapped if possible, or get appended the the unplaced_list if not
    constructTimeTable.remove_course_from_position(position_2)
    constructTimeTable.remove_course_from_position(position_1)
    if event_1 is not None:
        swap_possible = hardConstraints.course_event_fits_in_to_time_slot(event_1, time_slot_2) and hardConstraints.room_capacity_constraint(event_1, room_2)
        if swap_possible:
            constructTimeTable.assign_course_to_position(event_1, position_2)
        else:
            constructTimeTable.unplaced_events.append(event_1)
    if event_2 is not None:
        swap_possible = hardConstraints.course_event_fits_in_to_time_slot(event_2, time_slot_1) and hardConstraints.room_capacity_constraint(event_2, room_1)
        if swap_possible:
            constructTimeTable.assign_course_to_position(event_2, position_1)
        else:
            constructTimeTable.unplaced_events.append(event_2)
    return True
