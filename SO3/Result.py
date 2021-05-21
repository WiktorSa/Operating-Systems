import copy
import random
from FIFO import FIFO
from OPT import OPT
from LRU import LRU
from LRUApp import LRUApp
from RAND import RAND


def result(no_simulations=50, no_pages=2000, no_frames=40, no_unique_pages=50, locality_of_reference=None,
           how_large_locality=20, how_often_locality=50):
    if locality_of_reference is None:
        locality_of_reference = [2, 4, 9, 12, 25]

    fifo = FIFO()
    opt = OPT()
    lru = LRU()
    lru_app = LRUApp()
    rand = RAND()

    for i in range(no_simulations):
        pages = []

        time_locality = 0
        j = 0
        while j < no_pages:
            # Adding the locality
            if time_locality % how_often_locality == 0 and time_locality != 0 and j + 100 < no_pages:
                time_locality = 0
                # Changing the size of the locality so that it may be shorter or longer
                for k in range(how_large_locality + random.randint(-10, 10)):
                    pages.append(locality_of_reference[random.randint(0, len(locality_of_reference) - 1)])
                    j += 1
                    time_locality += 1

                # Chaning how often_locality
                how_often_locality += random.randint(-10, 10)
                if how_often_locality < 20 or how_often_locality > 100:
                    how_often_locality = 50

            time_locality += 1
            pages.append(random.randint(1, no_unique_pages))
            j += 1

        print("Simulation number: " + str(i + 1))
        print(fifo.fifo(no_frames, copy.deepcopy(pages)))
        print(opt.opt(no_frames, copy.deepcopy(pages)))
        print(lru.lru(no_frames, copy.deepcopy(pages)))
        print(lru_app.lru_app(no_frames, copy.deepcopy(pages)))
        print(rand.rand(no_frames, copy.deepcopy(pages)) + "\n")

    print('Final results:')
    print(fifo.get_results())
    print(fifo.get_page_that_caused_most_errors())
    print(opt.get_results())
    print(opt.get_page_that_caused_most_errors())
    print(lru.get_results())
    print(lru.get_page_that_caused_most_errors())
    print(lru_app.get_results())
    print(lru_app.get_page_that_caused_most_errors())
    print(rand.get_results())
    print(rand.get_page_that_caused_most_errors())
