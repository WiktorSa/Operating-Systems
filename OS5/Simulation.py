import copy
import heapq
import random
import numpy as np
from Algorithm1 import Algorithm1
from Algorithm2 import Algorithm2
from Algorithm3 import Algorithm3
from Process import Process


def perform_simulation(no_simulations, processors, no_processes, max_searches_alg1, max_searches_alg2,
                       max_searches_alg3, uneven_processes):
    alg1 = Algorithm1(copy.deepcopy(processors), max_searches_alg1)
    alg2 = Algorithm2(copy.deepcopy(processors), max_searches_alg2)
    alg3 = Algorithm3(copy.deepcopy(processors), max_searches_alg2, max_searches_alg3)

    for i in range(no_simulations):
        entrance_times = np.random.randint(low=0, high=3000, size=no_processes)
        entrance_times = np.sort(entrance_times, kind='heapsort')
        processes = np.empty(shape=no_processes, dtype=Process)
        # Generate processes so that they mainly go to a few processors
        if uneven_processes:
            for j in range(0, no_processes-1, 2):
                processes[j] = Process(entrance_times[j], random.randint(3, 15), random.randint(10, 50),
                                 random.randrange(0, 3))
                processes[j+1] = Process(entrance_times[j+1], random.randint(3, 15), random.randint(10, 50),
                                 random.randrange(0, len(processors)))
            # Handle odd number of processes
            if processes[-1] is None:
                processes[-1] = Process(entrance_times[-1], random.randint(3, 15), random.randint(10, 50),
                                 random.randrange(0, len(processors)))

        else:
            for j in range(no_processes):
                processes[j] = Process(entrance_times[j], random.randint(3, 15), random.randint(10, 50),
                                 random.randrange(0, len(processors)))

        print(f'Simulation number: {i + 1}')

        alg1.perform_simulation(copy.deepcopy(processes))
        alg2.perform_simulation(copy.deepcopy(processes))
        alg3.perform_simulation(copy.deepcopy(processes))

        print("\nAlgorithm 1 results:")
        alg1.print_result_one_simulation()
        print("\nAlgorithm 2 results:")
        alg2.print_result_one_simulation()
        print("\nAlgorithm 3 results:")
        alg3.print_result_one_simulation()
        print()

        alg1.save_results()
        alg2.save_results()
        alg3.save_results()

        alg1.reset()
        alg2.reset()
        alg3.reset()

    print("Final results")
    print("\nAlgorithm 1 results:")
    alg1.print_results_many_simulations()
    print("\nAlgorithm 2 results:")
    alg2.print_results_many_simulations()
    print("\nAlgorithm 3 results:")
    alg3.print_results_many_simulations()
