"""
    This module holds all soft constraints.
"""
import general_info as gi
from haversine import haversine
import math


def return_distance_penalty(room, course_event):
    """
    This function will calculate the total distance penalty for a specific course
    :param room: the current room
    :param course_event: the current course
    :return: we return the total penalty
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


def return_not_home_penalty(room, course_event):
    """
    This function calculates the not_home penalty for a given room and course.
    :param room: instance of ClassRoom
    :param course_event: instance of CourseEvent
    :return: The total not_home penalty.
    """
    count_not_home = 0
    curricula_of_courses = course_event.curricula

    for curriculum_code in curricula_of_courses:
        curriculum = gi.curricula_dict[curriculum_code]
        if curriculum.home_site != room.site_id:
            count_not_home += 1

    return count_not_home


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
    # TODO: finish this function
    return None


def return_only_one_hour_penalty(pos, event):
    """
    This function will look if the specific event is the only one on the day from position
    :param pos: This is the specific position
    :param event: the specific event
    :return: return a penalty if it is the only event in a day for that curriculum
    """
    penalty = 0
    curricula = event.curricula
    for curriculum in curricula:
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

    return one_hour_total_penalty

    # alternative solution to compute the one_hour penalty
    # for id, curriculum in gi.curricula_dict.items():
    #     time_slot_list = curriculum.occupied_time_slots
    #     days = [0,0,0,0,0]
    #     for ts in time_slot_list:
    #         day = int(math.floor(ts/8))
    #         days[day] += 1
    #     for i in range(5):
    #         if days[i] == 1:
    #             one_hour_total_penalty += 1


def return_not_home_penalty_all(timetable):
    """
    This function will calculate the total amount of not_home penalties for all scheduled events
    :param timetable: the current timetable
    :return: we return the total penalty
    """
    total_penalty = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            room = gi.class_rooms_dict[pos[0]]
            total_penalty += return_not_home_penalty(room, event)

    return total_penalty


def return_distance_penalty_all(timetable):
    """
    this function will return all the distance penalties of all scheduled events
    :param timetable: the current timetable
    :return: we return the total distance penalty
    """
    total_penalty = 0
    for pos, event in timetable.timetable.items():
        if event is not None:
            room = gi.class_rooms_dict[pos[0]]
            total_penalty += return_distance_penalty(room, event)

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
    room_size = return_room_size_penalty_all(timetable)
    not_home_penalty = return_not_home_penalty_all(timetable)
    distance_penalty = return_not_home_penalty_all(timetable)
    total_penalty = float(late_hour_penalty) + float(one_hour_penalty) + float(room_size) + float(not_home_penalty) + 4*distance_penalty/75
    return total_penalty


