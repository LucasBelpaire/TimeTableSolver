"""
    This module holds all hard constraints.
"""


def lecturer_is_occupied_in_time_slot(lecturer, time_slot):
    """
    Function checks if the given lecturer is free in the given time slot
    :param lecturer: instance of Lecturer
    :param time_slot: time slot (int)
    :return: True if the lecturer is occupied, False otherwise
    """
    return lecturer.contains_time_slot(time_slot)


def lecturers_are_occupied_in_time_slot(course_event, time_slot):
    """
    This function will check if a lecturer is available for a given time
    :param course_event: instance of CourseEvent, contains the list of lecturers.
    :param time_slot: the specific time_slot that needs to be checked.
    :return: True if no lecturer is available, otherwise False.
    """
    if course_event is None:
        return True

    for lecturer in course_event.lecturers:
        if not lecturer_is_occupied_in_time_slot(lecturer, time_slot):
            return False

    return True


def curriculum_is_occupied_in_time_slot(course_event, time_slot):
    """
    This functions checks if all curricula are available for the given course for a certain time slot.
    :param course_event: instance of CourseEvent
    :param time_slot: the time slot.
    :return: True if not all curricula are available, False otherwise
    """
    if course_event is None:
        return False

    for curriculum in course_event.curricula:
        if not curriculum.contains_time_slot(time_slot):
            return False

    return True


def room_capacity_constraint(course_event, room):
    """
    This function will check if there is enough room for the amount of students that needs to be scheduled.
    :param course_event: instance of CourseEvent
    :param room: instance of ClassRoom
    :return: True if there is enough place for all students, False otherwise
    """
    if course_event is None:
        return False
    if course_event.student_amount <= room.capacity:
        return True
    return False


def course_event_fits_into_time_slot(course_event, time_slot):
    """
    Checks if a course event can be placed into a certain time slot.
    :param course_event: instance of CourseEvent.
    :param time_slot: the time slot that will be checked.
    :return: True if the course can be assigned to a specific time slot, False otherwise.
    """
    return not lecturers_are_occupied_in_time_slot(course_event, time_slot) and not \
        curriculum_is_occupied_in_time_slot(course_event, time_slot)
