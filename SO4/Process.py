import sys

from Pages import Pages
from LRU import LRU


class Process:
    def __init__(self, no_pages, start_page, end_page, locality_of_reference, how_large_locality, how_often_locality,
                 time_frame, c):
        self.pages = Pages(no_pages, start_page, end_page, locality_of_reference, how_large_locality,
                           how_often_locality)
        self.lru = LRU(time_frame, c)
        # Possible states - Active, Frozen, Finished
        self.state = "Active"
        # Index of the current page
        self.current_page = 0

        # Overall number of page errors in all simulations
        self.overall_no_page_errors_algorithm_1 = 0
        self.overall_no_page_errors_algorithm_2 = 0
        self.overall_no_page_errors_algorithm_3 = 0
        self.overall_no_page_errors_algorithm_4 = 0

    def forward(self, no_algorithm):
        page_error = 0
        if self.state == 'Active':
            # For safety reasons
            try:
                page_error = self.lru.forward(self.pages[self.current_page], no_algorithm)
            except IndexError:
                self.state = 'Finished'
            self.current_page += 1
            if self.current_page == len(self.pages):
                self.state = 'Finished'

        if no_algorithm == 1:
            self.overall_no_page_errors_algorithm_1 += page_error
        elif no_algorithm == 2:
            self.overall_no_page_errors_algorithm_2 += page_error
        elif no_algorithm == 3:
            self.overall_no_page_errors_algorithm_3 += page_error
        else:
            self.overall_no_page_errors_algorithm_4 += page_error

        return page_error

    def reset_pages(self):
        self.pages.generate_new_pages()

    def reset_lru(self):
        self.lru.reset()
        self.current_page = 0
        self.state = 'Active'

    def get_results_one_simulation(self):
        return self.lru.overall_no_page_errors_algorithm

    def get_results_many_simulations(self, no_algorithm):
        if no_algorithm == 1:
            return self.overall_no_page_errors_algorithm_1
        elif no_algorithm == 2:
            return self.overall_no_page_errors_algorithm_2
        elif no_algorithm == 3:
            return self.overall_no_page_errors_algorithm_3
        else:
            return self.overall_no_page_errors_algorithm_4
