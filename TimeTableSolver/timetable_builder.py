import construct_timetable as ct
import feasible_timetable as ft
import copy
import time
import random
import improveTimeTable as it

class TimeTableBuilder:
    def __init__(self, timetable, events_1, events_2, events_3, events_4, courses_set, start_time):
        self.timetable = timetable
        self.events_1 = events_1
        self.events_2 = events_2
        random.shuffle(self.events_2)
        self.events_3 = events_3
        random.shuffle(self.events_3)
        self.events_4 = events_4
        random.shuffle(events_4)
        self.courses_set = courses_set
        self.start_time = start_time

    def build_timetable(self):
        timetable_13 = copy.deepcopy(self.timetable)  # empty timetable which will be used to represent the last week
        # events type 1
        print("Starting initial construction of timetable type 1.  " + str(time.perf_counter() - self.start_time))
        construct_timetable = ct.ConstructTimeTable(events_list=self.events_1,
                                                    courses_set=self.courses_set,
                                                    timetable=self.timetable,
                                                    week_13=False)
        events_1, timetable = construct_timetable.construct()
        print("Initial construction of timetable type 1 is finished.  " + str(time.perf_counter() - self.start_time))
        print("Starting tabu search on timetable type 1.  " + str(time.perf_counter() - self.start_time))
        feasible_timetable = ft.FeasibleTimetable(events=events_1,
                                                  timetable=timetable)
        events_1, timetable = feasible_timetable.tabu_search()
        print("Tabu search on timetable type 1 is finished.  " + str(time.perf_counter() - self.start_time))

        # improve_tt_1 = it.ImproveTimeTable(timetable)
        # timetable = improve_tt_1.improve_time_table()

        return [(timetable, [1,2,3,4,5,6,7,8,9,10,11,12])]

    @staticmethod
    def split(a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
