from disc.Disc import Disc
from request.Request import Request
import algorithms
import algorithms_EDF
import numpy as np
import random
import copy


# Get the results of the simulation
def Score(no_cycles: int, no_requests: int, no_real_requests: int, entrance_position: int, size_of_disc: int,
          is_going_right: bool):
    requests = np.empty(shape=no_requests, dtype=Request)
    real_time_requests = np.empty(shape=no_real_requests, dtype=Request)
    disc = Disc(entrance_position, size_of_disc)

    fcfs = algorithms.FCFS(no_cycles)
    sstf = algorithms.SSTF(no_cycles)
    scan = algorithms.SCAN(no_cycles, is_going_right)
    cscan = algorithms.CSCAN(no_cycles, is_going_right)
    fcfs_edf = algorithms_EDF.FCFS(no_cycles)
    sstf_edf = algorithms_EDF.SSTF(no_cycles)

    for i in range(no_cycles):
        # Generating processes
        # One process should appear every 20 seconds
        # One real time process should appear every 34 seconds
        # At the beginning of the simulation we will have 5 active processes
        requests[0] = Request(0, random.randint(0, size_of_disc), 0)
        requests[1] = Request(1, random.randint(0, size_of_disc), 0)
        requests[2] = Request(2, random.randint(0, size_of_disc), 0)
        requests[3] = Request(3, random.randint(0, size_of_disc), 0)
        requests[4] = Request(4, random.randint(0, size_of_disc), 0)

        index = 5
        index_real_time = 0
        chance_request_appear = 0.05
        chance_real_request_appear = 0.03
        time = 0
        while index < no_requests or index_real_time < no_real_requests:
            # Requests
            if index < no_requests:
                if random.random() <= chance_request_appear:
                    requests[index] = Request(index, random.randint(0, size_of_disc), time)
                    index += 1
                    chance_request_appear = 0.05

                else:
                    chance_request_appear += 0.05

            # Real time requests
            if index_real_time < no_real_requests:
                if random.random() <= chance_real_request_appear:
                    real_time_requests[index_real_time] = Request(index, random.randint(0, size_of_disc), time, True,
                                                                  random.randint(40, 140))
                    index_real_time += 1
                    chance_real_request_appear = 0.03

                else:
                    chance_real_request_appear += 0.03

            time += 1

        fcfs.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(disc))
        sstf.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(disc))
        scan.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(disc))
        cscan.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(disc))
        fcfs_edf.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc))
        sstf_edf.perform_simulaton(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc))

        print("Cycle " + str(i) + " finished\n")

    print("FCFS average: ", fcfs.get_results_many_simulations())
    print("SSTF average: ", sstf.get_results_many_simulations())
    print("SCAN average: ", scan.get_results_many_simulations())
    print("CSCAN average: ", cscan.get_results_many_simulations())
    print("FCFS-EDF average: ", fcfs_edf.get_results_many_simulations())
    print("FCFS-EDF average rejected real time requests: ", fcfs_edf.get_results_many_simulations_rejected())
    print("SSTF-EDF average: ", sstf_edf.get_results_many_simulations())
    print("SSTF-EDF average rejected real time requests: ", sstf_edf.get_results_many_simulations_rejected())
