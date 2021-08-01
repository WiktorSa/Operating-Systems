import math
from algorithms.algorithm import Algorithm


class EqualAlgorithm(Algorithm):
    def perform_simulation(self, processes: list):
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
                    no_page_errors += processes[i].use_lru()

                    # The process has finished
                    if processes[i].state == 'Finished':
                        no_finished_processes += 1

        print("Equal algorithm - number of page errors: ", no_page_errors)
        print("Number of page errors for every process: ")
        for i in range(len(processes)):
            print("Process number: {no} - {no_page_errors}".format(no=i+1, no_page_errors=processes[i].no_page_errors))
            self.no_page_errors_process[i] += processes[i].no_page_errors

        self.overall_no_page_errors += no_page_errors

    # This algorithm will divide frames for every process equally
    def divide_frames_at_start(self, processes: list):
        # Distributing frames for every process
        average_no_frames_per_process = math.floor(self.no_frames / len(processes))
        no_frames_per_process = [average_no_frames_per_process] * len(processes)

        # Assigning leftover frames
        left_frames = self.no_frames - average_no_frames_per_process * len(processes)
        for i in range(left_frames):
            no_frames_per_process[i] += 1

        return no_frames_per_process
