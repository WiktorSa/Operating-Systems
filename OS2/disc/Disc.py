class Disc:
    def __init__(self, entrance_position, size_of_disc):
        self.current_position = entrance_position
        self.entrance_position = entrance_position
        self.size_of_disc = size_of_disc

    def __str__(self):
        return str(self.size_of_disc)

    def move_to_beginnging(self):
        self.current_position = 0

    def move_to_end(self):
        self.current_position = self.size_of_disc
