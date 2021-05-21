class LRU:
    def __init__(self):
        self.no_simulations = 0
        self.no_page_errors = 0
        # This will allow us to track what page gave the most errors
        self.no_errors_per_page = {}

    def lru(self, no_frames, pages):
        no_page_errors = 0
        frames = [0] * no_frames
        # The first value will keep a page that was least recently used
        pages_in_memory = []

        for page in pages:
            # Was frame found for the page
            is_resolved = False
            # Searching for page in frames
            for i in range(no_frames):
                if frames[i] == page:
                    pages_in_memory.remove(page)
                    pages_in_memory.append(page)
                    is_resolved = True
                    break
                # There were no pages on this frame
                if frames[i] == 0:
                    no_page_errors += 1
                    self.no_errors_per_page[page] = 1
                    frames[i] = page
                    pages_in_memory.append(page)
                    is_resolved = True
                    break

            if not is_resolved:
                no_page_errors += 1
                if page in self.no_errors_per_page:
                    self.no_errors_per_page[page] = self.no_errors_per_page[page] + 1
                else:
                    self.no_errors_per_page[page] = 1

                least_recently_used_page = pages_in_memory.pop(0)
                pages_in_memory.append(page)

                # Changing the appropriate frame
                for j in range(no_frames):
                    if frames[j] == least_recently_used_page:
                        frames[j] = page
                        break

        self.no_simulations += 1
        self.no_page_errors += no_page_errors
        return "LRU result: {result}".format(result=no_page_errors)

    def get_results(self):
        return "LRU result: {result}".format(result=self.no_page_errors / self.no_simulations)

    def get_page_that_caused_most_errors(self):
        sorted_directory = dict(sorted(self.no_errors_per_page.items(), key=lambda item: item[1], reverse=True))
        page = next(iter(sorted_directory.keys()))
        return "Page with the most errors: {page}\nNumber of errors: {errors}\n".format(
            page=page, errors=sorted_directory[page])
