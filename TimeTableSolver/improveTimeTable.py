import time
import math
import soft_constraints as sc
import neighborhood

class ImproveTimeTable:

    def __init__(self, timetable):
        """
        The constructor for the third phase the improvement phase
        :param timetable: The feasible timetable that we want to improve
        """
        self.timetable = timetable #this will hold the final time table with the best penalty cost on the end
        self.best_cost = sc.return_total_penalty_of_timetable(self.timetable)
        self.last_cost = self.best_cost

    def simulated_annealing(self, max, min, steps):
        """
        This function will execute simulated annealing on the current time table.
        It's goal is to make it more correct in connection with the soft constraints.
        The time table in this phase is feasible, so it doesn't break any hard constraints
        :param max:
        :param min:
        :param steps:
        :return: best cost and best timetable
        """
        return None

    def swap_time_slots(self):
        time_slot_1, time_slot_2 = neighborhood.get_random_time_slots()

        succesfull, backup1, backup2 = neighborhood.swap_2_time_slots(time_slot_1, time_slot_2)