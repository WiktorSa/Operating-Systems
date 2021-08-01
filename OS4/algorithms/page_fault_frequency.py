from algorithms.algorithm import Algorithm


# Algorithm 3
class PageFaultFrequency(Algorithm):
    def __init__(self, no_frames, no_processes: int, no_simulations: int, is_3_or_4: bool, time_frame: int,
                 l: float, u: float, h: float):
        super().__init__(no_frames, no_processes, no_simulations, is_3_or_4)
        # Time after which we will check for working set size and change frames
        self.time_frame = time_frame
        # Parameters used to keep track of the page fault frequency
        self.l = l
        self.u = u
        self.h = h
        # Overall number of times the processes had to be frozen
        # We also count every frozen process that wasn't "unfrozen"
        self.overall_no_times_process_frozen = 0

    def perform_simulation(self, processes: list):
        original_no_of_frames = self.divide_frames_at_start(processes)
        for i in range(len(processes)):
            processes[i].lru.set_original_number_of_frames(original_no_of_frames[i])

        no_page_errors = 0
        no_times_process_frozen = 0
        # Perform simulation until all processes are finished
        time_for_time_frame = 0
        not_counting_errors = True
        no_finished_processes = 0
        while no_finished_processes < len(processes):
            # Doing one iteration of lru algorithm for every process
            for i in range(len(processes)):
                if processes[i].state == 'Active':
                    no_page_errors += processes[i].use_lru()

                    # The process has finished
                    if processes[i].state == 'Finished':
                        no_finished_processes += 1

                        # Distribute frames to other processes
                        frames_to_distribute = self.divide_frames(len(processes[i].lru.frames), processes)
                        frame_index = 0
                        for j in range(len(processes)):
                            if processes[j].state == 'Active':
                                processes[j].lru.change_frames(len(processes[j].lru.frames) +
                                                               frames_to_distribute[frame_index])
                                frame_index += 1

                        # We can perform simulation without this line but this will be useful for potential debugging
                        processes[i].lru.change_frames(0)

            time_for_time_frame += 1

            if time_for_time_frame == 10 and not_counting_errors:
                time_for_time_frame = 0
                not_counting_errors = False

            # PFF will be used here to distribute frames
            if time_for_time_frame == self.time_frame:
                time_for_time_frame = 0
                # Generating PFF for every active process
                # Pseudo-dictionary that contains number of errors per time frame
                PFF = []
                # Page that may turn to active if there are enough frames to distribute
                frozen_process = None
                for i in range(len(processes)):
                    if processes[i].state == 'Active':
                        PFF.append([i, sum(processes[i].lru.errors_in_time_frame) / self.time_frame])
                    elif processes[i].state == 'Frozen':
                        processes[i].no_times_frozen += 1
                        no_times_process_frozen += 1
                        frozen_process = processes[i]

                # Sort our PFF list by the value of PFF
                PFF.sort(key=lambda x: x[1], reverse=False)

                # Assigning frames till we ran out of frames to distribute or processes that need frames
                while len(PFF) > 1 and PFF[0][1] < self.l and PFF[-1][1] > self.u:
                    processes[PFF[0][0]].lru.remove_frame()
                    processes[PFF[-1][0]].lru.add_frame()
                    del PFF[0]
                    del PFF[-1]

                if len(PFF) > 0:
                    # We will need to stop this process
                    if PFF[-1][1] > self.h:
                        processes[PFF[-1][0]].no_times_frozen += 1
                        no_times_process_frozen += 1
                        left_frames = len(processes[PFF[-1][0]].lru.frames)
                        processes[PFF[-1][0]].lru.change_frames(0)
                        processes[PFF[-1][0]].state = 'Frozen'
                        del PFF[-1]

                        # First every process that requested for more frames will be given one extra frame
                        while len(PFF) > 0 and PFF[-1][1] > self.u and left_frames > 0:
                            processes[PFF[-1][0]].lru.add_frame()
                            left_frames -= 1
                            del PFF[-1]

                        # Distribute frames to other processes
                        frames_to_distribute = self.divide_frames(left_frames, processes)
                        frame_index = 0
                        for j in range(len(processes)):
                            if processes[j].state == 'Active':
                                processes[j].lru.change_frames(len(processes[j].lru.frames) +
                                                               frames_to_distribute[frame_index])
                                frame_index += 1

                    # We can restore the frozen process
                    elif PFF[0][1] < self.l and PFF[-1][1] <= self.u and frozen_process is not None:
                        # We counted this as frozen by accident earlier
                        frozen_process.no_times_frozen -= 1
                        no_times_process_frozen -= 1
                        frozen_process.state = 'Active'
                        frames_to_distribute = 0
                        # Gather every frame possible to give it to the frozen process
                        while len(PFF) > 0 and PFF[0][1] < self.l:
                            processes[PFF[0][0]].lru.remove_frame()
                            frames_to_distribute += 1
                            del PFF[0]
                        frozen_process.lru.change_frames(frames_to_distribute)

        print("Page Fault Frequency - number of page errors: ", no_page_errors)
        print("Number of times the processes got frozen: ", no_times_process_frozen)
        print("Number of page errors/times frozen for everry process: ")
        for i in range(len(processes)):
            print("Process number: {no} - {no_page_errors} / {times_frozen}".format(
                no=i + 1, no_page_errors=processes[i].no_page_errors, times_frozen=processes[i].no_times_frozen))
            self.no_page_errors_process[i] += processes[i].no_page_errors
            self.no_process_frozen[i] += processes[i].no_times_frozen

        self.overall_no_page_errors += no_page_errors
        self.overall_no_times_process_frozen += no_times_process_frozen
