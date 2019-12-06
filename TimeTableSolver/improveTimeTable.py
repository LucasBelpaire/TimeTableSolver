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
        print("switch on day: " +str(day) + ", with time_slots: " + str(ts_1) + ", " + str(ts_2))
        list_ts_1 = []
        list_ts_2 = []

        for oc_pos in self.timetable.occupied_positions:
            room = oc_pos[0]
            oc_pos_day = math.floor(oc_pos[1]/8)
            oc_pos_hour = oc_pos[1] % 8
            if oc_pos_day == day and oc_pos_hour == ts_1 or oc_pos_hour == ts_2:
                    removed_event = self.timetable.remove_course_from_position(oc_pos)
                    if oc_pos_hour == ts_1:
                        list_ts_1.append((removed_event, room))
                    elif oc_pos_hour == ts_2:
                        list_ts_2.append((removed_event, room))

        print("length of list_ev_1: " + str(len(list_ts_1)))
        print("length of list_ev_2: " + str(len(list_ts_2)))

        for ev, room in list_ts_1:
            self.timetable.assign_course_to_position(ev, (room, ts_2))
        for ev, room in list_ts_2:
            self.timetable.assign_course_to_position(ev, (room, ts_1))

    def switch_time_slots_for_late_hour_penalty(self):
        last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)
        print("last hour penalty of timetable: " + str(last_hour_penalty))

        # pick two time_slots in the same day, one must be the 6 or 7 (late hour)
        for day in range(5):
            print("day: " + str(day))
            # pick time_slot 6
            count_ts_6 = self.get_count_events_on_time_slot(6+(day*8))
            print("count pf 6:" + str(count_ts_6))
            smallest_count_ts_6 = None
            last_count_6 = count_ts_6
            for ts in range(6):
                print("for time_slot: " + str(ts))
                count_ts = self.get_count_events_on_time_slot(ts+(day*8))
                print(count_ts)
                if count_ts < last_count_6:
                    last_count_6 = count_ts
                    smallest_count_ts_6 = ts
            print("smallest_count_ts_6: " + str(smallest_count_ts_6))

            if smallest_count_ts_6 is not None:
                print("DO THIS")
                # smallest_count_ts contains a timeslot with fewer events
                # swap this ts with the 6th ts and there will be a smaller penalty
                self.switch_events_of_two_time_slots(day, 6, smallest_count_ts_6)

            #pick time_slot 7
            count_ts_7 = self.get_count_events_on_time_slot(7+(day*8))
            smallest_count_ts_7 = None
            last_count_7 = count_ts_7
            for ts in range(6):
                count_ts = self.get_count_events_on_time_slot(ts+(day*8))
                if count_ts < last_count_7:
                    last_count_7 = count_ts
                    smallest_count_ts_7 = ts

            if smallest_count_ts_7 is not None:
                # smallest_count_ts contains a time_slot with fewer events
                # swap this ts with the 7th ts and there will be a smaller penalty
                self.switch_events_of_two_time_slots(day, 7, smallest_count_ts_7)

        last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)
        print("last hour penalty of timetable: " + str(last_hour_penalty))