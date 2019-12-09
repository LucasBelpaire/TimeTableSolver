import construct_timetable as ctt
import process_input
import general_info as gi
import generate_output as go
import time
import timetable_builder as tb
import pickle
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
    courses_set = gi.courses_set
    print("Processing input completed.  " + str(time.perf_counter() - start_time))

    # Start constructing timetable
    timetable_builder = tb.TimeTableBuilder(timetable=timetable,
                                            events_1=events_1,
                                            events_2=events_2,
                                            events_3=events_3,
                                            events_4=events_4,
                                            courses_set=courses_set,
                                            start_time=start_time)
    timetable_complete = timetable_builder.build_timetable()
    # Start generating the output file
    print("Starting to generate output.  " + str(time.perf_counter() - start_time))
    go.generate_output_from_time_table(timetable_complete)
    print("Generating output completed.  " + str(time.perf_counter() - start_time))


if __name__ == '__main__':
    main()
