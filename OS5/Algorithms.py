import queue
import numpy as np
from abc import abstractmethod


class Algorithms:
    def __init__(self, processors):
        self.processors = processors
        # List containing the waiting time for execution for every process
        self.wait_times_execution = []
        # Lists used to store data from every simulation to use for final results
        self.avg_load_processors = []
        self.avg_no_asked_for_load = []
        self.avg_no_process_moved = []
        self.avg_wait_time_execution = []

    def perform_simulation(self, processes):
        time = 0
        index = 0
        q = queue.Queue()
        # Perform simulation until every process is finished
        while any(pr.load != 0 for pr in self.processors) or index < processes.shape[0]:
            # Put every process with proper time entrance in the queue
            while index < processes.shape[0] and (p := processes[index]).entrance_time == time:
                q.put(p)
                index += 1

            # Try to execute process on a processor
            while q.qsize() > 0 and (pr := self.get_processor(q.queue[0])) is not None:
                p = q.get()
                self.wait_times_execution.append(p.waiting_time_for_execution)
                pr.add_process(p)

            # Move processes from one processor to another (exclusive to algorithm 3)
            self.move_processes()

            for pr in self.processors:
                pr.perform_one_iteration(time)

            for p in q.queue:
                p.waiting_time_for_execution += 1

            time += 1

    @abstractmethod
    def get_processor(self, process):
        return

    def move_processes(self):
        return

    # Print all the statistics we can collect
    def print_result_one_simulation(self):
        avg_load_processors = [np.mean(pr.avg_load) for pr in self.processors]
        std_load_processors = [np.std(pr.avg_load) for pr in self.processors]
        avg_no_times_asked_for_load = [pr.no_times_asked_for_load for pr in self.processors]
        avg_no_times_got_process = [pr.no_times_got_process for pr in self.processors]
        avg_no_times_removed_process = [pr.no_times_removed_process for pr in self.processors]

        print("Average load of the processors: {avg:.4f}".format(avg=np.mean(avg_load_processors)))
        print("Std of the average loads: {std:.4f}".format(std=np.std(avg_load_processors)))
        print("Average std of loads for every process separately: {mean:.4f}".format(mean=np.mean(std_load_processors)))
        print("Average load for processor 0: {mean:.4f}".format(mean=avg_load_processors[0]))
        print("Std of loads for processor 0: {std:.4f}".format(std=std_load_processors[0]))
        print("Maximal average load: {max:.4f} Processor: {argmax}".format(
            max=np.max(avg_load_processors), argmax=np.argmax(avg_load_processors)))
        print("Minimal average load: {min:.4f} Processor: {argmin}".format(
            min=np.min(avg_load_processors), argmin=np.argmin(avg_load_processors)))
        print("Average number of times the processors were asked for their load: {avg:.4f}".format(
            avg=np.mean(avg_no_times_asked_for_load)))
        print("Maximal times asked for the load: {max} Processor: {argmax}".format(
            max=np.max(avg_no_times_asked_for_load), argmax=np.argmax(avg_no_times_asked_for_load)))
        print("Minimal times asked for the load: {min} Processor: {argmin}".format(
            min=np.min(avg_no_times_asked_for_load), argmin=np.argmin(avg_no_times_asked_for_load)))
        print("Average number of times the process got moved from one processor to another: {avg:.4f}".format(
            avg=np.mean(avg_no_times_got_process)))
        print("Maximal number of times the processor got process from another processor: {max} Processor: {argmax}"
              .format(max=np.max(avg_no_times_got_process), argmax=np.argmax(avg_no_times_got_process)))
        print("Minimal number of times the processor got process from another processor: {min} Processor: {argmin}"
              .format(min=np.min(avg_no_times_got_process), argmin=np.argmin(avg_no_times_got_process)))
        print("Maximal number of times the process gave process to another processor: {max} Processor: {argmax}"
            .format(max=np.max(avg_no_times_removed_process), argmax=np.argmax(avg_no_times_removed_process)))
        print("Minimal number of times the process gave process to another processor: {min} Processor {argmin}"
            .format(min=np.min(avg_no_times_removed_process), argmin=np.argmin(avg_no_times_removed_process)))
        print("Average waiting time for execution: {avg:.4f}".format(avg=np.mean(self.wait_times_execution)))
        print("Maximal waiting time for execution: {max}".format(max=np.max(self.wait_times_execution)))

    # Saving results of one simulation to use later
    def save_results(self):
        self.avg_load_processors.append(np.mean([np.mean(pr.avg_load) for pr in self.processors]))
        self.avg_no_asked_for_load.append(np.mean([pr.no_times_asked_for_load for pr in self.processors]))
        self.avg_no_process_moved.append(np.mean([pr.no_times_got_process for pr in self.processors]))
        self.avg_wait_time_execution.append(np.mean(self.wait_times_execution))

    def print_results_many_simulations(self):
        print("Average load of the processors: {avg:.4f}".format(avg=np.mean(self.avg_load_processors)))
        print("Std of the average: {std:.4f}".format(std=np.std(self.avg_load_processors)))
        print("Average number of times asked for load: {avg:.4f}".format(avg=np.mean(self.avg_no_asked_for_load)))
        print("Average number of times processes got moved: {avg:.4f}".format(avg=np.mean(self.avg_no_process_moved)))
        print("Average waiting time for execution: {avg:.4f}".format(avg=np.mean(self.avg_wait_time_execution)))

    def reset(self):
        for pr in self.processors:
            pr.reset()
        self.wait_times_execution = []
