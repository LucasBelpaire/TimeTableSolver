import construct_timetable as ctt
import process_input
import generate_output as go
import time
import feasible_timetable


def main():
    start_time = time.perf_counter()
    # Initialize all variables needed to create a time table
    print("Starting to process input.  " + str(time.perf_counter() - start_time))
    process_input.set_global_variables()
    print("Processing input completed.  " + str(time.perf_counter() - start_time))

    # Start the first phase of the feasibility process: construction phase
    print("Starting initial construction of timetable.  " + str(time.perf_counter() - start_time))
    ctt.construct_time_table()
    print("Initial construction of timetable finished.  " + str(time.perf_counter() - start_time))

    # Start the second phase of the feasibility process: tabu search
    print("Starting tabu search phase." + str(time.perf_counter() - start_time))
    feasible_timetable.tabu_search()
    print("Completed tabu search phase.  " + str(time.perf_counter() - start_time))

    # Start generating the output file
    print("Starting to generate output.  " + str(time.perf_counter() - start_time))
    go.generate_output_from_time_table()
    print("Generating output completed.  " + str(time.perf_counter() - start_time))


if __name__ == '__main__':
    main()
