import process_input
import json
import math


def generate_output_from_time_table(list_of_dicts):
    """
    This function will convert the end solution time table to a correct json file
    The JSON file will contain all reservation for a room during the semester
    :param list_of_dicts: list of tuples: (dictionary, weeks)
    :return: we return true if successful
    """
    room_reservation_dict = []
    for timetable_weeks in list_of_dicts:
        timetable = timetable_weeks[0].timetable
        weeks = timetable_weeks[1]
        for position, course_event in timetable.items():
            # if not none then there is a reservation for this room on the specific time_slot
            if course_event is not None:
                # we extract the course_id
                course = process_input.courses_dict[course_event.course_code]
                course_id = course.code

                # we need the room id
                room_fi_number = position[0]

                # we get the student amount for this reservation
                course_event_student_amount = course_event.student_amount

                days_of_week = {0:"ma",
                                1:"di",
                                2:"wo",
                                3:"do",
                                4:"vr"}

                time_slot = position[1]
                day = days_of_week[math.floor(int(time_slot)/8)]
                hour = (int(time_slot)%8)+1

                # we geven de dagen mee van de week als een lijst van strings
                days = [day]

                # welke uren van de dag deze reservatie nodig is
                hours = [hour]

                # the final reservation we want to write to the JSON file
                end_reservation = {"lokaal": room_fi_number,
                                   "code": course_id,
                                   "aantal": course_event_student_amount,
                                   "dagen":days,
                                   "weken": weeks,
                                   "uren":hours}

                room_reservation_dict.append(end_reservation)

    with open('output/output.json', 'w') as json_file:
        json.dump(room_reservation_dict, json_file)
