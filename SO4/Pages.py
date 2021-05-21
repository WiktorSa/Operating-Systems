"""
no_pages - how many pages will this process have
start_page, end_page - from which page to which we will generate new pages
(we need to do this to mantain that no page will appear twice in different processes
locality_of_reference - which pages will appear more than often
how_large_locality - how many pages from locality_of_reference will appear, this value will vary
when pages are added
how_often_locality - how often will pages from locality_of_reference appear. This
"""
import random


class Pages:
    def __init__(self, no_pages, start_page, end_page, locality_of_reference, how_large_locality, how_often_locality):
        self.no_pages = no_pages
        self.start_page = start_page
        self.end_page = end_page
        self.locality_of_reference = locality_of_reference
        if self.locality_of_reference is None:
            self.locality_of_reference = []
            for i in range(5):
                random_page = random.randint(start_page, end_page)
                while random_page in self.locality_of_reference:
                    random_page = random.randint(start_page, end_page)
                self.locality_of_reference.append(random_page)
        self.how_large_locality = how_large_locality
        self.how_often_locality = how_often_locality
        self.pages = []

    def generate_new_pages(self):
        self.pages.clear()
        how_often_locality = self.how_often_locality
        time_locality = 0
        time = 0
        while time < self.no_pages:
            # Adding the locality
            if time_locality % self.how_often_locality == 0 and time_locality != 0 and time + 100 < self.no_pages:
                time_locality = 0
                # Changing the size of the locality so that it may be shorter or longer
                for i in range(self.how_large_locality + random.randint(-10, 10)):
                    self.pages.append(self.locality_of_reference[random.randint(0,
                                                len(self.locality_of_reference) - 1)])
                    time_locality += 1
                    time += 1

                # Chaning how often_locality
                how_often_locality += random.randint(-10, 10)
                if how_often_locality < 20 or how_often_locality > 100:
                    how_often_locality = self.how_often_locality

            self.pages.append(random.randint(self.start_page, self.end_page))
            time_locality += 1
            time += 1

    def __getitem__(self, index):
        return self.pages[index]

    def __len__(self):
        return len(self.pages)
