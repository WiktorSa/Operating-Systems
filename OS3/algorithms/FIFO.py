import numpy as np
from algorithms.algorithm import Algorithm


class FIFO(Algorithm):
    def perform_simulation(self, no_frames: int, pages: np.array):
        no_page_errors = 0
        frames = np.zeros(shape=no_frames, dtype=np.int32)
        # This index will point to the frame that had a page that was the longest in memory
        longest_in_memory = 0

        for page in pages:
            # Was frame found for the page
            is_resolved = False
            # Searching for page in frames
            for i in range(no_frames):
                if frames[i] == page:
                    is_resolved = True
                    break
                # There were no pages on this frame
                if frames[i] == 0:
                    no_page_errors += 1
                    self.no_errors_per_page[page] = 1
                    frames[i] = page
                    is_resolved = True
                    break

            if not is_resolved:
                no_page_errors += 1
                if page in self.no_errors_per_page:
                    self.no_errors_per_page[page] = self.no_errors_per_page[page] + 1
                else:
                    self.no_errors_per_page[page] = 1

                frames[longest_in_memory] = page

                longest_in_memory += 1
                if longest_in_memory == no_frames:
                    longest_in_memory = 0

        print("FIFO result: ", no_page_errors)
        self.no_simulations += 1
        self.no_page_errors += no_page_errors
