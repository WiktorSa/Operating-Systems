import numpy as np
from algorithms.algorithm import Algorithm


class OPT(Algorithm):
    def perform_simulation(self, no_frames: int, pages: np.array):
        no_page_errors = 0
        frames = np.zeros(shape=no_frames, dtype=np.int32)

        for i in range(len(pages)):
            # Was frame found for the page
            is_resolved = False
            # Searching for page in frames
            for j in range(no_frames):
                if frames[j] == pages[i]:
                    is_resolved = True
                    break
                # There were no pages on this frame
                if frames[j] == 0:
                    no_page_errors += 1
                    self.no_errors_per_page[pages[i]] = 1
                    frames[j] = pages[i]
                    is_resolved = True
                    break

            if not is_resolved:
                no_page_errors += 1
                if pages[i] in self.no_errors_per_page:
                    self.no_errors_per_page[pages[i]] = self.no_errors_per_page[pages[i]] + 1
                else:
                    self.no_errors_per_page[pages[i]] = 1

                # Searching for the page that will be used last in the future
                not_found_pages = [frame_page for frame_page in frames]
                j = i + 1
                while j < len(pages) and len(not_found_pages) > 1:
                    if pages[j] in not_found_pages:
                        not_found_pages.remove(pages[j])
                    j += 1

                # Changing the appropriate frame
                for j in range(no_frames):
                    if frames[j] == not_found_pages[0]:
                        frames[j] = pages[i]
                        break

        print("OPT result: ", no_page_errors)
        self.no_simulations += 1
        self.no_page_errors += no_page_errors
