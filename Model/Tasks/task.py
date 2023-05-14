import random


class Task:
    max_weight = 38
    def __init__(self):
        self.isStub = True

    def __init__(self, id, type):
        self.isStub = False
        self.id_task = id
        self.type_task = type
        self.weight = self.set_weight()
        self.loyal = self.set_loyal()
        self.users = self.set_users()

    def set_weight(self):
        if self.type_task == 'S':
            return 38
        if self.type_task == 'M':
            return 76
        if self.type_task == 'L':
            return 114
        if self.type_task == 'XL':
            return 152

    def set_loyal(self):
        if self.type_task == 'S':
            return random.randint(2, 5) / 100
        if self.type_task == 'M':
            return random.randint(4, 10) / 100
        if self.type_task == 'L':
            return random.randint(8, 20) / 100
        if self.type_task == 'XL':
            return random.randint(16, 40) / 100

    def set_users(self):
        if self.type_task == 'S':
            return random.randint(2, 5) * 100
        if self.type_task == 'M':
            return random.randint(4, 10) * 100
        if self.type_task == 'L':
            return random.randint(8, 20) * 100
        if self.type_task == 'XL':
            return random.randint(16, 40) * 100

    def get_target(self):
        return self.weight if not self.isStub else -1