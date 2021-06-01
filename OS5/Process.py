
class Process:
    def __init__(self, entrance_time, load, execution_time, no_processor):
        # When the process will start realising
        self.entrance_time = entrance_time
        # How much of the processor this process requires
        self.load = load
        # How long our process should be realised
        self.execution_time = execution_time
        # We assume that if the process cannot be realised it will wait in the queue
        self.waiting_time_for_execution = 0
        # For reproducibility we assume that the process knows which processor to ask for execution
        self.no_processor = no_processor
