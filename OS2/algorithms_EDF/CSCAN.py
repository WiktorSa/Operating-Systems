import numpy as np
from request.Request import Request
from disc.Disc import Disc
from algorithms_EDF.Algorithm import Algorithm


class CSCAN(Algorithm):
    def __init__(self, no_simulations: int, is_going_right: bool):
        super().__init__(no_simulations)
        # In which direction to move
        if is_going_right:
            self.move = 1
        else:
            self.move = -1

    def perform_simulaton(self, requests: np.array, r_requests: np.array, disc: Disc):
        # Number of reject real time requests
        no_of_rejected_r_requests = 0
        # Fake request (made so EDF works)
        current_request = None
        # How many seek operations we did. This will also work as a time measurement in this task
        no_of_seek_operations = 0
        # All the requests that are waiting for execution
        waiting_requests = []
        waiting_r_requests = []
        # The index of the first request in requests that is not in requests waiting line
        no_request_wait_arrival = 0
        no_r_request_wait_arrival = 0
        # We will display the last 10 requests to finish to show some of the algorithms weaknesses
        finished_requests = np.empty(len(requests) + len(r_requests), dtype=Request)
        no_finished_request = 0

        while no_finished_request < len(finished_requests):
            # Add requests that have arrived to the queue of requests
            while no_request_wait_arrival != len(requests) and \
                    requests[no_request_wait_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_wait_arrival])
                no_request_wait_arrival += 1

            # Adding real_time_requests
            while no_r_request_wait_arrival != len(r_requests) and \
                    r_requests[no_r_request_wait_arrival].arrival_time == no_of_seek_operations:
                waiting_r_requests.append(r_requests[no_r_request_wait_arrival])
                no_r_request_wait_arrival += 1

            # Processing the real time requests (EDF algorithm)
            if len(waiting_r_requests) > 0 and current_request is None:
                current_request = waiting_r_requests.pop(0)

            # Move the disc in the proper direction
            if current_request is not None:
                disc.current_position += np.sign(current_request.block_position - disc.current_position)

            else:
                disc.current_position += self.move

            # The disk has moved once
            no_of_seek_operations += 1

            # Increasing waiting time for all waiting_requests
            for request in waiting_requests:
                request.waiting_time += 1

            for r_request in waiting_r_requests:
                r_request.waiting_time += 1
                # If deadline time has passed we just get rid of this process
                if r_request.waiting_time > r_request.deadline_time:
                    no_of_rejected_r_requests += 1
                    finished_requests[no_finished_request] = r_request
                    no_finished_request += 1
                    waiting_r_requests.remove(r_request)

            if current_request is not None:
                # Real time request is finished or ran out of time
                if disc.current_position == current_request.block_position or \
                        current_request.waiting_time > current_request.deadline_time:
                    if current_request.waiting_time > current_request.deadline_time:
                        no_of_rejected_r_requests += 1

                    finished_requests[no_finished_request] = current_request
                    no_finished_request += 1

                    if len(waiting_r_requests) != 0:
                        current_request = waiting_r_requests.pop(
                            self.get_argmin_distance_r_requests(waiting_r_requests, disc))

                    else:
                        current_request = None

            else:
                # Searching for all requests that will be done when the disc is on the given position
                for request in waiting_requests:
                    if disc.current_position == request.block_position:
                        finished_requests[no_finished_request] = request
                        no_finished_request += 1
                        waiting_requests.remove(request)

                # Move disc to the opposite side
                if disc.current_position == 0:
                    disc.current_position = disc.size_of_disc

                if disc.current_position == disc.size_of_disc:
                    disc.current_position = 0

                for request in waiting_requests:
                    if disc.current_position == request.block_position:
                        finished_requests[no_finished_request] = request
                        no_finished_request += 1
                        waiting_requests.remove(request)

        print("CSCAN-EDF last 15 finished requests")
        for i in range(1, 16):
            print(finished_requests[-i])

        print("Longest waiting request: ", np.sort(finished_requests)[-1])
        print("Average waiting time: ", sum(r.waiting_time for r in finished_requests) / len(finished_requests))
        print("Number of rejected requests: ", no_of_rejected_r_requests)
        print()

        self.overall_no_of_seek_operations += no_of_seek_operations
        self.overall_no_of_rejected_r_requests += no_of_rejected_r_requests
