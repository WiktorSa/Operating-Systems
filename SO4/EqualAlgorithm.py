#  Algorithm number 1
import math


# This works
class EqualAlgorithm:
    def __init__(self, no_frames):
        self.no_frames = no_frames
        # Number of page errors in all simulations
        self.overall_no_page_errors = 0

    # This algorithm will divide frames for every process equally
    def divide_frames_at_start(self, processes):
        # Distributing frames for every process
        average_no_frames_per_process = math.floor(self.no_frames / len(processes))
        no_frames_per_process = [average_no_frames_per_process] * len(processes)

        # Assigning leftover frames
        left_frames = self.no_frames - average_no_frames_per_process * len(processes)
        for i in range(left_frames):
            no_frames_per_process[i] += 1

        return no_frames_per_process

    def perform_simulation(self, processes):
        original_no_of_frames = self.divide_frames_at_start(processes)
        for i in range(len(processes)):
            processes[i].lru.set_original_number_of_frames(original_no_of_frames[i])

        no_page_errors = 0
        # Perform simulation until all processes are finished
        no_finished_processes = 0
        while no_finished_processes < len(processes):
            # Doing one iteration of lru algorithm for every process
            for i in range(len(processes)):
                if processes[i].state == 'Active':
                    no_page_errors += processes[i].forward(1)

                    # The process has finished
                    if processes[i].state == 'Finished':
                        no_finished_processes += 1

        self.overall_no_page_errors += no_page_errors
        return no_page_errors

    def get_results_many_simulations(self):
        return self.overall_no_page_errors
