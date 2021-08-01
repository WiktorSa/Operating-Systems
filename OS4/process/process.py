import sys
from process.pages import Pages
from process.lru import LRU


class Process:
    def __init__(self, no_pages: int, start_page: int, end_page: int, locality_of_reference: list,
                 how_large_locality: int, how_often_locality: int, time_frame: int, c: int):
        self.pages = Pages(no_pages, start_page, end_page, locality_of_reference, how_large_locality,
                           how_often_locality)
        self.lru = LRU(time_frame, c)
        # Possible states - Active, Frozen, Finished
        self.state = "Active"
        # Index of the current page
        self.current_page = 0
        # Number of page errors for this process
        self.no_page_errors = 0
        # Number of this this process got frozen
        self.no_times_frozen = 0

    def use_lru(self):
        page_error = 0
        if self.state == 'Active':
            # For safety reasons
            try:
                page_error = self.lru.forward(self.pages[self.current_page])
            except IndexError:
                self.state = 'Finished'
            self.current_page += 1
            if self.current_page == len(self.pages):
                self.state = 'Finished'

        self.no_page_errors += page_error
        return page_error
