"""
    This module holds all variables which the different parts of the program need.
"""

# Variables:
events = []  # events is a list of all course events
time_table = {}  # the TT is represented by a dictionary. key: (room_fi_number, time_slot)
number_of_time_slots = None  # amount of possible course hours per week
empty_positions = []  # holds all empty positions, consists of (room_fi_number, time_slot)
unplaced_events = []  # will hold all events that could not be placed.
generalInfo = None  # Object that will hold all general/meta information

# Mappings:
courses_dict = {}  # key: (course)code. value: course object
lecturers_dict = {}  # key: ugent_id, value: lecturer object
curricula_dict = {}  # key: (curriculum)code. value: curriculum object
sites_dict = {}  # key: site_id. value: site object
class_rooms_dict = {}  # key: fi_number. value: class_room object



