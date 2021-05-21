class FIFO:
    def __init__(self):
        self.no_simulations = 0
        self.no_page_errors = 0
        # This will allow us to track what page gave the most errors
        self.no_errors_per_page = {}

    def fifo(self, no_frames, pages):
        no_page_errors = 0
        frames = [0] * no_frames
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

        self.no_simulations += 1
        self.no_page_errors += no_page_errors
        return "FIFO result: {result}".format(result=no_page_errors)

    def get_results(self):
        return "FIFO result: {result}".format(result=self.no_page_errors / self.no_simulations)

    def get_page_that_caused_most_errors(self):
        sorted_directory = dict(sorted(self.no_errors_per_page.items(), key=lambda item: item[1], reverse=True))
        page = next(iter(sorted_directory.keys()))
        return "Page with the most errors: {page}\nNumber of errors: {errors}\n".format(
            page=page, errors=sorted_directory[page])