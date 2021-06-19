import collections
import numpy as np
import random
import copy
from process.Process import Process
from algorithms.FCFS import FCFS
from algorithms.SJF import SJF
from algorithms.RR import RR


def Score(no_simulations: int, no_processes: int, quant: int):
    arrival_times = np.empty(shape=no_processes, dtype=np.int32)
    processes = collections.deque()
    fcfs = FCFS(no_simulations)
    sjf = SJF(no_simulations)
    rr = RR(no_simulations, quant)

    for i in range(no_simulations):
        # Generate waiting times for every process (it's important that 5 of time have arrival time = 0)
        for j in range(5):
            arrival_times[j] = 0
        for j in range(5, no_processes):
            arrival_times[j] = random.randint(0, 9999)

        arrival_times.sort()

        for j in range(no_processes):
            processes.append(Process(j, random.randint(1, 30), arrival_times[j]))

        print("Simulation: ", (i+1))
        fcfs.perform_simulation(copy.deepcopy(processes))
        sjf.perform_simulation(copy.deepcopy(processes))
        rr.perform_simulation(copy.deepcopy(processes))

        processes.clear()

    print("Average result after {no_simulations} simulations".format(no_simulations=no_simulations))
    print("FCFS average: ", fcfs.get_results_all_simulations())
    print("SJF average:  ", sjf.get_results_all_simulations())
    print("RR average:   ", rr.get_results_all_simulations())
