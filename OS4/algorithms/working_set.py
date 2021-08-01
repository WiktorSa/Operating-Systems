from algorithms.algorithm import Algorithm


# Algorithm 4
class WorkingSet(Algorithm):
    def __init__(self, no_frames, no_processes: int, no_simulations: int, is_3_or_4: bool, time_frame: int, c: float):
        super().__init__(no_frames, no_processes, no_simulations, is_3_or_4)
        # Time after which we will check for working set size and change frames
        self.time_frame = time_frame
        # Time after we will create WSS for every process
        self.c = c
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
        time_for_c = 0
        # Working set for active processes
        WSS = []
        # Working set for frozen processes
        WSS_frozen = []
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
            time_for_c += 1

            # Creating WSS for every process
            if time_for_c == self.c:
                time_for_c = 0
                WSS = []
                WSS_frozen = []
                for i in range(len(processes)):
                    if processes[i].state == 'Active':
                        # Our working set is equal to the number of unique pages over the given period of time
                        WSS.append([i, len(set(processes[i].lru.pages_in_time_c))])
                    elif processes[i].state == 'Frozen':
                        WSS_frozen.append([i, len(set(processes[i].lru.pages_in_time_c))])

            # Using WSS to distribute frames
            if time_for_time_frame == self.time_frame:
                time_for_time_frame = 0
                # Sorting WSS from the processes that require the least amount of frames
                WSS.sort(key=lambda x: x[1], reverse=False)
                WSS_frozen.sort(key=lambda x: x[1], reverse=False)
                left_frames = self.no_frames
                # Distributing frames according the WSS (firstly active processes)
                while len(WSS) > 0:
                    # There are frames left to distribute
                    if WSS[0][1] <= left_frames:
                        processes[WSS[0][0]].lru.change_frames(WSS[0][1])
                        left_frames -= WSS[0][1]
                        del WSS[0]
                    else:
                        processes[WSS[0][0]].lru.change_frames(0)
                        processes[WSS[0][0]].state = 'Frozen'
                        processes[WSS[0][0]].no_times_frozen += 1
                        no_times_process_frozen += 1
                        del WSS[0]

                # Distributing frames to the frozen processes (if possible)
                while len(WSS_frozen) > 0:
                    if WSS_frozen[0][1] <= left_frames:
                        processes[WSS_frozen[0][0]].lru.change_frames(WSS_frozen[0][1])
                        processes[WSS_frozen[0][0]].state = 'Active'
                        left_frames -= WSS_frozen[0][1]
                        del WSS_frozen[0]
                    else:
                        processes[WSS_frozen[0][0]].no_times_frozen += 1
                        no_times_process_frozen += 1
                        del WSS_frozen[0]

                # Distribute leftover frames
                frames_to_distribute = self.divide_frames(left_frames, processes)
                frame_index = 0
                for j in range(len(processes)):
                    if processes[j].state == 'Active':
                        processes[j].lru.change_frames(len(processes[j].lru.frames) +
                                                       frames_to_distribute[frame_index])
                        frame_index += 1

        print("Working Set - number of page errors: ", no_page_errors)
        print("Number of times the processes got frozen: ", no_times_process_frozen)
        print("Number of page errors/times frozen for everry process: ")
        for i in range(len(processes)):
            print("Process number: {no} - {no_page_errors} / {times_frozen}".format(
                no=i + 1, no_page_errors=processes[i].no_page_errors, times_frozen=processes[i].no_times_frozen))
            self.no_page_errors_process[i] += processes[i].no_page_errors
            self.no_process_frozen[i] += processes[i].no_times_frozen

        self.overall_no_page_errors += no_page_errors
        self.overall_no_times_process_frozen += no_times_process_frozen
