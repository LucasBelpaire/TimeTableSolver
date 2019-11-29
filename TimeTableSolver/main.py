import construct_time_table as ctt
import process_input
import generate_output as go


def main():
    # Initialize all variables needed to create a time table
    print("Starting to process input.")
    process_input.set_global_variables()
    print("Processing input completed.")

    # Start the first phase of the construction process
    print("Starting initial construction of timetable.")
    ctt.construct_time_table()
    print("Initial construction of timetable finished.")

    print("Starting to generate output")
    go.generate_output_from_time_table()
    print("Generating output completed.")


if __name__ == '__main__':
    main()
