import data
import processInput


# This function will return True if there is no teacher available to give this eventCourse
# otherwise it returns False
# Hard Constraint: a teacher can only give one lesson at a time
def time_slot_already_has_this_teacher(course, timeslot):
    if course is None:
        return False

    occupied_lecturers = []
    for room in processInput.class_rooms_dict.values():
        room_fi_number = room.fi_number
        if processInput.time_table[(room_fi_number, timeslot)] is not None:
            existing_event = processInput.time_table[(room_fi_number, timeslot)]
            course_lecturers = course.lecturers
            event_lecturers = existing_event.lecturers
            for lecturer in course_lecturers:
                if lecturer in event_lecturers and lecturer not in occupied_lecturers:
                    occupied_lecturers.append(lecturer)
            if len(event_lecturers) == len(occupied_lecturers): #if the two array's are equal in length then there is no teacher available at this moment
                return True

    return False


def is_class_room_free(room, time_slot):
    return processInput.time_table[(room.fi_number, time_slot)] is None

# this function will return True if there is already a lecture of the same curriculum at this timeslot
# Hard Constraint: Students can only follow one lecture at a time from one curriculum
def timeslot_already_has_this_curriculum(course, timeslot):

    if course is None:
        return False

    current_event_curricula = processInput.courses_dict[course.code]
    for room in processInput.class_rooms_dict.values():
        room_fi_number = room.fi_number
        if processInput.time_table[(room_fi_number, timeslot)] is not None:
            existing_event = processInput.time_table[(room_fi_number, timeslot)]

            for curricula in current_event_curricula:
                # TODO: nog afwerken!!!

                return False

    return False


# This functions check if the room has enough space for the total amount of students
# it returns True if there is enough space, otherwise False
# Hard Constraint: we can't exceed the room capacity 
def room_capacity_constraint(course, room):
    if course.student_amount <= room.capacity:
        return True
    return False


# This function will remove an already assigned course to a time slot
# and will add it to the list of unplaced events
# It will return the remove event
def remove_event_at_position(position_of_event):

    rem_event = processInput.time_table[position_of_event]
    if rem_event is not None:
        processInput.time_table[position_of_event] = None
        processInput.empty_positions.append(position_of_event)

    return rem_event

# This function will assign a course to a position in the timetable
# It won't return any value
def assign_course_to_position(course, position):

    processInput.time_table[position] = course
    course.course_hours -= 1
    processInput.empty_positions.remove(position)
    processInput.forbidden_positions.append(position)


# This is the main function of the hardconstraint class, it will check if the course fits in
# the timeslot without breaking any hard constraints
# this function returns True or False
def course_fits_in_to_time_slot(course, time_slot):
    """

    :param course: The course we want to assign
    :param time_slot: the specific time we want to use
    :param room: the specific room we want to use
    :return: This returns true if the course can be assigned to a specific time_slot and room
    """
    return not time_slot_already_has_this_teacher(course, time_slot) \
           and not timeslot_already_has_this_curriculum(course, time_slot)
