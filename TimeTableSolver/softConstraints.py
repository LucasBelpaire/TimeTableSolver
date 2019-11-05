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
    # TODO: deze functie moet nog rekening houden met de hard constraint voor de roomcapacityç!!
    room, timeslot = position
    return hardConstraints.course_fits_in_to_time_slot(course, timeslot)


