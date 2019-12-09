import neighborhood
import hard_constraints as hc
import general_info as gi
import data
import time
import random
import copy
import math

class FeasibleTimetable:

    def __init__(self, events, timetable):
        self.events = events
        self.timetable = timetable
        self.best_distance = len(self.events)
        self.last_distance = len(self.events)
        self.best_feasible_tt = copy.deepcopy(timetable)


    def try_unplaced_evnts(self):
        count_unplaced_events = 0
        for current_unplaced_event in self.events:
            # we can't place this event no where in the table
            count_unplaced_events += 1
            print("count: " + str(count_unplaced_events))
            print("course: " +str(current_unplaced_event.course_code))
            # iterate over all positions in the time_table
            fit_found = False
            for pos in self.timetable.occupied_positions:
                room = gi.class_rooms_dict[pos[0]]
                placed_event = self.timetable.remove_course_from_position(pos)

                if placed_event is False:
                    # something went wrong with the remove
                    print("something went wrong with the remove")
                    continue

                if hc.course_event_fits_into_time_slot(current_unplaced_event, pos[1]) and hc.room_capacity_constraint(current_unplaced_event, room):
                    print("fits")
                    available_pos = self.compute_available_positions_for_event(placed_event, pos)
                    print(len(available_pos))
                else:
                    #print("geen fit")
                    # current unplaced event doesn't fit in that post, place the removed event back in it
                    self.timetable.assign_course_to_position(placed_event, pos)

            print("end, no place")

    def compute_available_positions_for_event(self, event, old_pos):
        available_pos = []
        for pos in self.timetable.empty_positions:
            room = gi.class_rooms_dict[pos[0]]
            if hc.course_event_fits_into_time_slot(event, pos[1]) and hc.room_capacity_constraint(event, room):
                if pos != old_pos:
                    available_pos.append(pos)
        if len(available_pos) == 0:
            print("NO POS")
        return available_pos

    def position_swap(self, tabu_list):
        position_1, position_2 = neighborhood.get_random_positions(self.timetable)

        # check if the moves are already in the tabu list
        # if not, add them to the list
        if (position_1, position_2) in tabu_list or (position_2, position_1) in tabu_list:
            return False
        tabu_list.append((position_1, position_2))
        tabu_list.append((position_2, position_1))

        # make a back up, so a rollback is possible
        timetable_back_up = copy.deepcopy(self.timetable)
        events_back_up = copy.deepcopy(self.events)
        success, self.timetable, self.events = neighborhood.swap_positions(self.timetable,
                                                                           self.events,
                                                                           position_1,
                                                                           position_2,
                                                                           feasibility=False
                                                                           )

        if not success:
            self.timetable = timetable_back_up
            self.events = events_back_up
            return False
        # shuffle events, and try to place them in a random order
        random.shuffle(self.events)
        events_to_remove = []
        for event in self.events:
            for position in self.timetable.empty_positions:
                room_fi_number = position[0]
                time_slot = position[1]
                room = gi.class_rooms_dict[room_fi_number]
                if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                    self.timetable.assign_course_to_position(event, position)
                    events_to_remove.append(event)
                    break

        # removed assigned events
        for event in events_to_remove:
            self.events.remove(event)

        distance = len(self.events)
        delta_e = distance - self.last_distance

        if delta_e > 0:
            self.timetable = timetable_back_up
            self.events = events_back_up
            return False
        # Success!
        self.last_distance = distance
        if self.last_distance <= self.best_distance:
            self.best_feasible_tt = copy.deepcopy(self.timetable)
            self.best_distance = distance
        return True

    def split_event(self, tabu_list):
        # sort events by largest student amount
        self.events.sort(key=lambda ev: ev.student_amount, reverse=True)
        # get the course with the most amount of students
        event = self.events.pop(0)
        # check if this event is not in the tabu list
        while event in tabu_list:
            self.events.append(event)
            event = self.events.pop(0)

        # get all available positions, not taking in account the room capacity
        biggest_capacity = 0
        for empty_position in self.timetable.empty_positions:
            fi_number = empty_position[0]
            time_slot = empty_position[1]
            if hc.course_event_fits_into_time_slot(event, time_slot):
                size = gi.class_rooms_dict[fi_number].capacity
                if size > biggest_capacity:
                    biggest_capacity = size

        if biggest_capacity == 0:
            tabu_list.append(event)
            self.events.append(event)
            return
        # split the event
        course_code = event.course_code
        lecturers = event.lecturers
        student_amount_1 = biggest_capacity
        student_amount_2 = event.student_amount - student_amount_1
        curricula = event.curricula
        event_number = event.event_number
        course = gi.courses_dict[course_code]
        course.course_hours += 1  # because the event is split into two, an extra course hour should be created
        event_1 = data.CourseEvent(course_code=course_code,
                                   lecturers=lecturers,
                                   student_amount=student_amount_1,
                                   curricula=curricula,
                                   event_number=event_number)
        event_2 = data.CourseEvent(course_code=course_code,
                                   lecturers=lecturers,
                                   student_amount=student_amount_2,
                                   curricula=curricula,
                                   event_number=event_number)
        # add the new events to the tabu list
        tabu_list.append(event_1)
        tabu_list.append(event_2)
        self.events.insert(0, event_1)
        self.events.insert(1, event_2)

        # check if it is possible to place extra events
        events_to_remove = []
        for event in self.events:
            for position in self.timetable.empty_positions:
                room_fi_number = position[0]
                time_slot = position[1]
                room = gi.class_rooms_dict[room_fi_number]
                if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                    self.timetable.assign_course_to_position(event, position)
                    events_to_remove.append(event)
                    break
        # remove the events that got assigned
        for event in events_to_remove:
            self.events.remove(event)

        distance = len(self.events)
        self.last_distance = distance
        if self.last_distance <= self.best_distance:
            self.best_feasible_tt = copy.deepcopy(self.timetable)
            self.best_distance = distance
        return

    def occupied_unplaced_time_slot_swap(self, tabu_list):
        time_slot = neighborhood.get_random_time_slot()
        if time_slot in tabu_list:
            return False
        tabu_list.append(time_slot)

        timetable_back_up = copy.deepcopy(self.timetable)
        events_back_up = copy.deepcopy(self.events)

        success, self.timetable, self.events = neighborhood.swap_occupied_for_unplaced_in_time_slot(self.timetable,
                                                                                                    self.events,
                                                                                                    time_slot
                                                                                                    )

        if not success:
            self.timetable = timetable_back_up
            self.events = events_back_up
            return False

        # shuffle events, and try to place them in a random order
        random.shuffle(self.events)
        events_to_remove = []
        for event in self.events:
            for position in self.timetable.empty_positions:
                room_fi_number = position[0]
                time_slot = position[1]
                room = gi.class_rooms_dict[room_fi_number]
                if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                    self.timetable.assign_course_to_position(event, position)
                    events_to_remove.append(event)
                    break

        # removed assigned events
        for event in events_to_remove:
            self.events.remove(event)

        distance = len(self.events)
        delta_e = distance - self.last_distance

        if delta_e > 0:
            self.timetable = timetable_back_up
            self.events = events_back_up
            return False
        # Success!
        self.last_distance = distance
        if self.last_distance <= self.best_distance:
            self.best_feasible_tt = copy.deepcopy(self.timetable)
            self.best_distance = distance
        return True

    def tabu_search(self):
        starting_time = time.clock()
        max_time = 300
        tabu_length = 300
        tabu_length_unplaced_swap = 10
        tabu_positions = []
        tabu_split = []
        tabu_unplaced_swap = []
        print(len(self.events))
        while len(self.events) > 0 and time.clock() < starting_time + max_time:
            print(len(self.events))
            # if tabu list is full, remove the oldest entry
            if len(tabu_positions) == 300:
                tabu_positions.pop(0)
            if len(tabu_split) == 20:
                tabu_split.pop(0)
            if len(tabu_unplaced_swap) == 20:
                tabu_unplaced_swap.pop(0)

            # randomly choose an action
            action = random.randrange(100)
            if action < 33:
                print("swap")
                self.position_swap(tabu_positions)
                continue
            if action < 66:
                print("occupied_swap")
                self.occupied_unplaced_time_slot_swap(tabu_unplaced_swap)
                continue
            if action >= 66:
                print("split")
                self.split_event(tabu_split)
        print(len(self.events))
        return self.best_distance, self.best_feasible_tt

    def simulated_annealing(self, t_max, t_min, steps):
        starting_time = time.clock()

        step = 0

        t_factor = -math.log(float(t_max) / t_min)

        no_improvement = 0

        iterations = 0

        while self.best_distance > 0 and time.clock() - starting_time < 300:
            if no_improvement > 10:
                step = 0

            t_value = t_max * math.exp(t_factor * step / steps)

            if t_value > t_min:
                step += 1

            #x = random.randrange(2)

            change = self.swap_positions_sa(t_value)

            if not change:
                no_improvement += 1
            else:
                no_improvement = 0

            print("length of unplaced: " + str(len(self.events)))

        return self.best_distance, self.best_feasible_tt

    def swap_positions_sa(self, t_value):
        pos1, pos2 = neighborhood.get_random_positions(self.timetable)

        backupEvents = copy.deepcopy(self.events)
        backupTimeTable = copy.deepcopy(self.timetable)

        succesful, backup1, backup2 = neighborhood.swap_positions(self.timetable,
                                                                  self.events,
                                                                  pos1,
                                                                  pos2,
                                                                  feasibility=False
                                                                  )
        if not succesful:
            self.timetable = backupTimeTable
            self.events = backupEvents
            return False

        print("Swap successful")

        # try to assigning the unplaced events to empty positions
        events_to_remove = []
        for event in self.events:
            count_curr = 0
            count_lect = 0
            for position in self.timetable.empty_positions:
                room_fi_number = position[0]
                time_slot = position[1]
                room = gi.class_rooms_dict[room_fi_number]
                if hc.curriculum_is_occupied_in_time_slot(event, time_slot):
                    count_curr += 1

                if hc.lecturers_are_occupied_in_time_slot(event, time_slot):
                    count_lect += 1

                # if hc.course_event_fits_into_time_slot(event, time_slot) and hc.room_capacity_constraint(event, room):
                #     self.timetable.assign_course_to_position(event, position)
                #     events_to_remove.append(event)
                #     break
            print("count curriculum occupied: " + str(count_curr))
            
        if len(events_to_remove) == 0:
            print("no events to remove")

        # removed assigned events
        for event in events_to_remove:
            self.events.remove(event)

        distance = len(self.events)
        delta_e = distance - self.last_distance

        if delta_e > 0 and random.random() > math.exp(-delta_e / t_value):
            self.timetable = backupTimeTable
            self.events = backupEvents
            return False

        print("Success !!!!!!!")
        self.last_distance = distance
        if self.last_distance <= self.best_distance:
            self.best_feasible_tt = copy.deepcopy(self.timetable)
            self.best_distance = distance
        return True