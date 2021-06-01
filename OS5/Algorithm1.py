import queue
import random
from Algorithms import Algorithms


class Algorithm1(Algorithms):
    def __init__(self, processors, max_no_searches):
        super().__init__(processors)
        self.max_no_searches = max_no_searches

    def get_processor(self, process):
        for _ in range(self.max_no_searches):
            pr = self.processors[random.randrange(0, len(self.processors))]
            # The processor cannot ask itself to execute process
            while pr.id_number == process.no_processor:
                pr = self.processors[random.randrange(0, len(self.processors))]

            if pr.should_process_be_executed():
                return pr

        # Check if the process can be executed on the original processor
        if (pr := self.processors[process.no_processor]).can_process_be_executed(process):
            return pr

        return None
