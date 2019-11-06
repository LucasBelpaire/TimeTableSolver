"""

    Dit zijn de soft constraints

 - Het verschil tussen het aantal zitplaatsen en het aantal studenten per reservatie dient geminimaliseerd te worden. De lokalen moeten dus zo goed mogelijk passen bij de grootte van de groep.
 - De laatste twee lesuren van de dag dienen vermeden te worden, alsook lesuren in de inhaalweek
 - Vermijd vier of meer opeenvolgende lesuren zonder pauze
 - Vermijd dat studenten op sommige dagen slechts één lesuur hebben

"""
import hardConstraints

#
#
def does_course_fits_in_position(course, position):
    #extract the room and timeslot from the course

    room, time_slot = position

    return hardConstraints.course_fits_in_to_time_slot(course, time_slot) \
           and hardConstraints.room_capacity_constraint(course, room)


def room_is_at_home_base(room, course):
    # TODO: zorg dat course ook een array home_site_id heeft, alle homesites van de curricula waartoe het behoort
    return False