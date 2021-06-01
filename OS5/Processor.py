

class Processor:
    def __init__(self, id_number, maximum_load, minimal_load):
        # Used to identify the processor
        self.id_number = id_number
        # Maximum load that should only be crossed if necessary
        self.maximum_load = maximum_load
        # Minimal load from which it can accept new processes from other processors
        self.minimal_load = minimal_load
        # Current load
        self.load = 0
        # All active processes in the processor
        self.processes = []
        # Every 20 seconds we take the value of load and store it here
        self.avg_load = []
        # How often was this processor asked for his load
        self.no_times_asked_for_load = 0
        # How often was the process added from another processor
        self.no_times_got_process = 0
        # How often was the process removed for another processor
        self.no_times_removed_process = 0

    #  Execute for one second all processes in the processor
    def perform_one_iteration(self, time):
        for p in self.processes:
            p.execution_time -= 1
        self.processes = [p for p in self.processes if p.execution_time > 0]
        self.load = sum([p.load for p in self.processes])
        if time % 20 == 0:
            self.avg_load.append(self.load)

    def add_process(self, process):
        self.processes.append(process)
        self.load += process.load

    def add_process_from_another_processor(self, process):
        self.no_times_got_process += 1
        self.processes.append(process)
        self.load += process.load

    # Remove last process from the list
    def remove_process_for_another_processor(self):
        self.no_times_removed_process += 1
        process = self.processes.pop()
        self.load -= process.load
        return process

    def should_process_be_executed(self):
        self.no_times_asked_for_load += 1
        return self.load <= self.maximum_load

    # The processor cannot perform at more than 100% capacity
    def can_process_be_executed(self, process):
        self.no_times_asked_for_load += 1
        return self.load + process.load <= 100

    # Check if the processor should receive a process from another processor
    def should_receive_process(self):
        self.no_times_asked_for_load += 1
        return self.load < self.minimal_load

    # Check if the processor should give a process to another processor
    def should_give_process(self):
        self.no_times_asked_for_load += 1
        return self.load > self.maximum_load

    def reset(self):
        self.avg_load = []
        self.no_times_asked_for_load = 0
        self.no_times_got_process = 0
        self.no_times_removed_process = 0
