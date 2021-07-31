import numpy as np
from algorithms.algorithm import Algorithm


# LRU Approximation
class LRUApp(Algorithm):
    def perform_simulation(self, no_frames: int, pages: np.array):
        no_page_errors = 0
        frames = np.zeros(shape=no_frames, dtype=np.int32)
        # This will allow us to keep track of reference bits for every page in memory
        pages_in_memory = {}

        for page in pages:
            # Was frame found for the page
            is_resolved = False
            # Searching for page in frames
            for i in range(no_frames):
                if frames[i] == page:
                    pages_in_memory[page] = 1
                    is_resolved = True
                    break
                # There were no pages on this frame
                if frames[i] == 0:
                    no_page_errors += 1
                    self.no_errors_per_page[page] = 1
                    frames[i] = page
                    pages_in_memory[page] = 1
                    is_resolved = True
                    break

            if not is_resolved:
                no_page_errors += 1
                if page in self.no_errors_per_page:
                    self.no_errors_per_page[page] = self.no_errors_per_page[page] + 1
                else:
                    self.no_errors_per_page[page] = 1

                for key in list(pages_in_memory.keys()):
                    # Found the right page to swap
                    if pages_in_memory[key] == 0:
                        break

                    # Give a second chance to a page
                    else:
                        del pages_in_memory[key]
                        pages_in_memory[key] = 0

                # Deleting the first value in the dictionary
                least_used_page_approximated = next(iter(pages_in_memory.keys()))
                del pages_in_memory[least_used_page_approximated]

                # Addding the page that caused the error to the end of the dictionary
                pages_in_memory[page] = 1

                # Changing the appropriate frame
                for j in range(no_frames):
                    if frames[j] == least_used_page_approximated:
                        frames[j] = page
                        break

        print("LRU Approximation result: ", no_page_errors)
        self.no_simulations += 1
        self.no_page_errors += no_page_errors
