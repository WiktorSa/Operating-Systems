import queue
import random
from Algorithm2 import Algorithm2


class Algorithm3(Algorithm2):
    def __init__(self, processors, max_no_searches_alg_2, max_no_searches):
        super().__init__(processors, max_no_searches_alg_2)
        self.max_no_searches = max_no_searches

    def move_processes(self):
        for pr1 in self.processors:
            if pr1.should_receive_process():
                for _ in range(self.max_no_searches):
                    pr2 = self.processors[random.randrange(0, len(self.processors))]
                    # The processor cannot ask itself for transfer
                    while pr1 == pr2:
                        pr2 = self.processors[random.randrange(0, len(self.processors))]

                    # We will pass processes until pr2 is under the limit
                    while pr2.should_give_process():
                        p = pr2.remove_process_for_another_processor()
                        pr1.add_process_from_another_processor(p)
