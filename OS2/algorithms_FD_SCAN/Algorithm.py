from abc import ABC, abstractmethod
from disc.Disc import Disc
import numpy as np


class Algorithm(ABC):
    def __init__(self, no_simulations: int):
        self.overall_no_of_seek_operations = 0
        self.overall_no_of_rejected_r_requests = 0
        self.no_simulations = no_simulations

    @abstractmethod
    def perform_simulaton(self, requests: np.array, r_requests: np.array, disc: Disc):
        pass

    def get_results_many_simulations(self):
        return self.overall_no_of_seek_operations / self.no_simulations

    def get_results_many_simulations_rejected(self):
        return self.overall_no_of_rejected_r_requests / self.no_simulations

    # Choose next real time request based on EDF algorithm
    @staticmethod
    def get_argmin_distance_r_requests(wait_r_requests: np.array, disc: Disc):
        min_index = None
        for i in range(len(wait_r_requests)):
            if min_index is None and abs(disc.current_position - wait_r_requests[i].block_position) >= \
                    wait_r_requests[i].deadline_time:
                min_index = i

            elif wait_r_requests[i].deadline_time <= abs(disc.current_position - wait_r_requests[i].block_position) < \
                    abs(disc.current_position - wait_r_requests[min_index].block_position):
                min_index = i

        return min_index
