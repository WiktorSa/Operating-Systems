import random
import numpy as np


class Pages:
    def __init__(self, no_pages: int, start_page: int, end_page: int, locality_of_reference: list,
                 how_large_locality: int, how_often_locality: int):
        self.pages = np.empty(shape=no_pages)
        self.no_pages = no_pages
        self.start_page = start_page
        self.end_page = end_page
        self.locality_of_reference = locality_of_reference
        self.how_large_locality = how_large_locality
        self.how_often_locality = how_often_locality

    def generate_new_pages(self):
        how_often_locality = self.how_often_locality
        j = 0
        time_locality = 0
        while j < self.no_pages:
            # Adding the locality
            if time_locality % how_often_locality == 0 and 100 < j + 100 < self.no_pages:
                # Changing the size of the locality so that it may be shorter or longer
                for _ in range(self.how_large_locality + random.randint(-10, 10)):
                    self.pages[j] = self.locality_of_reference[random.randint(0, len(self.locality_of_reference) - 1)]
                    j += 1
                    time_locality += 1

                # Chaning how often_locality
                how_often_locality += random.randint(-10, 10)
                if how_often_locality < 20 or how_often_locality > 100:
                    how_often_locality = 50

            else:
                time_locality += 1
                self.pages[j] = random.randint(self.start_page, self.end_page)
                j += 1

    def __getitem__(self, index: int):
        return self.pages[index]

    def __len__(self):
        return len(self.pages)
