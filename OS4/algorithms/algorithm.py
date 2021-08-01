from abc import ABC, abstractmethod
import math


# is_3_or_4 - is it algorithm 3 or 4 where processes can be frozen
class Algorithm(ABC):
    def __init__(self, no_frames: int, no_processes: int, no_simulations: int, is_3_or_4: bool):
        self.no_frames = no_frames
        self.no_simulations = no_simulations
        # Number of page errors in all simulations
        self.overall_no_page_errors = 0
        # Number of page errors for every process
        self.no_page_errors_process = [0] * no_processes
        # How many times the given process got frozen
        self.overall_no_times_process_frozen = 0
        self.no_process_frozen = [0] * no_processes
        self.is_3_or_4 = is_3_or_4

    @abstractmethod
    def perform_simulation(self, processes: list):
        pass

    # Proportional algorithm
    def divide_frames_at_start(self, processes: list):
        no_of_frames_per_process = [0] * len(processes)
        overall_no_processes = 0
        # Calculating the average number of frames needed for one page
        for i in range(len(processes)):
            overall_no_processes += len(processes[i].pages)
        no_frames_for_every_page = self.no_frames / overall_no_processes

        # Assigning frames to the processes (rounded down)
        used_frames = 0
        for i in range(len(processes)):
            no_frames = math.ceil(no_frames_for_every_page * len(processes[i].pages))
            no_of_frames_per_process[i] = no_frames
            used_frames += no_frames

        # Assigning leftover frames
        left_frames = self.no_frames - used_frames
        for i in range(left_frames):
            no_of_frames_per_process[i] += 1

        return no_of_frames_per_process

    # Divide the leftover frames after the process is finished
    # noinspection PyMethodMayBeStatic
    def divide_frames(self, no_leftover_frames, processes):
        no_of_frames_per_process = []
        overall_no_processes = 0
        # Calculating the average number of frames needed for one page (pages that were left)
        for i in range(len(processes)):
            if processes[i].state == 'Active':
                overall_no_processes = overall_no_processes + len(processes[i].pages) - processes[i].current_page

        # Very rare condition but sometimes overall_no_processes may be equal to 0
        if overall_no_processes == 0:
            return [0] * len(processes)
        no_frames_for_every_page = no_leftover_frames / overall_no_processes

        # Assigning frames to the processes (rounded down)
        used_frames = 0
        for i in range(len(processes)):
            if processes[i].state == 'Active':
                no_frames = math.ceil(
                    no_frames_for_every_page * (len(processes[i].pages) - processes[i].current_page))
                no_of_frames_per_process.append(no_frames)
                used_frames += no_frames

        # Assigning leftover frames
        left_frames = no_leftover_frames - used_frames
        for i in range(left_frames):
            if processes[i].state == 'Active':
                no_of_frames_per_process[i] += 1

        return no_of_frames_per_process

    def print_results(self):
        print("Average number of page errors: ", self.overall_no_page_errors / self.no_simulations)
        if self.is_3_or_4:
            print("Average number of times the processes got frozen: ",
                  self.overall_no_times_process_frozen / self.no_simulations)
            print("Average number of page errors/times frozen for everry process: ")
            for i in range(len(self.no_page_errors_process)):
                print("Process number: {no} - {no_page_errors} / {times_frozen}".format(
                    no=i + 1, no_page_errors=self.no_page_errors_process[i] / self.no_simulations,
                    times_frozen=self.no_process_frozen[i] / self.no_simulations))

        else:
            print("Average number of page errors for every process: ")
            for i in range(len(self.no_page_errors_process)):
                print("Process number: {no} - {no_page_errors}".format(no=i + 1,
                                        no_page_errors=self.no_page_errors_process[i] / self.no_simulations))
