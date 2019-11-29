import data
import processInput


def time_slot_already_has_this_teacher(course_event, time_slot):
    '''
    This function will check if the teacher is available on that specific time_slot
    This function is needed to accomplish the hard constraint: a teacher can only teach one course at a time
    :param course_event: this is the course that the teacher need to give
    :param time_slot: the specific time_slot that we want to assign this course to
    :return: we return True if the teacher isn't available, otherwise we return False, and than the
        course_event can be scheduled at this specific time_slot
    '''

    #TODO: in het verslag schrijven: eerst gingen we alle rooms en time_slots overlopen, maar dit hebben we veranderd
    #TODO: naar het bijhouden van een veld in het object lecturer die de tijden bijhudt waar deze lesgever al les geeft.

    # if None was passed then we return False, because there was no teacher
    if course_event is None:
        return True

    for lecturer in course_event.lecturers:
        if not lecturer.contains_time_slot(time_slot):
            return False

    #print("HARD CONSTRAINT violation: there are no teachers available at this time")
    return True


# def is_class_room_free(room, time_slot):
#     '''
#     This is a small function that will check if a room is already used or not in the time table
#     :param room: the first parameter is the room object
#     :param time_slot: the second parameter is the time_slot object
#     :return: we return true if the room is free at that specific time_slot else false
#     '''
#     return processInput.time_table[(room.fi_number, time_slot)] is None


def time_slot_already_has_this_curriculum(course_event, time_slot):
    '''
    This function will check if any room already has a course were the students needs to be
    this will handle the hard constraint: a student can only attend one course at a time from one curriculum
    :param course_event: first parameter is the course_event, we use the curriculum of this course_event
    :param time_slot: the time_slot to be used in the time table
    :return: we return true if there is already a course form the same curriculum.
    '''

    #TODO: in het verslag schrijven: eerst gingen we alle rooms en time_slots overlopen, maar dit hebben we veranderd
    #TODO: naar het bijhouden van een veld in het object curriculum die de tijden bijhoudt waar dit curriculum al gegeven wordt.
    
    if course_event is None:
        return False

    for curriculum in course_event.curricula:
        if not curriculum.contains_time_slot(time_slot):
            return False

    #print("HARD CONSTRAINT violation: this curriculum is already in progress at this time")
    return True


def room_capacity_constraint(course_event, room):
    '''
    This function will check if there is enough room for the amount of students that needs to be scheduled
    :param course_event: this is the current course that needs to be scheduled
    :param room: the room we want to check
    :return: we return True if there are enough seats for the students
    '''
    if course_event.student_amount <= room.capacity:
        return True

    return False


# This is the main function of the hardconstraint class, it will check if the course fits in
# the time_slot without breaking any hard constraints
# this function returns True or False
def course_event_fits_in_to_time_slot(course_event, time_slot):
    """

    :param course: The course we want to assign
    :param time_slot: the specific time we want to use
    :param room: the specific room we want to use
    :return: This returns true if the course can be assigned to a specific time_slot and room
    """
    return not time_slot_already_has_this_teacher(course_event, time_slot) \
           and not time_slot_already_has_this_curriculum(course_event, time_slot)
