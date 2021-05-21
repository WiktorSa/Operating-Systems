from Process import Process
from Algorithms import FCFS, SJF, RR
import random
import copy


# This function will calculate the mean time for waiting for the processor for all activities
def Score(no_cycles, no_processes, quant):
    processes = []
    sum_FCFS = 0
    sum_SJF = 0
    sum_RR = 0

    for i in range(0, no_cycles):
        for j in range(0, no_processes):
            processes.append(Process(j, random.randint(1, 30), random.randint(0, 9999)))

        sum_FCFS += FCFS(copy.deepcopy(processes))
        sum_SJF += SJF(copy.deepcopy(processes))
        sum_RR += RR(copy.deepcopy(processes), quant)
        processes.clear()

        print("Cycle " + str(i) + " finished\n")

    print()
    print("FCFS average: ", sum_FCFS/no_cycles)
    print("SJF average: ", sum_SJF / no_cycles)
    print("RR average: ", sum_RR / no_cycles)
