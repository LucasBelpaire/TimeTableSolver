import processInput
import random


def get_random_time_slots():
    """
    :return: two different random time slots, integers
    """
    time_slot_1 = random.randrange(processInput.generalInfo.total_course_hours)
    time_slot_2 = random.randrange(processInput.generalInfo.total_course_hours)
    while time_slot_1 == time_slot_2:
        time_slot_2 = random.randrange(processInput.generalInfo.total_course_hours)
    return time_slot_1, time_slot_2
