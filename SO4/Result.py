"""
This class will keep all the data needed to generate processes and perform simulation
"""
import copy

from Process import Process
from EqualAlgorithm import EqualAlgorithm
from ProportionalAlgorithm import ProportionalAlgorithm
from PageFaultFrequency import PageFaultFrequency
from WorkingSet import WorkingSet


class Result:
    def __init__(self, no_pages, start_pages, end_pages, localities_of_reference=None, how_large_localities=None,
                 how_often_localities=None):
        self.no_pages = no_pages
        self.start_pages = start_pages
        self.end_pages = end_pages
        self.localities_of_reference = localities_of_reference
        if self.localities_of_reference is None:
            self.localities_of_reference = [None] * len(start_pages)
        self.how_large_localities = how_large_localities
        if how_large_localities is None:
            self.how_large_localities = [20] * len(start_pages)
        self.how_often_localities = how_often_localities
        if self.how_often_localities is None:
            self.how_often_localities = [50] * len(start_pages)

    def get_results(self, no_simulations=5, no_frames=40, time_frame=30, l=0.4, u=0.6, h=0.7, c=18):
        processes = [Process(self.no_pages[i], self.start_pages[i], self.end_pages[i], self.localities_of_reference[i],
                             self.how_large_localities[i], self.how_often_localities[i], time_frame, c)
                     for i in range(len(self.no_pages))]

        equal_algorithm = EqualAlgorithm(no_frames)
        proportional_algorithm = ProportionalAlgorithm(no_frames)
        page_fault_frequency = PageFaultFrequency(no_frames, time_frame, l, u, h)
        working_set = WorkingSet(no_frames, time_frame, c)

        for i in range(no_simulations):
            # Generate new pages for every process
            for j in range(len(processes)):
                processes[j].reset_pages()

            print("Simulation number: " + str(i + 1) + "\n")

            print("Equal algorithm (algorithm 1) results")
            print("Overall result: " + str(equal_algorithm.perform_simulation(processes)))
            for j in range(len(processes)):
                print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_one_simulation()))
                # Reseting lru for the next algorithm
                processes[j].reset_lru()

            print("\nProportional algorithm (algorithm 2) results")
            print("Overall result: " + str(proportional_algorithm.perform_simulation(processes)))
            for j in range(len(processes)):
                print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_one_simulation()))
                # Reseting lru for the next algorithm
                processes[j].reset_lru()

            no_page_errors, no_frozen = page_fault_frequency.perform_simulation(processes)
            print("\nPage Fault Frequency (algorithm 3) results")
            print("Overall result: " + str(no_page_errors))
            print("Number of times the processes had to be frozen: " + str(no_frozen))
            for j in range(len(processes)):
                print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_one_simulation()))
            #     # Reseting lru for the next algorithm
                processes[j].reset_lru()

            no_page_errors, no_frozen = working_set.perform_simulation(processes)
            print("\nWorking Set (algorithm 4) results")
            print("Overall result: " + str(no_page_errors))
            print("Number of times the processes had to be frozen: " + str(no_frozen))
            for j in range(len(processes)):
                print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_one_simulation()))
                # Reseting lru for the next algorithm
                processes[j].reset_lru()

            print()

        print("Final results\n")

        print("Equal algorithm (algorithm 1) results")
        print("Overall result: " + str(equal_algorithm.get_results_many_simulations() / no_simulations))
        for j in range(len(processes)):
            print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_many_simulations(1)
                                                                         / no_simulations))

        print("\nProportional algorithm (algorithm 2) results")
        print("Overall result: " + str(proportional_algorithm.get_results_many_simulations() / no_simulations))
        for j in range(len(processes)):
            print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_many_simulations(2)
                                                                         / no_simulations))

        print("\nPage Fault Frequency (algorithm 3) results")
        overall_no_page_errors, overall_no_frozen = page_fault_frequency.get_results_many_simulations()
        print("Overall result: " + str(overall_no_page_errors / no_simulations))
        print("Overall number of times the processes had to be frozen: " + str(overall_no_frozen / no_simulations))
        for j in range(len(processes)):
            print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_many_simulations(3)
                                                                         / no_simulations))

        print("\nWorking Set (algorithm 4) results")
        overall_no_page_errors, overall_no_frozen = working_set.get_results_many_simulations()
        print("Overall result: " + str(overall_no_page_errors / no_simulations))
        print("Overall number of times the processes had to be frozen: " + str(overall_no_frozen / no_simulations))
        for j in range(len(processes)):
            print("Result for process number " + str(j + 1) + ": " + str(processes[j].get_results_many_simulations(4)
                                                                         / no_simulations))
