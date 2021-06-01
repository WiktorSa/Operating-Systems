import queue

from Processor import Processor
from Simulation import perform_simulation

if __name__ == '__main__':
    # Parameter N, p and r
    no_processors = 65
    maximal_load_to_accept = 60
    minimal_load_to_accept = 30
    processors = [Processor(i, maximal_load_to_accept, minimal_load_to_accept) for i in range(no_processors)]

    no_simulations = 20
    no_processes = 50000
    # z in algorithm 1
    max_searches_alg1 = 50
    # How many times we will search for proper processor until we do a brute force search
    max_searches_alg2 = 20
    # How many times will the processor with low loads ask other processors
    max_searches_alg3 = 10
    # Should processes be generated equally or not
    uneven_processes = False

    perform_simulation(no_simulations, processors, no_processes, max_searches_alg1, max_searches_alg2,
                       max_searches_alg3, uneven_processes)
