class Office:
    def __init__(self):
        self.cost_robot = 50000
        self.count_robot = 2
        self.cost_work = 10000

    def add_robot(self):  # ограничений на кол-во роботов у нас нету
        self.count_robot += 1
        self.cost_work += 10000
        if self.count_robot < 17:
            if self.count_robot % 4 == 0:
                self.cost_robot = 200000 * 1.5 * (self.count_robot // 4)
            else:
                self.cost_robot = 50000
        else:
            self.cost_robot *= 2
