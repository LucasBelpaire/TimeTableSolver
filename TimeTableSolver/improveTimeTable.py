import time
import math
import soft_constraints as sc
import neighborhood
import general_info as gi
import hard_constraints as hc


class ImproveTimeTable:

    def __init__(self, timetable):
        """

        The constructor for the third phase: the improvement phase
        here we will try to reduce the total soft constraint penalty

        :param timetable: The feasible timetable that we want to improve
        """
        self.timetable = timetable # this will hold the final time table with the best penalty cost on the end
        #self.best_cost = sc.return_total_penalty_of_timetable(self.timetable)
        #self.last_cost = self.best_cost

    def improve_time_table(self):
        """

        This function will improve the time table to reduce all the penalties from the soft constraints
        :return: we return the total soft constraint penalty
        """
        total_penalty = sc.return_total_penalty_of_timetable(self.timetable)
        print("Score before improvement: " +str(total_penalty))
        # try to improve the timetable
        #self.switch_time_slots_for_late_hour_penalty()
        self.four_or_more_events()
        end_total_penalty = sc.return_total_penalty_of_timetable(self.timetable)
        print("Score after improvement: " +str(end_total_penalty))

        return self.timetable

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
            if place[0] is None:
                print("ts1, place 0 is none")
            if place[1] is None:
                print("ts1, place 1 is None")
            self.timetable.assign_course_to_position(place[1], place[0])

        for place in list_ts_2:
            if place[0] is None:
                print("ts2, place 0 is none")
            if place[1] is None:
                print("ts2, place 1 is None")
            self.timetable.assign_course_to_position(place[1], place[0])

    def switch_time_slots_for_late_hour_penalty(self):
        """

        This function will try to switch as many time slots as possible to reduce the total penalty of late hours
        :return: return true if successful
        """

        # just for testing purposes
        # last_hour_penalty = sc.return_last_two_hour_penalty_all(self.timetable)

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
                #print(count_ts)
                #print(smallest_count_ts_6)
                print("switch timeslots: " + str(6+(day*8)) + ", and " + str(smallest_count_ts_6+(day*8)) + ", with counts of: " + str(count_ts_6) + ", " + str(last_count_6))
                self.switch_events_of_two_time_slots(day, 6+(day*8), smallest_count_ts_6+(day*8))

            #if smallest_count_ts_7 is not None:
                #self.switch_events_of_two_time_slots(day, 7+(day*8), smallest_count_ts_7+(day*8))

        return True

    def four_or_more_events(self):
        """

        This function will try to fix the soft constraint that a curriculum can't have 4 or more lessons after each other
        :return: returns true if succesfull

        """

        successful = True

        for curriculum_id, curriculum in gi.curricula_dict.items():
            events_of_curriculum = list(curriculum.occupied_time_slots)
            # check if there are 4 or more events after each other
            for i in range(len(events_of_curriculum) - 4):

                sub_list_to_check = events_of_curriculum[i,i+4]
                if sorted(sub_list_to_check) == sub_list_to_check:
                    # the list is ascending
                    # Try to replace an event to an other time slot in the time table
                    success = self.try_to_assign_to_new_ts(sub_list_to_check, curriculum_id)
                    if success:
                        continue
                    else:
                        print("Couldn't assign a new pos, so still 4 or more lessons")
                        successful = False

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
            curricula_list = event.curricula
            if pos[1] in list_of_ts and pos[1] not in already_in_list and cur_id in curricula_list:
                already_in_list.append(pos[1])
                removed_event = self.timetable.timetable.remove_course_from_position(pos)
                if not removed_event:
                    print("error bij het removen van een event in try to assign!!!")
                    position_event_list.append((pos, removed_event))
                    position_list.append(pos)

        if len(list_of_ts) != len(position_event_list):
            print('ERROR for try to assign!!!!')
            return



        for position, event in position_event_list:
            for pos in self.timetable.empty_positions:
                room = gi.class_rooms_dict[pos[0]]
                if pos not in position_list and hc.course_event_fits_into_time_slot(event, pos) and hc.room_capacity_constraint(event, room):
                    # course fits in new time_slot
                    print("!!! course fits in to new time slot!")
                    self.timetable.assign_course_to_position(event, pos)
                    continue
            print("course coumdn't be fitted any where else")
            self.timetable.assign_course_to_position(event, position)
