import global_variables
import process_input
import json
import math


def generate_output_from_time_table():
    """
    This function will convert the end solution time table to a correct json file
    The JSON file will contain all reservation for a room during the semester
    :return: we return true if successful
    """

    end_time_table = global_variables.time_table

    room_reservation_dict = []

    for position, course_event in end_time_table.items():
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

            # we kijken in welke weken we deze reservatie doen
            weeks = [1,2,3,4,5,6,7,8,9,10,11,12]

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