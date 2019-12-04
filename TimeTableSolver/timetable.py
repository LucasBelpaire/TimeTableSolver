import hard_constraints as hc
import general_info as gi


class TimeTable:

    def __init__(self, timetable, occupied_positions, empty_positions):
        self.timetable = timetable
        self.occupied_positions = occupied_positions
        self.empty_positions = empty_positions

    def assign_course_to_position(self, course_event, position):
        """
        This function will assign a course_event to a specific position in the time table.
        :param course_event: instance of CourseEvent, the course event that will be scheduled.
        :param position: (fi_number, time_slot)
        :return: True if the event is successfully scheduled, False otherwise
        """

        if self.timetable[position] is not None:
            self.remove_course_from_position(position)

        if course_event is None:
            return False

        self.timetable[position] = course_event
        course = hc.courses_dict[course_event.course_code]
        room_fi_number = position[0]
        time_slot = position[1]

        for curriculum in course.curricula:
            # adding the time_slot to the list of occupied time_slots
            curriculum.add_occupied_time_slot(time_slot)

        # get a lecturer
        assigned_lecturer = None
        for lecturer in course_event.lecturers:
            if not hc.lecturer_is_occupied_in_time_slot(lecturer, time_slot):
                assigned_lecturer = lecturer
                continue

        assigned_lecturer.add_occupied_time_slot(time_slot)
        course_event.set_assigned_lecturer(assigned_lecturer.ugent_id)

        course.course_hours -= 1
        try:
            self.empty_positions.remove(position)
        except ValueError:
            # event got swapped, so is not part of events.
            return

    def remove_course_from_position(self, position):
        """
        This function will remove a courseEvent from the timetable.
        :param position: (fi_number, time_slot)
        :return: True if the removal is successful, False otherwise
        """
        fi_number = position[0]
        time_slot = position[1]
        if self.timetable[position] is not None:
            course_event = self.timetable[position]
            self.timetable[position] = None
            self.empty_positions.append(position)

            course = gi.courses_dict[course_event.course_code]
            course.course_hours += 1

            # remove the time_slot from the occupied time_sot list from every curriculum
            for curriculum in course.curricula:
                curriculum.remove_occupied_time_slot(time_slot)

            ugent_id = course_event.assigned_lecturer
            lecturer = gi.lecturers_dict[ugent_id]
            lecturer.remove_occupied_time_slot(time_slot)
            course_event.remove_assigned_lecturer()

            return True

        return False
