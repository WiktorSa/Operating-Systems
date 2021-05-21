class Process:
    def __init__(self, no_of_process, burst_time, arrival_time):
        self.no_of_process = no_of_process
        self.burst_time = burst_time  # Length process
        self.original_burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0

    def __str__(self):
        return str(self.no_of_process) + " " + str(self.burst_time) + " " + str(self.original_burst_time) + " " + \
               str(self.arrival_time) + " " + str(self.waiting_time)
