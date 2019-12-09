import construct_timetable as ct
import feasible_timetable as ft
import process_input as pi
import copy
import random
import pickle


class TimeTableBuilder:
    def __init__(self, timetable, events_1, events_2, events_3, events_4, courses_set):
        self.timetable = timetable
        self.events_1 = events_1
        self.events_2 = events_2
        random.shuffle(self.events_2)
        self.events_3 = events_3
        random.shuffle(self.events_3)
        self.events_4 = events_4
        random.shuffle(events_4)
        self.courses_set = courses_set

    def build_timetable(self):
        # events type 1
        print("Type 1")
        construct_timetable = ct.ConstructTimeTable(events_list=self.events_1,
                                                    courses_set=self.courses_set,
                                                    timetable=self.timetable)
        events_1, timetable = construct_timetable.construct()

        with open('events.pckl', 'wb') as f:
            pickle.dump(events_1, f)
        with open('timetable.pckl', 'wb') as f:
            pickle.dump(timetable, f)

        # f1 = open('timetable.pckl', 'rb')
        # timetable = pickle.load(f1)
        # f1.close()
        # f2 = open('events.pckl', 'rb')
        # events_1 = pickle.load(f2)
        # f2.close()

        feasible_timetable = ft.FeasibleTimetable(events=events_1,
                                                  timetable=timetable)
        events_1, timetable = feasible_timetable.tabu_search()

        # events type 2, split original timetable into two
        print("Type 2")
        events_2a = self.events_2[len(self.events_2):]
        events_2b = self.events_2[:len(self.events_2)]

        timetable_2a = timetable  # starts at week 0 -> offset = 0
        timetable_2b = copy.deepcopy(timetable)  # starts at week 6 -> offset = 6
        timetable_2b.update_offset(5)

        construct_timetable_2a = ct.ConstructTimeTable(events_list=events_2a,
                                                       courses_set=self.courses_set,
                                                       timetable=timetable_2a)
        construct_timetable_2b = ct.ConstructTimeTable(events_list=events_2b,
                                                       courses_set=self.courses_set,
                                                       timetable=timetable_2b)
        events_2a, timetable_2a = construct_timetable_2a.construct()
        events_2b, timetable_2b = construct_timetable_2b.construct()
        feasible_timetable_2a = ft.FeasibleTimetable(events=events_2a,
                                                     timetable=timetable_2a)
        feasible_timetable_2b = ft.FeasibleTimetable(events=events_2b,
                                                     timetable=timetable_2b)
        events_2a, timetable_2a = feasible_timetable_2a.tabu_search()  # first 6 weeks
        events_2b, timetable_2b = feasible_timetable_2b.tabu_search()  # second 6 weeks

        # events type 3
        print("Type 3")
        timetable_3a = timetable_2a  # starts at week 0 -> offset = 0
        timetable_3b = copy.deepcopy(timetable_2a)  # starts at week 3 -> offset = 3
        timetable_3b.update_offset(3)
        timetable_3c = timetable_2b  # starts at week 6 -> offset = 6
        timetable_3d = copy.deepcopy(timetable_2b)  # starts at week 9 -> offset = 9
        timetable_3d.update_offset(9)

        events_3 = list(self.split(self.events_3, 4))
        events_3a = events_3[0]
        events_3b = events_3[1]
        events_3c = events_3[2]
        events_3d = events_3[3]

        ct_3a = ct.ConstructTimeTable(events_list=events_3a,
                                      courses_set=self.courses_set,
                                      timetable=timetable_3a)
        ct_3b = ct.ConstructTimeTable(events_list=events_3b,
                                      courses_set=self.courses_set,
                                      timetable=timetable_3b)
        ct_3c = ct.ConstructTimeTable(events_list=events_3c,
                                      courses_set=self.courses_set,
                                      timetable=timetable_3c)
        ct_3d = ct.ConstructTimeTable(events_list=events_3d,
                                      courses_set=self.courses_set,
                                      timetable=timetable_3d)
        events_3a, timetable_3a = ct_3a.construct()
        events_3b, timetable_3b = ct_3b.construct()
        events_3c, timetable_3c = ct_3c.construct()
        events_3d, timetable_3d = ct_3d.construct()

        ft_3a = ft.FeasibleTimetable(events=events_3a,
                                     timetable=timetable_3a)
        ft_3b = ft.FeasibleTimetable(events=events_3b,
                                     timetable=timetable_3b)
        ft_3c = ft.FeasibleTimetable(events=events_3c,
                                     timetable=timetable_3c)
        ft_3d = ft.FeasibleTimetable(events=events_3d,
                                     timetable=timetable_3d)
        events_3a, timetable_3a = ft_3a.tabu_search()
        events_3b, timetable_3b = ft_3b.tabu_search()
        events_3c, timetable_3c = ft_3c.tabu_search()
        events_3d, timetable_3d = ft_3d.tabu_search()

        # events type 4
        print("Type 4")
        timetable_4a = timetable_3a  # starts at week 0 -> offset = 0
        timetable_4b = copy.deepcopy(timetable_3a)  # starts at week 1 -> offset = 1
        timetable_4b.update_offset(1)
        timetable_4c = copy.deepcopy(timetable_3a)  # starts at week 2 -> offset = 2
        timetable_4b.update_offset(2)
        timetable_4d = timetable_3b  # starts at week 3 -> offset = 3
        timetable_4e = copy.deepcopy(timetable_3b)  # starts at week 4 -> offset = 4
        timetable_4e.update_offset(4)
        timetable_4f = copy.deepcopy(timetable_3b)  # starts at week 5 -> offset = 5
        timetable_4f.update_offset(5)
        timetable_4g = timetable_3c  # starts at week 6 -> offset = 6
        timetable_4h = copy.deepcopy(timetable_3c)  # starts at week 7 -> offset = 7
        timetable_4h.update_offset(7)
        timetable_4i = copy.deepcopy(timetable_3c)  # starts at week 8 -> offset = 8
        timetable_4i.update_offset(8)
        timetable_4j = timetable_3d  # starts at week 9 -> offset = 9
        timetable_4k = copy.deepcopy(timetable_3d)  # starts at week 10 -> offset = 10
        timetable_4k.update_offset(10)
        timetable_4l = copy.deepcopy(timetable_3d)  # starts at week 11 -> offset = 11
        timetable_4l.update_offset(11)

        events_4 = list(self.split(self.events_4, 12))
        events_4a = events_4[0]
        events_4b = events_4[1]
        events_4c = events_4[2]
        events_4d = events_4[3]
        events_4e = events_4[4]
        events_4f = events_4[5]
        events_4g = events_4[6]
        events_4h = events_4[7]
        events_4i = events_4[8]
        events_4j = events_4[9]
        events_4k = events_4[10]
        events_4l = events_4[11]

        ct_4a = ct.ConstructTimeTable(events_list=events_4a,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4a)
        ct_4b = ct.ConstructTimeTable(events_list=events_4b,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4b)
        ct_4c = ct.ConstructTimeTable(events_list=events_4c,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4c)
        ct_4d = ct.ConstructTimeTable(events_list=events_4d,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4d)
        ct_4e = ct.ConstructTimeTable(events_list=events_4e,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4e)
        ct_4f = ct.ConstructTimeTable(events_list=events_4f,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4f)
        ct_4g = ct.ConstructTimeTable(events_list=events_4g,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4g)
        ct_4h = ct.ConstructTimeTable(events_list=events_4h,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4h)
        ct_4i = ct.ConstructTimeTable(events_list=events_4i,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4i)
        ct_4j = ct.ConstructTimeTable(events_list=events_4j,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4j)
        ct_4k = ct.ConstructTimeTable(events_list=events_4k,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4k)
        ct_4l = ct.ConstructTimeTable(events_list=events_4l,
                                      courses_set=self.courses_set,
                                      timetable=timetable_4l)

        events_4a, timetable_4a = ct_4a.construct()
        events_4b, timetable_4b = ct_4b.construct()
        events_4c, timetable_4c = ct_4c.construct()
        events_4d, timetable_4d = ct_4d.construct()
        events_4e, timetable_4e = ct_4e.construct()
        events_4f, timetable_4f = ct_4f.construct()
        events_4g, timetable_4g = ct_4g.construct()
        events_4h, timetable_4h = ct_4h.construct()
        events_4i, timetable_4j = ct_4i.construct()
        events_4j, timetable_4i = ct_4j.construct()
        events_4k, timetable_4k = ct_4k.construct()
        events_4l, timetable_4l = ct_4l.construct()

        ft_4a = ft.FeasibleTimetable(events=events_4a,
                                     timetable=timetable_4a)
        ft_4b = ft.FeasibleTimetable(events=events_4b,
                                     timetable=timetable_4b)
        ft_4c = ft.FeasibleTimetable(events=events_4c,
                                     timetable=timetable_4c)
        ft_4d = ft.FeasibleTimetable(events=events_4d,
                                     timetable=timetable_4d)
        ft_4e = ft.FeasibleTimetable(events=events_4e,
                                     timetable=timetable_4e)
        ft_4f = ft.FeasibleTimetable(events=events_4f,
                                     timetable=timetable_4f)
        ft_4g = ft.FeasibleTimetable(events=events_4g,
                                     timetable=timetable_4g)
        ft_4h = ft.FeasibleTimetable(events=events_4h,
                                     timetable=timetable_4h)
        ft_4i = ft.FeasibleTimetable(events=events_4i,
                                     timetable=timetable_4i)
        ft_4j = ft.FeasibleTimetable(events=events_4j,
                                     timetable=timetable_4j)
        ft_4k = ft.FeasibleTimetable(events=events_4k,
                                     timetable=timetable_4k)
        ft_4l = ft.FeasibleTimetable(events=events_4l,
                                     timetable=timetable_4l)

        events_4a, timetable_4a = ft_4a.tabu_search()
        events_4b, timetable_4b = ft_4b.tabu_search()
        events_4c, timetable_4c = ft_4c.tabu_search()
        events_4d, timetable_4d = ft_4d.tabu_search()
        events_4e, timetable_4e = ft_4e.tabu_search()
        events_4f, timetable_4f = ft_4f.tabu_search()
        events_4g, timetable_4g = ft_4g.tabu_search()
        events_4h, timetable_4h = ft_4h.tabu_search()
        events_4i, timetable_4j = ft_4i.tabu_search()
        events_4j, timetable_4i = ft_4j.tabu_search()
        events_4k, timetable_4k = ft_4k.tabu_search()
        events_4l, timetable_4l = ft_4l.tabu_search()

        # fixing unplaced events
        # type 1
        unplaced_events = []
        for i in range(12):
            unplaced_events += copy.deepcopy(events_1)
        # type 2
        for i in range(6):
            unplaced_events += copy.deepcopy(events_2a) + copy.deepcopy(events_2b)
        # type 3
        for i in range(3):
            unplaced_events += copy.deepcopy(events_3a) + copy.deepcopy(events_3b) + copy.deepcopy(events_3c) + copy.deepcopy(events_3d)
        # type 4
        unplaced_events += copy.deepcopy(events_4a) + copy.deepcopy(events_4b) + copy.deepcopy(events_4c) + copy.deepcopy(events_4d) + copy.deepcopy(events_4e) + copy.deepcopy(events_4f)
        unplaced_events += copy.deepcopy(events_4g) + copy.deepcopy(events_4h) + copy.deepcopy(events_4i) + copy.deepcopy(events_4j) + copy.deepcopy(events_4k) + copy.deepcopy(events_4l)
        print("unplaced: "+str(len(unplaced_events)))
        timetable_13 = pi.create_initial_timetable()
        timetable.update_offset(12)
        random.shuffle(unplaced_events)
        ct_13 = ct.ConstructTimeTable(events_list=unplaced_events,
                                      courses_set=self.courses_set,
                                      timetable=timetable_13)
        events_13, timetable_13 = ct_13.construct()
        print(len(events_13))

        # test
        l = [(timetable_4a, [1]),
                (timetable_4b, [2]),
                (timetable_4c, [3]),
                (timetable_4d, [4]),
                (timetable_4e, [5]),
                (timetable_4f, [6]),
                (timetable_4g, [7]),
                (timetable_4h, [8]),
                (timetable_4i, [9]),
                (timetable_4j, [10]),
                (timetable_4k, [11]),
                (timetable_4l, [12]),
                (timetable_13, [13])]
        for index, tup in enumerate(l):
            fst = tup[0]
            count = 0
            for value in fst.timetable.values():
                if value is not None:
                    count += 1
            print("Timetable "+str(index)+"  "+str(count))

        return [(timetable_4a, [1]),
                (timetable_4b, [2]),
                (timetable_4c, [3]),
                (timetable_4d, [4]),
                (timetable_4e, [5]),
                (timetable_4f, [6]),
                (timetable_4g, [7]),
                (timetable_4h, [8]),
                (timetable_4i, [9]),
                (timetable_4j, [10]),
                (timetable_4k, [11]),
                (timetable_4l, [12]),
                (timetable_13, [13])]

        # return [(timetable, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])]

    @staticmethod
    def split(a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
