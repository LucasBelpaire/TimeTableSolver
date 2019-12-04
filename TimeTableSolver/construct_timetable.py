import time
import hard_constraints as hc
import soft_constraints as sc
import math
import general_info as gi


class ConstructTimeTable:

    def __init__(self, events_list, courses_set, time_table):
        self.events = events_list
        self.courses = courses_set
        self.time_table = time_table

    def construct_time_table(self):
        """
        This function will try to build an initial timetable using an heuristic approach.
        It will prioritize "harder" events, and try to place them in their best positions.
        This process will end if either a feasible timetable is build, or the time limit is reached.
        """

        unplaced_events = []

        # the events get sorted, harder to place events will get placed first
        sorted_events = self.order_course_events_by_priority(self.events, self.courses)
        # collect all available positions for this event
        for index, course_event in enumerate(sorted_events):
            available_positions = []
            for room_fi_number, time_slot in self.time_table.empty_postions:
                room = gi.class_rooms_dict[room_fi_number]
                fits = hc.course_event_fits_into_time_slot(course_event, time_slot) and hc.room_capacity_constraint(
                    course_event, room)
                if fits:
                    available_positions.append((room_fi_number, time_slot))
            # if no available positions were found, the event gets added to unplaced_events
            if len(available_positions) == 0:
                unplaced_events.append(course_event)
                continue

            # sort the available positions by possible fit, the best one gets selected
            sorted_positions = self.order_positions_by_priority(available_positions, course_event)
            best_fit = sorted_positions.pop(0)
            self.time_table.assign_course_to_position(course_event, best_fit)
            return unplaced_events

    def order_course_events_by_priority(self, course_events, courses_set):
        """
        Orders the course events by priority,
        events with a higher priority will be scheduled first.
        :param course_events: a list of instances of CourseEvents
        :param courses_set: a set of all possible courses
        :return: the sorted list of events
        """
        course_events_ranking = {}

        for event in course_events:
            course_events_ranking[event.course_code] = []

        lectures_amount = self.count_lectures_per_course(courses_set)

        # fill the ranking array with all rankings in descending priority
        for course_event in course_events:
            # highest priority
            # we invert the solution, because the lowest value has the highest priority
            # and we want to order from biggest priority value to smallest
            rank1 = self.get_events_ranking1(course_event, lectures_amount[course_event.course_code])
            course_events_ranking[course_event.course_code].append(1 / rank1 if rank1 != 0 else 0)
            course_events_ranking[course_event.course_code].append(self.get_events_ranking2(course_event, list(courses_set)))

        courses_sorted = list(course_events)
        courses_sorted.sort(key=lambda cr: course_events_ranking[cr.course_code], reverse=True)
        return courses_sorted

    @staticmethod
    def count_lectures_per_course(courses_set):
        """
        Get the amount of lectures per course.
        :param courses_set: a list of course events
        :return: a dictionary containing the amount of course events per course
        """
        lectures_amount = {}
        for course in list(courses_set):
            lectures_amount[course.code] = course.course_hours
        return lectures_amount

    @staticmethod
    def compute_amount_of_available_time_slots(course_event):
        """
        :param course_event: an instance of course event
        :return: the total number of available time slots for the given course
        """
        amount = 0
        for i in range(gi.total_course_hours):
            if hc.course_event_fits_into_time_slot(course_event, i):
                amount += 1
        return amount

    @staticmethod
    def have_common_lecturers(course_event, course):
        """
        Checks if the two courses have a common lecturer.
        :param course_event: instance of CourseEvent
        :param course: instance of course
        :return: True if there is at least one common lecturer, False otherwise
        """
        for lecturer in course_event.lecturers:
            if lecturer in course.lecturers:
                return True
        return False

    @staticmethod
    def have_common_curricula(course_event, course):
        """
        Checks if two courses have a common curriculum.
        :param course_event: instance of CourseEvent
        :param course: instance of course
        :return: True if there is at least one common curriculum, False otherwise
        """
        for curriculum in course_event.curricula:
            if curriculum in course.curricula:
                return True
        return False

    def get_events_ranking1(self, course_event, amount_of_events):
        """
        Returns priority based on courses which consist of many lectures,
        but have only a small number of available time slots.
        A smaller value means a higher priority.
        :param course_event: an instance of course event
        :param amount_of_events: number of events that will take place for the given course
        :return: the rank of the given course
        """
        total_number_of_available_time_slots = self.compute_amount_of_available_time_slots(course_event)
        rank = total_number_of_available_time_slots / math.sqrt(amount_of_events)
        return rank

    def get_events_ranking2(self, course_event, courses):
        """
        Order priority by conflict, a conflict is a course_event with has the same lecturer as another event,
        or is part of the same curriculum of another event.
        :param course_event: an instance of course event
        :param courses: a list of all courses
        :return: the rank of the given course
        """
        amount = 0
        for curr_course in courses:
            if course_event.course_code != curr_course.code:
                if self.have_common_lecturers(course_event, curr_course) or self.have_common_curricula(course_event, curr_course):
                    amount += 1
        rank = amount
        return rank

    def order_positions_by_priority(self, positions, course_event):
        """
        This function will order all available positions for a given course_event.
        The best position will be the first in the returned list.
        We sort using rank1, if two positions have an equal rank1, than rank2 decides which one gets priority.
        :param positions: all available positions, (fi_number, time_slot)
        :param course_event: instance of CourseEvent
        :return: sorted list of positions
        """
        positions_ranking = {}

        for room_fi_number, time_slot in positions:
            positions_ranking[room_fi_number] = []

        for room_fi_number, time_slot in positions:
            room = gi.class_rooms_dict[room_fi_number]
            rank1 = self.get_positions_ranking1(room, course_event)
            positions_ranking[room.fi_number].append(rank1)
            rank2 = self.get_positions_ranking2(room, course_event)
            positions_ranking[room.fi_number].append(rank2)
        positions.sort(key=lambda tup: positions_ranking[tup[0]], reverse=False)
        return positions

    @staticmethod
    def get_positions_ranking1(room, course_event):
        """
        Rank1 is equal to the not home penalty, the smaller the better.
        :param room: an instance of ClassRoom
        :param course_event: instance of CourseEvent
        :return: the not home penalty
        """
        return sc.return_not_home_penalty(room, course_event)

    @staticmethod
    def get_positions_ranking2(room, course_event):
        """
        Rank2 indicates how many empty places there are left in a room.
        The smaller the better.
        :param room: an instance of room
        :param course_event: an instance of CourseEvent
        :return:
        """
        return room.capacity - course_event.student_amount
