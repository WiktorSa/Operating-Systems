import copy

import numpy as np
from process.process import Process
import algorithms


class Result:
    def __init__(self, no_pages: np.array, start_pages: np.array, end_pages: np.array,
                 localities_of_reference: np.array, how_large_localities: np.array, how_often_localities: np.array):
        self.no_pages = no_pages
        self.start_pages = start_pages
        self.end_pages = end_pages
        self.localities_of_reference = localities_of_reference
        self.how_large_localities = how_large_localities
        self.how_often_localities = how_often_localities

    def get_results(self, no_simulations: int, no_frames: int, time_frame: int, l: float, u: float, h: float, c: int):
        processes = [Process(self.no_pages[i], self.start_pages[i], self.end_pages[i], self.localities_of_reference[i],
                             self.how_large_localities[i], self.how_often_localities[i], time_frame, c)
                     for i in range(len(self.no_pages))]

        equal_algorithm = algorithms.EqualAlgorithm(no_frames, len(processes), no_simulations, False)
        proportional_algorithm = algorithms.ProportionalAlgorithm(no_frames, len(processes), no_simulations, False)
        page_fault_frequency = algorithms.PageFaultFrequency(no_frames, len(processes), no_simulations, True,
                                                             time_frame, l, u, h)
        working_set = algorithms.WorkingSet(no_frames, len(processes), no_simulations, True, time_frame, c)

        for i in range(no_simulations):
            for process in processes:
                process.pages.generate_new_pages()

            print("Simulation number: ", i + 1)
            equal_algorithm.perform_simulation(copy.deepcopy(processes))
            print()
            proportional_algorithm.perform_simulation(copy.deepcopy(processes))
            print()
            page_fault_frequency.perform_simulation(copy.deepcopy(processes))
            print()
            working_set.perform_simulation(copy.deepcopy(processes))
            print()

        print("Final results")
        print("\nEqual algorithm")
        equal_algorithm.print_results()
        print("\nProportional algorithm")
        proportional_algorithm.print_results()
        print("\nPage Fault Frequency")
        page_fault_frequency.print_results()
        print("\nWorking Set")
        working_set.print_results()
