# Algorithm number 4
import math
import sys


# This works
class WorkingSet:
    def __init__(self, no_frames, time_frame, c):
        self.no_frames = no_frames
        # Number of page errors in all simulations
        self.overall_no_page_errors = 0
        # Time after which we will check for working set size and change frames
        self.time_frame = time_frame
        # Time after we will create WSS for every process
        self.c = c
        # Overall number of times the processes had to be frozen
        # We also count every frozen process that wasn't "unfrozen"
        self.overall_no_times_process_frozen = 0

    # This algorithm will divide frames proportionally
    def divide_frames_at_start(self, processes):
        no_of_frames_per_process = []
        overall_no_processes = 0
        # Calculating the average number of frames needed for one page
        for i in range(len(processes)):
            overall_no_processes += len(processes[i].pages)
        no_frames_for_every_page = self.no_frames / overall_no_processes

        # Assigning frames to the processes (rounded down)
        used_frames = 0
        for i in range(len(processes)):
            no_frames = math.ceil(no_frames_for_every_page * len(processes[i].pages))
            no_of_frames_per_process.append(no_frames)
            used_frames += no_frames

        # Assigning leftover frames
        left_frames = self.no_frames - used_frames
        for i in range(left_frames):
            no_of_frames_per_process[i] += 1

        return no_of_frames_per_process

    # Divide the leftover frames after the process is finished
    # noinspection PyMethodMayBeStatic
    def divide_frames(self, no_leftover_frames, processes):
        no_of_frames_per_process = []
        overall_no_processes = 0
        # Calculating the average number of frames needed for one page (pages that were left)
        for i in range(len(processes)):
            if processes[i].state == 'Active':
                overall_no_processes = overall_no_processes + len(processes[i].pages) - processes[i].current_page

        # Very rare condition but sometimes overall_no_processes may be equal to 0
        if overall_no_processes == 0:
            return [0] * len(processes)
        no_frames_for_every_page = no_leftover_frames / overall_no_processes

        # Assigning frames to the processes (rounded down)
        used_frames = 0
        for i in range(len(processes)):
            if processes[i].state == 'Active':
                no_frames = math.ceil(no_frames_for_every_page * (len(processes[i].pages) - processes[i].current_page))
                no_of_frames_per_process.append(no_frames)
                used_frames += no_frames

        # Assigning leftover frames
        left_frames = no_leftover_frames - used_frames
        for i in range(left_frames):
            if processes[i].state == 'Active':
                no_of_frames_per_process[i] += 1

        return no_of_frames_per_process

    def perform_simulation(self, processes):
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
                    no_page_errors += processes[i].forward(4)

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

        self.overall_no_page_errors += no_page_errors
        self.overall_no_times_process_frozen += no_times_process_frozen
        return no_page_errors, no_times_process_frozen

    def get_results_many_simulations(self):
        return self.overall_no_page_errors, self.overall_no_times_process_frozen
