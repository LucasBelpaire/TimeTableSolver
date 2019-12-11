"""
    This module holds all soft constraints.
"""
import general_info as gi
from haversine import haversine
import math


def return_not_home_penalty(room, course_event):
    """
    this function will return the total not home penalty
    :param room: the specific room
    :param course_event: the current course event
    :return: we return 0 if at home, otherwise the total not_home_penalty
    """

    curricula_of_courses = course_event.curricula

    if len(curricula_of_courses) == 0:
        # no curricula, so also no not home_penalty, can be placed anywhere
        return 0

    total_penalty = 0
    for curriculum_code in curricula_of_courses:
        curriculum = gi.curricula_dict[curriculum_code]
        if curriculum.home_site != room.site_id:
            total_penalty += gi.not_home_penalty

    return total_penalty

def return_distance_penalty(room, course_event):
    """
    This function calculates the distance for all students to the specific room
    :param room: instance of ClassRoom
    :param course_event: instance of CourseEvent
    :return: The total not_home penalty.
    """
    class_room_site = gi.sites_dict[room.site_id]

    curricula_of_courses = course_event.curricula

    total_penalty = 0
    for curriculum_code in curricula_of_courses:
        curriculum = gi.curricula_dict[curriculum_code]
        if curriculum.home_site == room.site_id:
            continue

        x_coord_class = float(class_room_site.x_coord)
        y_coord_class = float(class_room_site.y_coord)
        position_class = (x_coord_class, y_coord_class)

        home_of_curriculum = gi.sites_dict[curriculum.home_site]
        x_coord_home_of_curriculum = float(home_of_curriculum.x_coord)
        y_coord_home_of_curriculum = float(home_of_curriculum.y_coord)
        position_home = (x_coord_home_of_curriculum, y_coord_home_of_curriculum)

        distance = haversine(position_class, position_home)

        total_penalty += gi.kilometer_penalty * distance

    return total_penalty

def return_not_home_penalty_all(timetable):
    count = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            curricula_of_courses = event.curricula
            if len(curricula_of_courses) == 0:
                continue
            for curriculum_id in curricula_of_courses:
                curriculum = gi.curricula_dict[curriculum_id]
                class_room = gi.class_rooms_dict[pos[0]]
                if curriculum.home_site != class_room.site_id:
                    count += 1

    return count * gi.not_home_penalty

def return_room_size_penalty_all(timetable):
    """
    This function will compute the penalty for the room size difference for all reservations
    :param timetable: The object that holds the timetable
    :return: we return the mean of all room_size_penalties
    """
    mean_size = 0
    count = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            count += 1
            diff = return_room_size_penalty(pos, event)
            mean_size += diff
    return mean_size / count


def return_room_size_penalty(position, event):
    """
    This function will compute the room_size penalty for one room and event that is scheduled their
    :param position: the position, containing the room and time_slot
    :param event: the event that was scheduled
    :return: we return the penalty
    """
    room_id = position[0]
    room = gi.class_rooms_dict[room_id]
    student_amount = event.student_amount
    room_capacity = room.capacity
    diff = student_amount / room_capacity
    return diff


def return_last_two_hour_penalty(position, event):
    """
    This function will compute a penalty if the event is scheduled at the last two hours of a day
    :param position: the position in the timetable
    :param event: the event scheduled
    :return: we return the penalty
    """
    if event is not None:
        time_slot = position[1]
        # compute the hour of the day
        event_hour = time_slot % 8
        if event_hour == 6 or event_hour == 7:  # last two hours of a day
            return gi.late_hour_penalty
        return 0
    return 0


def return_last_two_hour_penalty_all(timetable):
    """
    This function will compute the penalty for all the events in the last two hours
    :param timetable: the object that holds the timetable
    :return: we return the total penalty
    """
    count_last_two_hours = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            count_last_two_hours += return_last_two_hour_penalty(pos, event)

    return count_last_two_hours


def return_to_many_straight_hours_penalty_all(timetable):
    """
    This function will compute the penalty for all curricula that have 4 or more hours after each other
    :param timetable: the object that holds the time table
    :return: we return the total penalty
    """

    count = 0

    for curriculum_id, curriculum in gi.curricula_dict.items():

        events_of_curriculum = sorted(curriculum.occupied_time_slots)
        #print(len(events_of_curriculum))
        # check if there are 4 or more events after each other
        for i in range(len(events_of_curriculum) - 4):
            #print("test")
            sub_list_to_check = events_of_curriculum[i:(i+4)]
            len(sub_list_to_check)
            if sorted(sub_list_to_check) == sub_list_to_check:
                # 4 events after each other
                count += 1

    #print("aantal 4 of meer:" + str(count))
    return count


def return_only_one_hour_penalty(pos, event):
    """
    This function will look if the specific event is the only one on the day from position
    :param pos: This is the specific position
    :param event: the specific event
    :return: return a penalty if it is the only event in a day for that curriculum
    """
    penalty = 0
    curricula = event.curricula
    for curriculum_id in curricula:
        curriculum = gi.curricula_dict[curriculum_id]
        time_slot_list = curriculum.occupied_time_slots
        current_time_slot = pos[1]
        day = int(math.floor(current_time_slot/8))
        min_two = False
        for ts in time_slot_list:
            ts_day = int(math.floor(ts/8))
            if ts_day == day and ts != current_time_slot:
                # another lesson on the same day
                min_two = True
                break
        if not min_two:
            penalty += 1
    return penalty


def return_only_one_hour_penalty_all(timetable):
    """
    This function will compute the total penalty of all lessons that are scheduled alone on a day
    :param timetable: the object that will hold the timetable
    :return: we return the total penalty
    """

    one_hour_total_penalty = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            one_hour_total_penalty += return_only_one_hour_penalty(pos, event)
    print("One hour penalty: " +str(one_hour_total_penalty))
    return one_hour_total_penalty

    # alternative solution to compute the one_hour penalty
    # total_penalty = 0
    # for id, curriculum in gi.curricula_dict.items():
    #     time_slot_list = sorted(curriculum.occupied_time_slots)
    #     days = [False, False, False, False, False]
    #     only_events_list = []
    #     only_events_and_pos_list = []
    #     for index in range(len(time_slot_list) - 1):
    #         current_ts = time_slot_list[index]
    #         next_ts = time_slot_list[index+1]
    #         current_day = int(math.floor(current_ts/8))
    #         next_day = int(math.floor(next_ts/8))
    #         if current_day != next_day and not days[current_day]:
    #             # new only event on this day
    #             only_events_list.append(current_ts)
    #             # get the pos and event from this one
    #             pos, event = get_pos_and_event_from_ts(timetable, current_ts, id)
    #             only_events_and_pos_list.append((pos, event))
    #         else:
    #             days[current_day] = True
    #     total_penalty += len(only_events_list)
    # return total_penalty

def get_pos_and_event_from_ts(timetable, ts, curriculum_id):
    final = []
    for current_pos, current_event in timetable.timetable.items():
        if current_event is not None and current_pos[1] == ts:
            if curriculum_id in current_event.curricula:
                final.append((current_pos, current_event))
    if len(final) != 1:
        print("length is niet 1, dus meerdere events gevonden op hetzelfde timeslot")
        return False
    return final[0]

def return_distance_penalty(timetable):
    total_penalty = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            room = gi.class_rooms_dict[pos[0]]
            total_penalty += return_not_home_penalty(room, event)

    return total_penalty

def return_total_penalty_of_timetable(timetable):
    """
    This function will compute the total penalty for a specific timetable object
    :param timetable: the object that contains the timetable
    :return:
    """
    # a big value is a bad time_table with a lot of late hours
    late_hour_penalty = return_last_two_hour_penalty_all(timetable)
    one_hour_penalty = return_only_one_hour_penalty_all(timetable)
    #room_size = return_room_size_penalty_all(timetable)
    to_many_straight_hours = return_to_many_straight_hours_penalty_all(timetable)

    # not home penalty
    not_home_penalty = return_not_home_penalty_all(timetable)
    print("Not home penalty: " +str(not_home_penalty))

    # Distance penalty
    #distance_penalty = return_distance_penalty(timetable)

    #final_distance_penalty = 4*distance_penalty/75

    total_penalty = float(late_hour_penalty) + float(one_hour_penalty) + float(to_many_straight_hours) + float(not_home_penalty) #+ float(final_distance_penalty)
    return total_penalty


