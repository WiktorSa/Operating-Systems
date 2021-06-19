import collections
from abc import abstractmethod, ABC


class Algorithm(ABC):
    def __init__(self, no_simulations: int):
        self.overall_waiting_time = 0
        self.no_simulations = no_simulations

    @abstractmethod
    def perform_simulation(self, processes: collections.deque):
        pass

    def get_results_all_simulations(self):
        return self.overall_waiting_time / self.no_simulations
