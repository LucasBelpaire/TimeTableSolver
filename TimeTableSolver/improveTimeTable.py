import time
import math
import soft_constraints as sc
import neighborhood
import general_info as gi
import hard_constraints as hc

class ImproveTimeTable:

    def __init__(self, timetable):
        """
        The constructor for the third phase the improvement phase
        :param timetable: The feasible timetable that we want to improve
        """
        self.timetable = timetable # this will hold the final time table with the best penalty cost on the end
        self.best_cost = sc.return_total_penalty_of_timetable(self.timetable)
        self.last_cost = self.best_cost

    def get_count_events_on_time_slot(self, time_slot):
        count = 0
        for pos, event in self.timetable.timetable.items():
            if event is not None and pos[1] == time_slot:
                count += 1
        return count

    def switch_events_of_two_time_slots(self, day, ts_1, ts_2):
        list_ts_1 = []
        list_ts_2 = []

        for oc_pos in self.timetable.occupied_positions:
            removed_event = False
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
        """

        :return:
        """
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

    def remove_one_hour_lessons(self):
       return None