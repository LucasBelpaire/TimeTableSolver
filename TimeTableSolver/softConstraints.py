"""

    Dit zijn de soft constraints

 - Het verschil tussen het aantal zitplaatsen en het aantal studenten per reservatie dient geminimaliseerd te worden. De lokalen moeten dus zo goed mogelijk passen bij de grootte van de groep.
 - De laatste twee lesuren van de dag dienen vermeden te worden, alsook lesuren in de inhaalweek
 - Vermijd vier of meer opeenvolgende lesuren zonder pauze
 - Vermijd dat studenten op sommige dagen slechts één lesuur hebben

"""
import processInput
from haversine import haversine


def return_not_home_penalty(position, course_event):
    """

    :param position: the position in the time table
    :param course_event: the course we want to schedule
    :return: This function returns the total sum of all distance penalties
    """
    penalty = 0

    room, time_slot = position
    class_room_site_id = room.site_id
    class_room_site = processInput.sites_dict[class_room_site_id]

    current_course = processInput.courses_dict[course_event.course_code]
    curricula_of_course = current_course.curricula

    # iterate over
    total_penalty = 0
    for curriculum in curricula_of_course:
        x_coord_class = class_room_site.x_coord
        y_coord_class = class_room_site.y_coord
        position_class = (x_coord_class, y_coord_class)

        home_of_curriculum = curriculum.home_site
        x_coord_home_of_curriculum = home_of_curriculum.x_coord
        y_coord_home_of_curriculum = home_of_curriculum.y_coord
        position_home = (x_coord_home_of_curriculum, y_coord_home_of_curriculum)

        distance = haversine(position_class, position_home)
        total_penalty += distance * processInput.kilometer_penalty

    return total_penalty
