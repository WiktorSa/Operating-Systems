class Request:
    def __init__(self, no_of_process, block_position, arrival_time, is_real_time=False, deadline_time=None):
        self.no_of_process = no_of_process
        self.block_position = block_position
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.is_real_time = is_real_time
        # Only applies if is_real_time == True
        self.deadline_time = deadline_time

    def __str__(self):
        return str(self.no_of_process) + " " + str(self.block_position) + " " + \
               str(self.arrival_time) + " " + str(self.waiting_time) + " " + str(self.is_real_time) + \
               " " + str(self.deadline_time)
