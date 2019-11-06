import time
import data  # TODO: nog veranderen naar de jusite klasse, waar zit de lijst van alle events?
import hardConstraints
import random
import processInput


# This function will constructs a feasible solution or a partially feasible solution
# it will also terminate when no solution is found in a specific time span
def construct_time_table():
    # we hold the starting time while processing a time table
    start_construct = time.clock()

    # TODO: de tijd wordt nu hard gecodeerd, dit moet nog veranderen!!!!
    while (len(processInput.events) > 0 or len(processInput.unplaced_events) > 0) and time.clock()-start_construct < 90:

        # Construct a time table with the remaining events
        events_size = len(processInput.events)
        for index in range(events_size):
            # get an event from the list and look if we can place it on a position
            current_event = processInput.events.pop()
            all_av_positions = order_positions_by_priority(current_event)
            # if this list of positions is empty, than we didn't find a place to put this event
            # so now we change this event from unassigned to unplaced
            if not all_av_positions:
                processInput.unplaced_events.append(current_event)
            else:
                hardConstraints.assign_course_to_position(current_event, all_av_positions[0])

        unplaced_events_size = len(processInput.unplaced_events)

        new_positions = []
        
        # The following lines of code will remove some random events that are already placed in the timetable
        # all the unplaced_events couldn't be assinged to any open position in the timetable
        # so it is necessary to create new open positions by randomly removing events.
        for index in range(unplaced_events_size):
            random_position = random.choice(processInput.forbidden_positions)
            current_random_event = hardConstraints.remove_event_at_position(random_position)
            processInput.forbidden_positions.remove(random_position)
            processInput.events.append(current_random_event)
            new_positions.append(random_position)

        # The next for loop will try to assign some unplaced events in the free timeslot in the timetable
        for index in range(unplaced_events_size):
            current_unplaced_event = processInput.unplaced_events.pop()
            is_assigned = False
            for pos in new_positions:
                if hardConstraints.course_fits_in_to_time_slot(current_unplaced_event, pos[1]):
                    hardConstraints.assign_course_to_position(current_unplaced_event, pos)
                    new_positions.remove(pos)
                    is_assigned = True
                    break
            if not is_assigned:
                processInput.events.append(current_unplaced_event)

    return len(processInput.events)


# This function returns a list of all positions in the timetable that this event can be placed.
def order_positions_by_priority(event):
    # !!!!! pagina 34 voor pseudo code !!!!!

    # Hard_pos is a list that contains positions that don't violate the hard constraints
    hard_pos = []

    # feasible_pos is a list with positions with penalties from the soft constraints
    feasible_pos = []

    # TODO: hoe hervormen we deze functie?

    all_possible_pos = hard_pos + feasible_pos
    return all_possible_pos
