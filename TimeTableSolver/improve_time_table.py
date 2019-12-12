import time
import math
import soft_constraints as sc
import neighborhood
import random
import copy


class ImproveTimeTable:

    def __init__(self, timetable):
        """
        The constructor for the third phase the improvement phase
        :param timetable: The feasible timetable that we want to improve
        """
        self.timetable = timetable # this will hold the final time table with the best penalty cost on the end
        self.best_cost = sc.return_total_penalty_of_timetable(self.timetable)
        self.last_cost = self.best_cost

    def improve(self):
        """
        This function will try to improve the timetable and it soft constraints
        :return: we return the total penalty and the timetable

        """
        total_cost = sc.return_total_penalty_of_timetable(self.timetable)
        print("Cost of tt before improve: " + str(total_cost))

        self.simulated_annealing(10, 1.3, 5)

        print("Cost after improve phase: " + str(self.best_cost))

        return self.best_cost, self.timetable

    def get_count_events_on_time_slot(self, time_slot):
        """
        This function will count the total amount of events on this time slot
        :param time_slot: the current time slot
        :return: we return the total amount
        """
        count = 0
        for pos, event in self.timetable.timetable.items():
            if event is not None and pos[1] == time_slot:
                count += 1
        return count

    def switch_events_of_two_time_slots(self, day, ts_1, ts_2):
        list_ts_1 = []
        list_ts_2 = []

        for oc_pos in self.timetable.occupied_positions:
            if oc_pos[1] == ts_1:
                removed_event = self.timetable.remove_course_from_position(oc_pos)
                list_ts_1.append(((oc_pos[0], ts_2), removed_event))
            elif oc_pos[1] == ts_2:
                removed_event = self.timetable.remove_course_from_position(oc_pos)
                list_ts_2.append(((oc_pos[0], ts_1), removed_event))

        for place in list_ts_1:
            self.timetable.assign_course_to_position(place[1], place[0])
        for place in list_ts_2:
            self.timetable.assign_course_to_position(place[1], place[0])

    def switch_time_slots_for_late_hour_penalty(self):
        last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)

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

            if smallest_count_ts_6 is not None:
                # smallest_count_ts contains a timeslot with fewer events
                # swap this ts with the 6th ts and there will be a smaller penalty
                self.switch_events_of_two_time_slots(day, 6+(day*8), smallest_count_ts_6+(day*8))

            if smallest_count_ts_7 is not None:
                self.switch_events_of_two_time_slots(day, 7+(day*8), smallest_count_ts_7+(day*8))

        return True

    def simulated_annealing(self, t_max, t_min, steps):
        """
        This function will execute simulated annealing on the current time table
        :param t_max: The highest temp
        :param t_min:  The lowest Temp
        :param steps: count of steps
        :return: we return the total cost of the final timetable
        """
        starting_time = time.clock()

        step = 0

        t_factor = -math.log(float(t_max) / t_min)

        no_improvement = 0

        # iterations = 0

        while self.best_cost > 0 and time.clock() - starting_time < 180:
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
