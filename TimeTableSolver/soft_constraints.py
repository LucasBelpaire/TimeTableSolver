"""
    This module holds all soft constraints.
"""
import global_variables as gv
from haversine import haversine


def return_not_home_penalty(room, course_event):
    """
    This function calculates the not_home penalty for a given room and course.
    :param room: instance of ClassRoom
    :param course_event: instance of CourseEvent
    :return: The total not_home penalty.
    """
    class_room_site = gv.sites_dict[room.site_id]

    curricula_of_courses = course_event.curricula

    total_penalty = 0
    for curriculum in curricula_of_courses: 
        if curriculum.home_site == room.site_id:
            continue

        x_coord_class = float(class_room_site.x_coord)
        y_coord_class = float(class_room_site.y_coord)
        position_class = (x_coord_class, y_coord_class)

        home_of_curriculum = gv.sites_dict[curriculum.home_site]
        x_coord_home_of_curriculum = float(home_of_curriculum.x_coord)
        y_coord_home_of_curriculum = float(home_of_curriculum.y_coord)
        position_home = (x_coord_home_of_curriculum, y_coord_home_of_curriculum)

        distance = haversine(position_class, position_home)

        total_penalty += gv.generalInfo.kilometer_penalty * distance

    return total_penalty
