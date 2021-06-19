import queue
import collections
from algorithms.Algorithm import Algorithm


# Non-preemptive SJF (Shorest Job First)
class SJF(Algorithm):
    def perform_simulation(self, processes: collections.deque):
        overall_waiting_time = 0
        current_process = processes.popleft()
        waiting_processses = queue.PriorityQueue()

        # The max length is 10000 so that we could analyse any processes that were left over
        for i in range(10000):
            # Here we add processes that have arrived to the queue of processes
            while len(processes) > 0 and processes[0].arrival_time == i:
                waiting_processses.put(processes.popleft())

            # Swap the finished process with a new one (note that we use priority queue so everything should be sorted)
            if current_process.burst_time <= 0 and waiting_processses.qsize() > 0:
                current_process = waiting_processses.get()

            current_process.burst_time -= 1
            overall_waiting_time += waiting_processses.qsize()
            # Increasing waiting time for all waiting_processes
            # (useful if we want to analyse waiting time for individual processes)
            for process in waiting_processses.queue:
                process.waiting_time += 1

        print("SJF results:")
        print("Waiting time: {wait_time}".format(wait_time=overall_waiting_time))

        if waiting_processses.qsize() != 0:
            print("Processes still in queue")
            while waiting_processses.qsize() > 0:
                print(waiting_processses.get())

        else:
            print("No processes left")

        print()

        self.overall_waiting_time += overall_waiting_time
