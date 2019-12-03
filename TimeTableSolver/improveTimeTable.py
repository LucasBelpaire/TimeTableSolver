import time
import math


def simulated_annealing(max, min, steps):
    """
    This function will execute simulated annealing on the current time table.
    It's goal is to make it more correct in connection with the soft constraints.
    The time table in this phase is feasible, so it doesn't break any hard constraints
    :param max:
    :param min:
    :param steps:
    :return: best cost and best timetable
    """
    starting_time = time.clock()

    while (time.clock() - starting_time) < 100:
        t_factor = -math.log(float(max)/min)

        no_improvement = 0

        iterations = 0

        while bes