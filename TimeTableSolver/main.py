import construct_timetable as ctt
import process_input
import general_info as gi
import generate_output as go
import time
import copy
import feasible_timetable
import improveTimeTable


def main():
    start_time = time.perf_counter()
    # Initialize all variables needed to create a time table
    print("Starting to process input.  " + str(time.perf_counter() - start_time))
    process_input.init_general_info()
    timetable = process_input.create_initial_timetable()
    events_1, events_2, events_3, events_4 = process_input.create_initial_events_lists()
    print(len(events_1))
    courses_set = gi.courses_set
    print("Processing input completed.  " + str(time.perf_counter() - start_time))

    # Start the first phase of the feasibility process: construction phase
    print("Starting initial construction of timetable.  " + str(time.perf_counter() - start_time))
    construct_timetable = ctt.ConstructTimeTable(events_list=events_1,
                                                 courses_set=courses_set,
                                                 timetable=timetable)
    events_1, timetable = construct_timetable.construct()
    print("Initial construction of timetable finished.  " + str(time.perf_counter() - start_time))

    # Start the second phase of the feasibility process: tabu search
    print("Starting tabu search phase. " + str(time.perf_counter() - start_time))
    ftt = feasible_timetable.FeasibleTimetable(events_1,
                                               timetable)
    best_distance, timetable = ftt.tabu_search()
    print("Completed tabu search phase.  " + str(time.perf_counter() - start_time))
    # timetable_2 = copy.deepcopy(timetable)
    # construct_timetable_2a = ctt.ConstructTimeTable(events_list=events_2[len(events_2):],
    #                                                 courses_set=courses_set,
    #                                                 timetable=timetable)
    #
    # construct_timetable_2b = ctt.ConstructTimeTable(events_list=events_2[:len(events_2)],
    #                                                 courses_set=courses_set,
    #                                                 timetable=timetable_2)
    # events_2a, timetable2a = construct_timetable_2a.construct()
    # events_2b, timetable2b = construct_timetable_2b.construct()
    #
    # ftt2a = feasible_timetable.FeasibleTimetable(events_2a,
    #                                              timetable2a)
    # ftt2b = feasible_timetable.FeasibleTimetable(events_2b,
    #                                              timetable2b)
    # best_distance2a, timetable2a = ftt2a.tabu_search()
    # best_distance2b, timetable2b = ftt2b.tabu_search()

    # Start the second phase of the feasibility process: tabu search
    # print("Starting improving phase. " + str(time.perf_counter() - start_time))
    # improve = improveTimeTable.ImproveTimeTable(timetable)
    # total_penalty = improve.best_cost
    # print("total penalty: " + str(total_penalty))
    # print("Completed improving phase.  " + str(time.perf_counter() - start_time))

    # Start generating the output file
    print("Starting to generate output.  " + str(time.perf_counter() - start_time))
    # go.generate_output_from_time_table( [(timetable2a, [1, 2, 3, 4, 5, 6]), (timetable2b, [7, 8, 9, 10, 11, 12])])
    go.generate_output_from_time_table([(timetable, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])])
    print("Generating output completed.  " + str(time.perf_counter() - start_time))


if __name__ == '__main__':
    main()
