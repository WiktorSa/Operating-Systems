# First Come First Served
# This works correctly
def FCFS(processes):
    # Sorting by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    overall_waiting_time = 0

    current_process = processes[0]
    waiting_processses = []
    no_process_waiting_for_arrival = 1

    # The max length is 10000 so that we could analyse any process that were left over
    # We are starting from the first process arrival time because we can't be sure if this time will be equal to 0
    for i in range(current_process.arrival_time, 10000):
        # Here we add processes that have arrived to the queue of processes
        if no_process_waiting_for_arrival != len(processes):
            while processes[no_process_waiting_for_arrival].arrival_time == i:
                waiting_processses.append(processes[no_process_waiting_for_arrival])
                no_process_waiting_for_arrival += 1

                # If there are no more processes that will arrive we break from this loop
                if no_process_waiting_for_arrival == len(processes):
                    break

        # Swaping the finished process with a new one
        if len(waiting_processses) != 0 and current_process.burst_time <= 0:
            current_process = waiting_processses[0]
            waiting_processses.pop(0)

        current_process.burst_time -= 1
        overall_waiting_time += len(waiting_processses)
        # Increasing waiting time for all waiting_processes
        # (useful if we want to analyse waiting time for individual processes)
        for j in range(0, len(waiting_processses)):
            waiting_processses[j].waiting_time += 1

    if len(waiting_processses) != 0:
        print("FCFS processes still left")
        for process in waiting_processses:
            print(process)
        print()

        waiting_processses.sort(key=lambda x: x.waiting_time, reverse=True)
        print("Longest waiting process that is still waiting for execution")
        print(waiting_processses[0])
        print()

    else:
        print("No processes left for FCFS")

    return overall_waiting_time / len(processes)


# Non-preemptive SJF (Shorest Job First) (bez wywlaszczania)
# This works correctly
def SJF(processes):
    # Sorting by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    overall_waiting_time = 0

    current_process = processes[0]
    waiting_processses = []
    no_process_waiting_for_arrival = 1

    # The max length is 10000 so that we could analyse any process that were left over
    for i in range(current_process.arrival_time, 10000):
        # Here we add processes that have arrived to the queue of processes
        if no_process_waiting_for_arrival != len(processes):
            while processes[no_process_waiting_for_arrival].arrival_time == i:
                waiting_processses.append(processes[no_process_waiting_for_arrival])
                no_process_waiting_for_arrival += 1

                # If there are no more processes that will arrive we break from this loop
                if no_process_waiting_for_arrival == len(processes):
                    break

        # Swaping the finished process with a new one
        if len(waiting_processses) != 0 and current_process.burst_time <= 0:
            # Sorting by the burst time
            waiting_processses.sort(key=lambda x: x.burst_time)
            current_process = waiting_processses[0]
            waiting_processses.pop(0)

        current_process.burst_time -= 1
        overall_waiting_time += len(waiting_processses)
        # Increasing waiting time for all waiting_processes
        # (useful if we want to analyse waiting time for individual processes)
        for j in range(0, len(waiting_processses)):
            waiting_processses[j].waiting_time += 1

    if len(waiting_processses) != 0:
        print("SJF processes still left")
        for process in waiting_processses:
            print(process)
        print()

        waiting_processses.sort(key=lambda x: x.waiting_time, reverse=True)
        print("Longest waiting process that is still waiting for execution")
        print(waiting_processses[0])
        print()

    else:
        print("No processes left for FCFS")

    return overall_waiting_time / len(processes)


# Round Robin (planowanie priorytetowe)
# This works correctly
def RR(processes, quant):
    # Sorting by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    overall_waiting_time = 0

    current_process = processes[0]
    waiting_processses = []
    no_process_waiting_for_arrival = 1
    current_quant = 0

    # The max length is 10000 so that we could analyse any process that were left over
    for i in range(current_process.arrival_time, 10000):
        # Here we add processes that have arrived to the queue of processes
        if no_process_waiting_for_arrival != len(processes):
            while processes[no_process_waiting_for_arrival].arrival_time == i:
                waiting_processses.append(processes[no_process_waiting_for_arrival])
                no_process_waiting_for_arrival += 1

                # If there are no more processes that will arrive we break from this loop
                if no_process_waiting_for_arrival == len(processes):
                    break

        # Swaping the finished process with a new one
        if len(waiting_processses) != 0 and current_process.burst_time <= 0:
            current_process = waiting_processses[0]
            waiting_processses.pop(0)
            current_quant = 0

        # Current process gets replaced with first waiting process and than it gets put in the end of the list
        if len(waiting_processses) != 0 and current_quant >= quant:
            waiting_processses.append(current_process)
            current_process = waiting_processses[0]
            waiting_processses.pop(0)
            current_quant = 0

        current_process.burst_time -= 1
        current_quant += 1
        overall_waiting_time += len(waiting_processses)
        # Increasing waiting time for all waiting_processes
        # (useful if we want to analyse waiting time for individual processes)
        for j in range(0, len(waiting_processses)):
            waiting_processses[j].waiting_time += 1

    if len(waiting_processses) != 0:
        print("RR processes still left")
        for process in waiting_processses:
            print(process)
        print()

        waiting_processses.sort(key=lambda x: x.waiting_time, reverse=True)
        print("Longest waiting process that is still waiting for execution")
        print(waiting_processses[0])
        print()

    else:
        print("No processes left for FCFS")

    return overall_waiting_time / len(processes)


'''# Preemptive SJF (Shorest Job First)
def SFJP(processes):
    # Sorting by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    overall_waiting_time = 0

    current_process = processes[0]
    waiting_processses = []
    no_process_waiting_for_arrival = 1

    # I assume that processes won't take longer than 100000 seconds
    for i in range(current_process.arrival_time, 100000):
        print(str(i) + " " + str(current_process.no_of_process))

        # Here we add processes that have arrived to the queue of processes
        if no_process_waiting_for_arrival != len(processes):
            while processes[no_process_waiting_for_arrival].arrival_time == i:
                waiting_processses.append(processes[no_process_waiting_for_arrival])
                no_process_waiting_for_arrival = no_process_waiting_for_arrival + 1

                # If the burst time of the arriving process is shorter than the burst time of the current process
                # We need to switch it
                if waiting_processses[-1].burst_time < current_process.burst_time:
                    current_process, waiting_processses[-1] = waiting_processses[-1], current_process

                # If there are no more processes that will arrive we break from this loop
                if no_process_waiting_for_arrival == len(processes):
                    break

        # Swaping the finished process with a new one
        if len(waiting_processses) != 0 and current_process.burst_time <= 0:
            # Sorting by the burst time
            waiting_processses.sort(key=lambda x: x.burst_time)
            current_process = waiting_processses[0]
            waiting_processses.pop(0)
            overall_waiting_time = overall_waiting_time + current_process.waiting_time

        current_process.burst_time = current_process.burst_time - 1
        # Increasing waiting time for all waiting_processes
        for j in range(0, len(waiting_processses)):
            waiting_processses[j].waiting_time = waiting_processses[j].waiting_time + 1

        print(str(i) + " " + str(current_process.no_of_process))
        print()

    return overall_waiting_time / len(processes)'''
