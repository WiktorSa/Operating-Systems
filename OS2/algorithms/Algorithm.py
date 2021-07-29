from abc import ABC, abstractmethod
from disc.Disc import Disc
import numpy as np


class Algorithm(ABC):
    def __init__(self, no_simulations: int):
        self.overall_no_of_seek_operations = 0
        self.no_simulations = no_simulations

    @abstractmethod
    def perform_simulaton(self, requests: np.array, disc: Disc):
        pass

    def get_results_many_simulations(self):
        return self.overall_no_of_seek_operations / self.no_simulations
