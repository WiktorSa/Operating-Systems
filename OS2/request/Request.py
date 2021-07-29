class Request:
    def __init__(self, no_process, block_position, arrival_time, is_real_time=False, deadline_time=None):
        self.no_process = no_process
        self.block_position = block_position
        self.arrival_time = arrival_time
        self.waiting_time = 0
        self.is_real_time = is_real_time
        # Only applies if is_real_time == True
        self.deadline_time = deadline_time

    def __str__(self):
        return "{no_process} {block_position} {arrival_time} {waiting_time} {is_real_time} {deadline_time}".format(
            no_process=self.no_process, block_position=self.block_position, arrival_time=self.arrival_time,
            waiting_time=self.waiting_time, is_real_time=self.is_real_time, deadline_time=self.deadline_time
        )

    def __lt__(self, other):
        return self.waiting_time < other.waiting_time
