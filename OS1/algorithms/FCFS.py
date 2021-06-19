import collections
from algorithms.Algorithm import Algorithm


# First Come First Served
class FCFS(Algorithm):
    def perform_simulation(self, processes: collections.deque):
        overall_waiting_time = 0
        current_process = processes.popleft()
        waiting_processses = collections.deque()

        # The max length is 10000 so that we could analyse any processes that were left over
        for i in range(10000):
            # Here we add processes that have arrived to the queue of processes
            while len(processes) > 0 and processes[0].arrival_time == i:
                waiting_processses.append(processes.popleft())

            # Swap the finished process with a new one
            if current_process.burst_time <= 0 and len(waiting_processses) > 0:
                current_process = waiting_processses.popleft()

            current_process.burst_time -= 1
            overall_waiting_time += len(waiting_processses)
            # Increasing waiting time for all waiting_processes
            # (useful if we want to analyse waiting time for individual processes)
            for process in waiting_processses:
                process.waiting_time += 1

        print("FCFS results:")
        print("Waiting time: {wait_time}".format(wait_time=overall_waiting_time))

        if len(waiting_processses) != 0:
            print("Processes still in queue")
            while len(waiting_processses) > 0:
                print(waiting_processses.popleft())

        else:
            print("No processes left")

        print()

        self.overall_waiting_time += overall_waiting_time
