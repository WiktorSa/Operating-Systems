# Algorithm number 3
import math
import sys


# This works
class PageFaultFrequency:
    def __init__(self, no_frames, time_frame, l, u, h):
        self.no_frames = no_frames
        # Number of page errors in all simulations
        self.overall_no_page_errors = 0
        # Time after which we will check for working set size and change frames
        self.time_frame = time_frame
        # Parameters used to keep track of the page fault frequency
        self.l = l
        self.u = u
        self.h = h
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
        not_counting_errors = True
        no_finished_processes = 0
        while no_finished_processes < len(processes):
            # Doing one iteration of lru algorithm for every process
            for i in range(len(processes)):
                if processes[i].state == 'Active':
                    no_page_errors += processes[i].forward(3)

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
                # Dictionary that contains number of errors per time frame
                PFF = []
                # Page that may turn to active if there are enough frames to distribute
                frozen_process = None
                for i in range(len(processes)):
                    if processes[i].state == 'Active':
                        PFF.append([i, sum(processes[i].lru.errors_in_time_frame) / self.time_frame])
                    elif processes[i].state == 'Frozen':
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
                        no_times_process_frozen -= 1
                        frozen_process.state = 'Active'
                        frames_to_distribute = 0
                        # Gather every frame possible to give it to the frozen process
                        while len(PFF) > 0 and PFF[0][1] < self.l:
                            processes[PFF[0][0]].lru.remove_frame()
                            frames_to_distribute += 1
                            del PFF[0]
                        frozen_process.lru.change_frames(frames_to_distribute)

        self.overall_no_page_errors += no_page_errors
        self.overall_no_times_process_frozen += no_times_process_frozen
        return no_page_errors, no_times_process_frozen

    def get_results_many_simulations(self):
        return self.overall_no_page_errors, self.overall_no_times_process_frozen
