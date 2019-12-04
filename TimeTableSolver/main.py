import construct_timetable as ctt
import process_input
import general_info as gi
import generate_output as go
import global_variables as gv
import process_input as pi
import copy
import time
import feasible_timetable


def main():
    start_time = time.perf_counter()
    # Initialize all variables needed to create a time table
    print("Starting to process input.  " + str(time.perf_counter() - start_time))
    process_input.init_general_info()
    timetable = process_input.create_initial_timetable()
    events_1, events_2 = process_input.create_initial_events_lists()
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
    feasible_timetable.tabu_search()
    print("Completed tabu search phase.  " + str(time.perf_counter() - start_time))

    # Start generating the output file
    print("Starting to generate output.  " + str(time.perf_counter() - start_time))
    go.generate_output_from_time_table()
    print("Generating output completed.  " + str(time.perf_counter() - start_time))


if __name__ == '__main__':
    main()
