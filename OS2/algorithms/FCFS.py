import numpy as np
from request.Request import Request
from disc.Disc import Disc
from algorithms.Algorithm import Algorithm


# First Come First Served
class FCFS(Algorithm):
    def __init__(self, no_simulations: int):
        super().__init__(no_simulations)

    def perform_simulaton(self, requests: np.array, disc: Disc):
        # Our current request
        current_request = requests[0]
        # How many seek operations we did. This will also work as a time measurement in this task
        no_of_seek_operations = 0
        # All the requests that are waiting for execution
        waiting_requests = []
        # The index of the first request in requests that is not in requests waiting line
        no_request_wait_arrival = 1
        # We will display the last 10 requests to finish to show some of the algorithms weaknesses
        finished_requests = np.empty(len(requests), dtype=Request)
        no_finished_request = 0

        while no_finished_request < len(finished_requests):
            # Add requests that have arrived to the queue of requests
            while no_request_wait_arrival != len(requests) and \
                    requests[no_request_wait_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_wait_arrival])
                no_request_wait_arrival += 1

            # Move the disc in the proper direction
            disc.current_position += np.sign(current_request.block_position - disc.current_position)

            # The disk has moved once
            no_of_seek_operations += 1

            # Increase waiting time for the request
            current_request.waiting_time += 1

            # Increasing waiting time for all waiting_requests
            for request in waiting_requests:
                request.waiting_time += 1

            # The request has been finished
            if disc.current_position == current_request.block_position:
                finished_requests[no_finished_request] = current_request
                no_finished_request += 1

                if len(waiting_requests) != 0:
                    current_request = waiting_requests.pop(0)

        print("FCFS last 15 finished requests")
        for i in range(1, 16):
            print(finished_requests[-i])

        print("Longest waiting request: ", np.sort(finished_requests)[-1])
        print("Average waiting time: ", sum(r.waiting_time for r in finished_requests) / len(finished_requests))
        print()

        self.overall_no_of_seek_operations += no_of_seek_operations
