import process.pages


class LRU:
    def __init__(self, time_frame: int, c: int):
        self.frames = None
        # The first value will keep a page that was least recently used
        self.pages_in_memory = []
        # A list of whether we had an error or not during one iteration in the time frame
        self.errors_in_time_frame = [0] * time_frame
        # This will keep all the pages that appeared within the time c
        # Warning - values in this list may not be unique
        self.pages_in_time_c = [0] * c
        self.time_frame = time_frame
        self.c = c

    def forward(self, page: int):
        # 1 if there was a page error, 0 if there wasn't
        page_error = 0
        # Was frame found for the page
        is_resolved = False

        # Searching for page in frames
        for i in range(len(self.frames)):
            if self.frames[i] == page:
                self.pages_in_memory.remove(page)
                self.pages_in_memory.append(page)
                is_resolved = True
                break
            # There were no pages on this frame
            if self.frames[i] == 0:
                page_error = 1
                self.frames[i] = page
                self.pages_in_memory.append(page)
                is_resolved = True
                break

        if not is_resolved:
            page_error = 1
            least_recently_used_page = self.pages_in_memory.pop(0)
            self.pages_in_memory.append(page)

            # Changing the appropriate frame
            for j in range(len(self.frames)):
                if self.frames[j] == least_recently_used_page:
                    self.frames[j] = page
                    break

        self.errors_in_time_frame.pop(0)
        self.errors_in_time_frame.append(page_error)
        self.pages_in_time_c.pop(0)
        self.pages_in_time_c.append(page)

        return page_error

    # Add a new frame (algorithm 3 and 4)
    def add_frame(self):
        self.frames.append(0)

    # Removing the most optimal frame (algorithm 3 and 4)
    # Note - last processes may have more frames than unique pages!
    def remove_frame(self):
        if len(self.pages_in_memory) != 0:
            self.frames.remove(self.pages_in_memory.pop(0))
        else:
            self.frames.pop(0)

    # Changing the number of frames (algorithm 4)
    def change_frames(self, no_frames: int):
        no_frames_to_change = no_frames - len(self.frames)
        if no_frames_to_change > 0:
            for i in range(no_frames_to_change):
                self.add_frame()

        else:
            for i in range(abs(no_frames_to_change)):
                self.remove_frame()

    # Setting the number of frames for this LRU (every algorithm)
    def set_original_number_of_frames(self, no_frames: int):
        self.frames = [0] * no_frames
