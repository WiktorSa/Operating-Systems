from Disc import Disc
from Request import Request
from Algorithms import FCFS, SSTF, SCAN, CSCAN
from Algorithms_EDF import FCFS_EDF, SSTF_EDF, SCAN_EDF, CSCAN_EDF
from Algorithms_FD_SCAN import FCFS_FD_SCAN, SSTF_FD_SCAN, SCAN_FD_SCAN, CSCAN_FD_SCAN
import random
import copy


# This function will calculate the mean amount of seek operations that needed to be done to go over all the requests
def Score(no_cycles, no_requests, no_real_requests, entrance_position, size_of_disc, is_going_left):
    requests = []
    real_time_requests = []
    disc = Disc(entrance_position, size_of_disc)
    sum_FCFS = 0
    sum_SSTF = 0
    sum_SCAN = 0
    sum_CSCAN = 0
    sum_FCFS_EDF = 0
    sum_SSTF_EDF = 0
    sum_SCAN_EDF = 0
    sum_CSCAN_EDF = 0
    sum_FCFS_FD_SCAN = 0
    sum_SSTF_FD_SCAN = 0
    sum_SCAN_FD_SCAN = 0
    sum_CSCAN_FD_SCAN = 0

    for i in range(0, no_cycles):
        # Generating processes. At least one process should appear every 20 seconds
        index = 5
        time = 0
        chance_for_request_to_appear = 0.05
        # We start with 5 requests
        requests.append(Request(0, random.randint(0, size_of_disc), 0))
        requests.append(Request(1, random.randint(0, size_of_disc), 0))
        requests.append(Request(2, random.randint(0, size_of_disc), 0))
        requests.append(Request(3, random.randint(0, size_of_disc), 0))
        requests.append(Request(4, random.randint(0, size_of_disc), 0))
        # And we add other requests (at least 1 every 20 seconds)
        while len(requests) <= no_requests:
            if random.random() <= chance_for_request_to_appear:
                requests.append(Request(index, random.randint(0, size_of_disc), time))
                index += 1
                chance_for_request_to_appear = 0.05
            else:
                chance_for_request_to_appear += 0.05

            time += 1

        # Similar thing goes for real time requests (but it will appear every 34 seconds)
        index = 0
        time = 500
        chance_for_request_to_appear = 0.03
        while len(real_time_requests) <= no_real_requests:
            if random.random() <= chance_for_request_to_appear:
                real_time_requests.append(Request(index, random.randint(0, size_of_disc), time, True,
                                                  random.randint(40, 140)))
                index += 1
                chance_for_request_to_appear = 0.03
            else:
                chance_for_request_to_appear += 0.03

            time += 1

        sum_FCFS += FCFS(copy.deepcopy(requests), copy.deepcopy(disc))
        sum_SSTF += SSTF(copy.deepcopy(requests), copy.deepcopy(disc))
        sum_SCAN += SCAN(copy.deepcopy(requests), copy.deepcopy(disc), is_going_left)
        sum_CSCAN += CSCAN(copy.deepcopy(requests), copy.deepcopy(disc), is_going_left)

        sum_FCFS_EDF += FCFS_EDF(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc))
        sum_SSTF_EDF += SSTF_EDF(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc))
        sum_SCAN_EDF += SCAN_EDF(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc),
                                 is_going_left)
        sum_CSCAN_EDF += CSCAN_EDF(copy.deepcopy(requests), copy.deepcopy(real_time_requests), copy.deepcopy(disc),
                                   is_going_left)

        sum_FCFS_FD_SCAN += FCFS_FD_SCAN(copy.deepcopy(requests), copy.deepcopy(real_time_requests),
                                         copy.deepcopy(disc))
        sum_SSTF_FD_SCAN += SSTF_FD_SCAN(copy.deepcopy(requests), copy.deepcopy(real_time_requests),
                                         copy.deepcopy(disc))
        sum_SCAN_FD_SCAN += SCAN_FD_SCAN(copy.deepcopy(requests), copy.deepcopy(real_time_requests),
                                         copy.deepcopy(disc), is_going_left)
        sum_CSCAN_FD_SCAN += CSCAN_FD_SCAN(copy.deepcopy(requests), copy.deepcopy(real_time_requests),
                                           copy.deepcopy(disc), is_going_left)

        requests.clear()
        real_time_requests.clear()

        print("Cycle " + str(i) + " finished\n")

    print()
    print("FCFS average: ", sum_FCFS/no_cycles)
    print("SSTF average: ", sum_SSTF / no_cycles)
    print("SCAN average: ", sum_SCAN / no_cycles)
    print("CSCAN average: ", sum_CSCAN / no_cycles)
    print("FCFS-EDF average: ", sum_FCFS_EDF / no_cycles)
    print("SSTF-EDF average: ", sum_SSTF_EDF / no_cycles)
    print("SCAN-EDF average: ", sum_SCAN_EDF / no_cycles)
    print("CSCAN-EDF average: ", sum_CSCAN_EDF / no_cycles)
    print("FCFS-FD-SCAN average: ", sum_FCFS_FD_SCAN / no_cycles)
    print("SSTF-FD-SCAN average: ", sum_SSTF_FD_SCAN / no_cycles)
    print("SCAN-FD-SCAN average: ", sum_SCAN_FD_SCAN / no_cycles)
    print("CSCAN-FD-SCAN average: ", sum_CSCAN_FD_SCAN / no_cycles)
