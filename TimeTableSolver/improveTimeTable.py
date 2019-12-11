import time
import math
import soft_constraints as sc
import neighborhood
import general_info as gi
import hard_constraints as hc
import copy
import random

class ImproveTimeTable:

    def __init__(self, timetable):
        """

        The constructor for the third phase: the improvement phase
        here we will try to reduce the total soft constraint penalty

        :param timetable: The feasible timetable that we want to improve
        """
        self.timetable = timetable # this will hold the final time table with the best penalty cost on the end
        self.best_cost = sc.return_total_penalty_of_timetable(self.timetable)
        self.last_cost = self.best_cost

    def improve_time_table(self):
        """

        This function will improve the time table to reduce all the penalties from the soft constraints
        :return: we return the total soft constraint penalty
        """
        #total_penalty = sc.return_total_penalty_of_timetable(self.timetable)
        #print("Score before improvement: " +str(total_penalty))

        #self.switch_time_slots_for_late_hour_penalty()


        # ------------------------------------------------
            # Testing

        self.simulated_annealing(15,1.3,5)
        # ------------------------------------------------


        # try to improve the timetable
        #best_total_pen = self.simulated_annealing(5,1.3,5)

        #end_total_penalty = sc.return_total_penalty_of_timetable(self.timetable)
        #print("Score after improvement: " +str(best_total_pen))

        return self.timetable

    def count_events_with_no_curriculum(self):
        count = 0
        for pos, event in self.timetable.timetable.items():
            if event is not None:
                if len(event.curricula) == 0:
                    # an event with no curricula!
                    hour = pos[1] % 8
                    if hour == 6 or hour == 7:
                        # try to move it to an other time_slot
                        count += 1
        print("events with no curriclum on last 2 hours: " + str(count))


    def removing_one_hour_lessons(self):
        for id, curriculum in gi.curricula_dict.items():
            time_slot_list = sorted(curriculum.occupied_time_slots)
            days = [False, False, False, False, False]
            only_events_list = []
            only_events_and_pos_list = []
            for index in range(len(time_slot_list) - 1):
                current_ts = time_slot_list[index]
                next_ts = time_slot_list[index + 1]
                current_day = int(math.floor(current_ts / 8))
                next_day = int(math.floor(next_ts / 8))
                if current_day != next_day and not days[current_day]:
                    # new only event on this day
                    only_events_list.append(current_ts)
                    # get the pos and event from this one
                    pos, event = self.get_pos_and_event_from_ts(self.timetable, current_ts, id)
                    only_events_and_pos_list.append((pos, event))
                else:
                    days[current_day] = True
            self.try_assign_one_hour_events_to_new_pos(only_events_and_pos_list, days)

        return True

    def try_assign_one_hour_events_to_new_pos(self, event_list, days):
        # all events of a curriculum that needs to be moved to an other day, so it doesn't stand alone

        for pos, event in event_list:
            removed_event = self.timetable.remove_course_from_position(pos)
            available_pos = []
            if removed_event == event:
                # try to find a new position on a day that already has a lecture
                for empty_pos in self.timetable.empty_positions:
                    room = gi.class_rooms_dict[empty_pos[0]]
                    day_of_empty_pos = math.floor(empty_pos[1] / 8)
                    if days[day_of_empty_pos] and hc.course_event_fits_into_time_slot(removed_event, empty_pos[1]) \
                            and hc.room_capacity_constraint(removed_event, room) and pos[1] != empty_pos[1]:
                        # there is already an event on this day, so we will improve this soft constraint
                        available_pos.append(empty_pos)
                        #self.timetable.assign_course_to_position(removed_event, empty_pos)
                        continue

                if len(available_pos) == 0:
                    print("NO available pos found, reassign event to old pos")
                    self.timetable.assign_course_to_position(removed_event, pos)
                else:
                    # find the best postion
                    new_pos = available_pos[0]
                    self.timetable.assign_course_to_position(removed_event, new_pos)

            else:
                print("PROBLEEM, removed event is niet hetzelfde als event")
                return False

        return True

    def get_pos_and_event_from_ts(self, timetable, ts, curriculum_id):
        final = []
        for current_pos, current_event in timetable.timetable.items():
            if current_event is not None and current_pos[1] == ts:
                if curriculum_id in current_event.curricula:
                    final.append((current_pos, current_event))
        if len(final) != 1:
            print("length is niet 1, dus meerdere events gevonden op hetzelfde timeslot")
            return False

        return final[0]

    def simulated_annealing(self, t_max, t_min, steps):
        """
        This function will execute simulated annealing on the current time table
        :param t_max: The higest temp
        :param t_min:  The lowest Temp
        :param steps: count of steps
        :return: we return the total cost of the final timetable
        """
        starting_time = time.clock()

        step = 0

        t_factor = -math.log(float(t_max) / t_min)

        no_improvement = 0

        #iterations = 0

        while self.best_cost > 0 and time.clock() - starting_time < 60:
            if no_improvement > 10:
                step = 0

            t_value = t_max * math.exp(t_factor * step / steps)

            if t_value > t_min:
                step += 1

            # select a random neighborhood move
            # x = random.randrange(2)

            change = self.swap_positions_sa(t_value)

            if not change:
                no_improvement += 1
            else:
                no_improvement = 0

            print("total cost of tt: " + str(self.best_cost))

        return True

    def swap_positions_sa(self, t_value):
        """
        This function will swap 2 positions for the simulated annealing process
        :param t_value: The current temp
        :return: we return True if successful else False
        """
        pos1, pos2 = neighborhood.get_random_positions(self.timetable)

        backup_time_table = copy.deepcopy(self.timetable)

        successful, backup1, backup2 = neighborhood.swap_positions(self.timetable, [], pos1, pos2, feasibility=True)

        if not successful:
            print("swap was no success")
            self.timetable = backup_time_table
            return False

        print("swap is SUCCESSFUL")
        total_cost = sc.return_total_penalty_of_timetable(self.timetable)
        delta_e = total_cost - self.last_cost

        if delta_e > 0 and random.random() > math.exp(-delta_e / t_value):
            self.timetable = backup_time_table
            return False

        self.last_cost = total_cost

        if total_cost < self.best_cost:
            self.best_cost = total_cost

        return True

    def get_count_events_on_time_slot(self, time_slot):
        """

        this function will count the amount of events on a given time slot over all rooms
        :param time_slot: the time slot we want to count all events from
        :return: we return the total count off all events on it.
        """
        count = 0

        for pos, event in self.timetable.timetable.items():

            if event is not None and pos[1] == time_slot:
                count += 1

        return count

    def switch_events_of_two_time_slots(self, day, ts_1, ts_2):
        """

        This function will switch two time slots and all events with them, with the purpose to reduce the number of
        lessons given on the last two hours of a day
        :param day: the first parameter is the day where we want to switch time_slots
        :param ts_1: the first time slot
        :param ts_2: the second time slot

        """

        list_ts_1 = []
        list_ts_2 = []

        for oc_pos in self.timetable.occupied_positions:

            if oc_pos[1] == ts_1:
                removed_event = self.timetable.remove_course_from_position(oc_pos)
                if not removed_event:
                    print("verwijderen niet gelukt bij ts1")
                list_ts_1.append(((oc_pos[0], ts_2), removed_event))

            elif oc_pos[1] == ts_2:
                removed_event = self.timetable.remove_course_from_position(oc_pos)
                if removed_event is None:
                    print("verwijderen niet gelukt bij ts2")
                list_ts_2.append(((oc_pos[0], ts_1), removed_event))

        print("length of list 1: " + str(len(list_ts_1)))
        print("length of list 2: " + str(len(list_ts_2)))

        for place in list_ts_1:
            # if place[0] is None:
            #     print("ts1, place 0 is none")
            # if place[1] is None:
            #     print("ts1, place 1 is None")
            self.timetable.assign_course_to_position(place[1], place[0])

        for place in list_ts_2:
            # if place[0] is None:
            #     print("ts2, place 0 is none")
            # if place[1] is None:
            #     print("ts2, place 1 is None")
            self.timetable.assign_course_to_position(place[1], place[0])

    def switch_time_slots_for_late_hour_penalty(self):
        """

        This function will try to switch as many time slots as possible to reduce the total penalty of late hours
        :return: return true if successful
        """

        # just for testing purposes
        last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)

        print("Last hour penalty before: " + str(last_hour_penalty))

        # pick two time_slots in the same day, one must be the 6 or 7 (late hour)
        for day in range(5):
            # pick time_slot 6
            count_ts_6 = self.get_count_events_on_time_slot(6+(day*8))
            smallest_count_ts_6 = None
            last_count_6 = count_ts_6

            count_ts_7 = self.get_count_events_on_time_slot(7 + (day * 8))
            smallest_count_ts_7 = None
            last_count_7 = count_ts_7

            for ts in range(6):
                count_ts = self.get_count_events_on_time_slot(ts+(day*8))
                if count_ts < last_count_6:
                    last_count_6 = count_ts
                    smallest_count_ts_6 = ts

                if count_ts < last_count_7:
                    last_count_7 = count_ts
                    smallest_count_ts_7 = ts

            if smallest_count_ts_6 is not None and last_count_6 < count_ts_6:
                # smallest_count_ts contains a timeslot with fewer events
                # swap this ts with the 6th ts and there will be a smaller penalty
                print("switch timeslots: " + str(6+(day*8)) + ", and " + str(smallest_count_ts_6+(day*8)) + ", with counts of: " + str(count_ts_6) + ", " + str(last_count_6))
                self.switch_events_of_two_time_slots(day, 6+(day*8), smallest_count_ts_6+(day*8))

            if smallest_count_ts_7 is not None and last_count_7 < count_ts_7:
                self.switch_events_of_two_time_slots(day, 7+(day*8), smallest_count_ts_7+(day*8))

        last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)

        print("Last hour penalty after: " + str(last_hour_penalty))

        return True

    def four_or_more_events(self):
        """

        This function will try to fix the soft constraint that a curriculum can't have 4 or more lessons after each other
        :return: returns true if successful

        """

        successful = True
        count = 0
        for curriculum_id, curriculum in gi.curricula_dict.items():
            events_of_curriculum = sorted(curriculum.occupied_time_slots)
            # check if there are 4 or more events after each other
            for i in range(len(events_of_curriculum) - 4):

                sub_list_to_check = events_of_curriculum[i:i+4]
                if sorted(sub_list_to_check) == sub_list_to_check:
                    count += 1
                    # the list is ascending
                    # Try to replace an event to an other time slot in the time table
                    success = self.try_to_assign_to_new_ts(sub_list_to_check, curriculum_id)
                    if success:
                        continue
                    else:
                        print("Couldn't assign a new pos, so still 4 or more lessons")
                        successful = False
        print("total four or more: " + str(count))
        return successful

    def try_to_assign_to_new_ts(self, list_of_ts, cur_id):
        """
        This function will try to assign on of the ascending time slots to an other one, so we don't violate this soft constraint anymore
        :param list_of_ts: the list of ascending time slot of one curriculum
        :return: we return true if successful, else false
        """
        position_event_list = []
        position_list = []
        already_in_list = []
        for pos, event in self.timetable.timetable.items():
            if event is not None:
                curricula_list = event.curricula
                if pos[1] in list_of_ts and pos[1] not in already_in_list and cur_id in curricula_list:
                    print("new spot found")
                    already_in_list.append(pos[1])
                    removed_event = self.timetable.remove_course_from_position(pos)
                    if not removed_event:
                        print("error bij het removen van een event in try to assign!!!")
                    position_event_list.append((pos, removed_event))
                    position_list.append(pos)

        if len(list_of_ts) != len(position_event_list):
            print('ERROR for try to assign!!!!')

            # reassign the old events to the old positions
            for pos, event in position_event_list:
                self.timetable.assign_course_to_position(event, pos)

            return False

        print("length of position_event_list: " + str(len(position_event_list)))

        for position, event in position_event_list:
            print("next pos and event in position_event_list")
            found_empty = False
            for pos in self.timetable.empty_positions:
                room = gi.class_rooms_dict[pos[0]]
                if pos not in position_list and hc.course_event_fits_into_time_slot(event, pos[1] + self.timetable.offset*40) and hc.room_capacity_constraint(event, room) and not found_empty:
                    # course fits in new time_slot
                    print("!!! course fits in to new time slot!")
                    self.timetable.assign_course_to_position(event, pos)
                    found_empty = True

            if not found_empty:
                print("geen plaats gevonden, terug zetten op oude plaats")
                self.timetable.assign_course_to_position(event, position)

        return True