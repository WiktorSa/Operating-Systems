from result.result import Result


if __name__ == '__main__':
    no_pages = [2143, 2335, 2394, 2889, 2955, 3030, 2657, 2500, 2967, 2463]
    start_pages = [1, 31, 56, 100, 129, 167, 199, 240, 284, 310]
    end_pages = [30, 55, 99, 128, 166, 198, 239, 283, 309, 337]
    localities_of_reference = [[2, 5, 18, 20], [31, 42, 47], [59, 69, 72, 78, 98], [100, 103, 105],
                               [130, 149, 155, 160], [168, 179, 180], [200, 230, 235, 236], [244, 256, 265],
                               [285, 290, 295, 301, 306], [314, 318, 329, 330]]
    how_large_localites = [20, 22, 24, 29, 18, 16, 28, 27, 16, 19]
    how_often_localities = [50, 40, 38, 44, 52, 36, 40, 55, 52, 49]

    no_simulations = 20
    no_frames = 100
    time_frame = 30
    l = 0.2
    u = 0.4
    h = 0.4
    c = 12

    r = Result(no_pages, start_pages, end_pages, localities_of_reference, how_large_localites, how_often_localities)
    r.get_results(no_simulations, no_frames, time_frame, l, u, h, c)
