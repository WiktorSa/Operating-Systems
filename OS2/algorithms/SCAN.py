import numpy as np
from request.Request import Request
from disc.Disc import Disc
from algorithms.Algorithm import Algorithm


class SCAN(Algorithm):
    def __init__(self, no_simulations: int, is_going_right: bool):
        super().__init__(no_simulations)
        if is_going_right:
            self.move = 1
        else:
            self.move = -1

    def perform_simulaton(self, requests: np.array, disc: Disc):
        # How many seek operations we did. This will also work as a time measurement in this task
        no_of_seek_operations = 0
        # All the requests that are waiting for execution
        waiting_requests = []
        # The index of the first request in requests that is not in requests waiting line
        no_request_wait_arrival = 0
        # We will display the last 10 requests to finish to show some of the algorithms weaknesses
        finished_requests = np.empty(len(requests), dtype=Request)
        no_finished_request = 0
        # In which direction to move
        move = self.move

        while no_finished_request < len(finished_requests):
            # Add requests that have arrived to the queue of requests
            while no_request_wait_arrival != len(requests) and \
                    requests[no_request_wait_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_wait_arrival])
                no_request_wait_arrival += 1

            # Move the disc in the proper direction
            disc.current_position += move

            # The disk has moved once
            no_of_seek_operations += 1

            for request in waiting_requests:
                request.waiting_time += 1
                if disc.current_position == request.block_position:
                    finished_requests[no_finished_request] = request
                    no_finished_request += 1
                    waiting_requests.remove(request)

            if disc.current_position == 0:
                move = 1

            if disc.current_position == disc.size_of_disc:
                move = -1

        print("SCAN last 15 finished requests")
        for i in range(1, 16):
            print(finished_requests[-i])

        print("Longest waiting request: ", np.sort(finished_requests)[-1])
        print("Average waiting time: ", sum(r.waiting_time for r in finished_requests) / len(finished_requests))
        print()

        self.overall_no_of_seek_operations += no_of_seek_operations
