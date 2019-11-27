"""

    Dit zijn de soft constraints

 - Het verschil tussen het aantal zitplaatsen en het aantal studenten per reservatie dient geminimaliseerd te worden. De lokalen moeten dus zo goed mogelijk passen bij de grootte van de groep.
 - De laatste twee lesuren van de dag dienen vermeden te worden, alsook lesuren in de inhaalweek
 - Vermijd vier of meer opeenvolgende lesuren zonder pauze
 - Vermijd dat studenten op sommige dagen slechts één lesuur hebben

"""
import processInput


def return_not_home_penalty(room, course):
    """

    :param room: the specific room we want to process
    :param course: the course we want to schedule
    :return: This function returns the total sum of all distance penalties
    """
    penalty = 0

    class_room_site = processInput.sites_dict[room.site_id]

    curricula_of_courses = course.curricula

    # iterate over
    total_penalty = 0
    for curriculum in curricula_of_courses:

        if curriculum.home_site == room.site_id:
            continue

        x_coord_class = class_room_site.x_coord
        y_coord_class = class_room_site.y_coord
        position_class = (x_coord_class, y_coord_class)

        home_of_curriculum = processInput.sites_dict[curriculum.home_site]
        x_coord_home_of_curriculum = home_of_curriculum.x_coord
        y_coord_home_of_curriculum = home_of_curriculum.y_coord
        position_home = (x_coord_home_of_curriculum, y_coord_home_of_curriculum)

        #distance = haversine(position_class, position_home)
        total_penalty += 5

    return total_penalty
