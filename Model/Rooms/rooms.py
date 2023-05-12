class Room:

    def __init__(self, idx):
        self.id = idx
        self.limit_robots = 4
        self.count_robots = 1
        self.status_full = False

    def add_robot(self):
        if not self.status_full:
            self.count_robots += 1
            if self.count_robots >= self.limit_robots:
                self.status_full = True

    def check_list(self):
        print(self.count_robots)
