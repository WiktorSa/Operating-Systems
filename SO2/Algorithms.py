# First Come First Served
# This works
def FCFS(requests, disc):
    # Sorting by arrival time
    requests.sort(key=lambda x: x.arrival_time)

    # Our current request
    current_request = requests[0]
    # How many seek operations we did. This will also work as a time measurement in this task
    no_of_seek_operations = 0
    # ALl the requests that are waiting for execution
    waiting_requests = []
    # The index of the first request in requests that is not in requests waiting line
    no_request_waiting_for_arrival = 1
    # We will display the last 10 requests to finish to show some of the algorithms weaknesses
    finished_requests = []

    while True:
        # Here we add requests that have arrived to the queue of requests
        if no_request_waiting_for_arrival != len(requests):
            while requests[no_request_waiting_for_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_waiting_for_arrival])
                no_request_waiting_for_arrival += 1

                # If there are no more requests that will arrive we break from this loop
                if no_request_waiting_for_arrival == len(requests):
                    break

        # We can assume that there is always at least one request being processed
        # The disc current position is on the right to the current request position
        if disc.current_position - current_request.block_position > 0:
            disc.current_position -= 1

        # The disc current position is on the left to the current request position
        else:
            disc.current_position += 1

        # The disk has moved once
        no_of_seek_operations += 1

        # Increase waiting time for the request
        current_request.waiting_time += 1

        # The request has been finished
        if disc.current_position == current_request.block_position:
            finished_requests.append(current_request)

            # We finished all requests
            if len(finished_requests) == len(requests):
                break
            else:
                current_request = waiting_requests.pop(0)

        # Increasing waiting time for all waiting_requests
        for request in waiting_requests:
            request.waiting_time += 1

    # Here we display last 15 requests that have been finished
    # (Note to yourself - for testing purposes we only show the last 5 requests
    print("FCFS last 15 finished requests")
    for request in list(reversed(finished_requests))[:15]:
        print(request)
    finished_requests.sort(key=lambda x: x.waiting_time)
    print("Longest waiting request: {longest_request}".format(longest_request=finished_requests[-1]))
    average = sum(r.waiting_time for r in finished_requests) / len(finished_requests)
    print("Average waiting time: {wait_time}\n".format(wait_time=average))

    return no_of_seek_operations


# Shortest Seek Time First
# This works
def SSTF(requests, disc):
    # Sorting by arrival time and by how
    requests.sort(key=lambda x: (x.arrival_time, abs(disc.current_position - x.block_position)))

    # Our current request
    current_request = requests[0]
    # How many seek operations we did. This will also work as a time measurement in this task
    no_of_seek_operations = 0
    # ALl the requests that are waiting for execution
    waiting_requests = []
    # The index of the first request in requests that is not in requests waiting line
    no_request_waiting_for_arrival = 1
    # We will display the last 10 requests to finish to show some of the algorithms weaknesses
    finished_requests = []

    while True:
        # Here we add requests that have arrived to the queue of requests
        if no_request_waiting_for_arrival != len(requests):
            while requests[no_request_waiting_for_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_waiting_for_arrival])
                no_request_waiting_for_arrival += 1

                # If there are no more requests that will arrive we break from this loop
                if no_request_waiting_for_arrival == len(requests):
                    break

        # We can assume that there is always at least one request being processed
        # The disc current position is on the right to the current request position
        if disc.current_position - current_request.block_position > 0:
            disc.current_position -= 1

        # The disc current position is on the left to the current request position
        else:
            disc.current_position += 1

        # The disk has moved once
        no_of_seek_operations += 1

        # Increase waiting time for the request
        current_request.waiting_time += 1

        # The request has been finished
        if disc.current_position == current_request.block_position:
            finished_requests.append(current_request)

            # We finished all requests
            if len(finished_requests) == len(requests):
                break
            else:
                # Finding the next request that is the closest to the disc current position
                waiting_requests.sort(key=lambda x: abs(disc.current_position - x.block_position))
                current_request = waiting_requests.pop(0)

        # Increasing waiting time for all waiting_requests
        for request in waiting_requests:
            request.waiting_time += 1

    # Here we display last 15 requests that have been finished
    # (Note to yourself - for testing purposes we only show the last 5 requests
    print("SSTF last 15 finished requests")
    for request in list(reversed(finished_requests))[:15]:
        print(request)
    finished_requests.sort(key=lambda x: x.waiting_time)
    print("Longest waiting request: {longest_request}".format(longest_request=finished_requests[-1]))
    average = sum(r.waiting_time for r in finished_requests) / len(finished_requests)
    print("Average waiting time: {wait_time}\n".format(wait_time=average))

    return no_of_seek_operations


# SCAN
# This works
def SCAN(requests, disc, is_going_left):
    # Sorting by arrival time and by how
    requests.sort(key=lambda x: x.arrival_time)

    # How many seek operations we did. This will also work as a time measurement in this task
    no_of_seek_operations = 0
    # ALl the requests that are waiting for execution
    waiting_requests = []
    # The index of the first request in requests that is not in requests waiting line
    no_request_waiting_for_arrival = 0
    # We will display the last 10 requests to finish to show some of the algorithms weaknesses
    finished_requests = []

    while True:
        # Here we add requests that have arrived to the queue of requests
        if no_request_waiting_for_arrival != len(requests):
            while requests[no_request_waiting_for_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_waiting_for_arrival])
                no_request_waiting_for_arrival += 1

                # If there are no more requests that will arrive we break from this loop
                if no_request_waiting_for_arrival == len(requests):
                    break

        # We can assume that there is always at least one request being processed
        # The disc moves to the left
        if is_going_left:
            disc.current_position -= 1

        # The disc moves to the right
        else:
            disc.current_position += 1

        # The disk has moved once
        no_of_seek_operations += 1

        # Searching for all requests that will be done when the disc is on the given position
        for request in waiting_requests:
            if disc.current_position == request.block_position:
                finished_requests.append(request)
                waiting_requests.remove(request)

        if disc.current_position == 0:
            is_going_left = False

        if disc.current_position == disc.size_of_disc:
            is_going_left = True

        # We finished all requests
        if len(finished_requests) == len(requests):
            break

        # Increasing waiting time for all waiting_requests
        for request in waiting_requests:
            request.waiting_time += 1

    # Here we display last 15 requests that have been finished
    # (Note to yourself - for testing purposes we only show the last 5 requests
    print("SCAN last 15 finished requests")
    for request in list(reversed(finished_requests))[:15]:
        print(request)
    finished_requests.sort(key=lambda x: x.waiting_time)
    print("Longest waiting request: {longest_request}".format(longest_request=finished_requests[-1]))
    average = sum(r.waiting_time for r in finished_requests) / len(finished_requests)
    print("Average waiting time: {wait_time}\n".format(wait_time=average))

    return no_of_seek_operations


# C-SCAN
# This works
def CSCAN(requests, disc, is_going_left):
    # Sorting by arrival time and by how
    requests.sort(key=lambda x: x.arrival_time)

    # How many seek operations we did. This will also work as a time measurement in this task
    no_of_seek_operations = 0
    # ALl the requests that are waiting for execution
    waiting_requests = []
    # The index of the first request in requests that is not in requests waiting line
    no_request_waiting_for_arrival = 0
    # We will display the last 10 requests to finish to show some of the algorithms weaknesses
    finished_requests = []

    while True:
        # Here we add requests that have arrived to the queue of requests
        if no_request_waiting_for_arrival != len(requests):
            while requests[no_request_waiting_for_arrival].arrival_time == no_of_seek_operations:
                waiting_requests.append(requests[no_request_waiting_for_arrival])
                no_request_waiting_for_arrival += 1

                # If there are no more requests that will arrive we break from this loop
                if no_request_waiting_for_arrival == len(requests):
                    break

        # We can assume that there is always at least one request being processed
        # The disc moves to the left
        if is_going_left:
            disc.current_position -= 1

        # The disc moves to the right
        else:
            disc.current_position += 1

        # The disk has moved once
        no_of_seek_operations += 1

        # Searching for all requests that will be done when the disc is on the given position
        for request in waiting_requests:
            if disc.current_position == request.block_position:
                finished_requests.append(request)
                waiting_requests.remove(request)

        # Moving to the other side of the disc. We need to be careful here with the no_of_seek_operations
        if disc.current_position == 0 and is_going_left:
            disc.current_position = disc.size_of_disc
            # Searching for all requests that will be done when the disc is on the given position
            for request in waiting_requests:
                if disc.current_position == request.block_position:
                    finished_requests.append(request)
                    waiting_requests.remove(request)

        if disc.current_position == disc.size_of_disc and not is_going_left:
            disc.current_position = 0
            # Searching for all requests that will be done when the disc is on the given position
            for request in waiting_requests:
                if disc.current_position == request.block_position:
                    finished_requests.append(request)
                    waiting_requests.remove(request)

        # We finished all requests
        if len(finished_requests) == len(requests):
            break

        # Increasing waiting time for all waiting_requests
        for request in waiting_requests:
            request.waiting_time += 1

    # Here we display last 15 requests that have been finished
    # (Note to yourself - for testing purposes we only show the last 5 requests
    print("C-SCAN last 15 finished requests")
    for request in list(reversed(finished_requests))[:15]:
        print(request)
    finished_requests.sort(key=lambda x: x.waiting_time)
    print("Longest waiting request: {longest_request}".format(longest_request=finished_requests[-1]))
    average = sum(r.waiting_time for r in finished_requests) / len(finished_requests)
    print("Average waiting time: {wait_time}\n".format(wait_time=average))

    return no_of_seek_operations
