

class Process:
    def __init__(self, id_number, burst_time, arrival_time):
        self.id_number = id_number
        self.burst_time = burst_time  # How long this process should be processed
        self.original_burst_time = burst_time
        self.arrival_time = arrival_time
        self.waiting_time = 0

    def __lt__(self, other):
        return self.burst_time < other.burst_time

    def __str__(self):
        return "{id_number} {burst_time} {original_burst_time} {arrival_time} {waiting_time}".format(
            id_number=self.id_number, burst_time=self.burst_time, original_burst_time=self.original_burst_time,
            arrival_time=self.arrival_time, waiting_time=self.waiting_time)
