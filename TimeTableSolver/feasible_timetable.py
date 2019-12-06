import neighborhood
import hard_constraints as hc
import general_info as gi
import data
import time
import random
import copy


class FeasibleTimetable:

    def __init__(self, events, timetable):
        self.events = events
        self.timetable = timetable
        self.best_distance = len(self.events)
        self.last_distance = len(self.events)
        self.best_feasible_tt = copy.deepcopy(timetable)

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
        if event in tabu_list:
            self.events.append(event)
            return False

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
            # if tabu list is full, remove the oldest entry
            if len(tabu_positions) == tabu_length:
                tabu_positions.pop(0)
            if len(tabu_split) == tabu_length:
                tabu_split.pop(0)
            if len(tabu_unplaced_swap) == tabu_length_unplaced_swap:
                tabu_unplaced_swap.pop(0)

            # randomly choose an action
            action = random.randrange(100)
            if action < 45:
                print("swap")
                self.position_swap(tabu_positions)
            if action < 90:
                print("occupied_swap")
                self.occupied_unplaced_time_slot_swap(tabu_unplaced_swap)
            if action >= 90:
                print("split")
                self.split_event(tabu_split)
            print(len(self.events))
        print(len(self.events))
        return self.best_distance, self.best_feasible_tt
