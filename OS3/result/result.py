import copy
import random
import numpy as np
import algorithms


def result(no_simulations=50, no_pages=2000, no_frames=40, no_unique_pages=50, locality_of_reference=None,
           how_large_locality=20, how_often_locality=50):
    if locality_of_reference is None:
        locality_of_reference = [2, 4, 9, 12, 25]

    fifo = algorithms.FIFO()
    opt = algorithms.OPT()
    lru = algorithms.LRU()
    lru_app = algorithms.LRUApp()
    rand = algorithms.RAND()

    for i in range(no_simulations):
        pages = np.empty(shape=no_pages, dtype=np.int32)

        j = 0
        time_locality = 0
        while j < no_pages:
            # Adding the locality
            if time_locality % how_often_locality == 0 and 100 < j + 100 < no_pages:
                # Changing the size of the locality so that it may be shorter or longer
                for _ in range(how_large_locality + random.randint(-10, 10)):
                    pages[j] = locality_of_reference[random.randint(0, len(locality_of_reference) - 1)]
                    j += 1
                    time_locality += 1

                # Chaning how often_locality
                how_often_locality += random.randint(-10, 10)
                if how_often_locality < 20 or how_often_locality > 100:
                    how_often_locality = 50

            else:
                time_locality += 1
                pages[j] = random.randint(1, no_unique_pages)
                j += 1

        print("Simulation number: " + str(i + 1))
        fifo.perform_simulation(no_frames, copy.deepcopy(pages))
        opt.perform_simulation(no_frames, copy.deepcopy(pages))
        lru.perform_simulation(no_frames, copy.deepcopy(pages))
        lru_app.perform_simulation(no_frames, copy.deepcopy(pages))
        rand.perform_simulation(no_frames, copy.deepcopy(pages))
        print()

    print('Final results:')
    print("FIFO:")
    print(fifo.get_results())
    print(fifo.get_page_that_caused_most_errors())
    print("OPT:")
    print(opt.get_results())
    print(opt.get_page_that_caused_most_errors())
    print("LRU:")
    print(lru.get_results())
    print(lru.get_page_that_caused_most_errors())
    print("LRU Approximation:")
    print(lru_app.get_results())
    print(lru_app.get_page_that_caused_most_errors())
    print("RAND:")
    print(rand.get_results())
    print(rand.get_page_that_caused_most_errors())
