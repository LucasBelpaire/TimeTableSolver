import data

# This function will check if a specific timeslot has a given lecture
# Hard Constraint: Students can only follow one lecture at a time from one curriculum
def timeslot_already_has_this_lecture(event, timeslot):

    if event is None:
        return False

    return False


# This function will return True if the specific timeslot already has this teacher
# otherwise it returns False
# Hard Constraint: a teacher can only give one lesson at a time
def timeslot_already_has_this_teacher(event, timeslot):

    if event is None:
        return False

    return False


# this function will return True if there is already a lecture of the same curriculum at this timeslot
# Hard Constraint: Students can only follow one lecture at a time from one curriculum
def timeslot_already_has_this_curriculum(event, timeslot):

    if event is None:
        return False

    return False


# This functions check if the room has enough space for the total amount of students
# it returns True if there is enough space, otherwise False
# Hard Constraint: we can't exceed the room capacity 
def room_capacity_constraint(course, room):

    return False


# This function will remove an already assinged course to a time slot
# and will add it to the list of unplaced events
# It will return the remove event
def remove_event_at_position(position_of_event):

    rem_event = data.timetable[position_of_event]
    if rem_event is not None:
        data.timetable[position_of_event] = None
        data.emptyPositions.append(position_of_event)

    return rem_event

# This function will assign a course to a position in the timetable
# It won't return any value
def assign_course_to_position(course, position):
    # TODO: Waarom staat de lijn hieronder in commentaar bij de voorbeeld code???
    # if data.timetable[position] is None and courseFitsIntoTimeslot(course, position[1]):
    data.timetable[position] = course
    data.emptyPositions.remove(position)
    data.forbiddenPositions.append(position)


# This is the main function of the hardconstraint class, it will check if the course fits in
# the timeslot without breaking any hard constraints
# this function returns True or False
def course_fits_in_to_time_slot(course, timeslot):
    # TODO: hier moeten we de hard constraint van de roomcapacity nog toevoegen.
    return not timeslot_already_has_this_lecture(course, timeslot) and not timeslot_already_has_this_teacher(course, timeslot) \
           and not timeslot_already_has_this_curriculum(course, timeslot)

