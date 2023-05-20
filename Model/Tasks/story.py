import random
import numpy as np

class Story:
    max_weight = 38

    def __init__(self, id, type):
        self.isWorking = False
        self.isComplete = False
        self.tasks = []
        self.count_task = 0
        self.id_story = id
        self.type_story = type
        self.weight = self.set_weight()
        self.loyal = self.set_loyal()
        self.users = self.set_users()
        self.percent_complete = 0
        create_tasks(self)

    def set_weight(self):
        if self.type_story == 'S':
            self.count_task = np.random.uniform(2, 6)
            return 38
        if self.type_story == 'M':
            self.count_task = np.random.uniform(4, 12)
            return 76
        if self.type_story == 'L':
            self.count_task = np.random.uniform(6, 18)
            return 114
        if self.type_story == 'XL':
            self.count_task = np.random.uniform(8, 24)
            return 152


    def set_loyal(self):
        if self.type_story == 'S':
            return random.randint(2, 5) / 100
        if self.type_story == 'M':
            return random.randint(4, 10) / 100
        if self.type_story == 'L':
            return random.randint(8, 20) / 100
        if self.type_story == 'XL':
            return random.randint(16, 40) / 100

    def set_users(self):
        if self.type_story == 'S':
            return random.randint(2, 5) * 100
        if self.type_story == 'M':
            return random.randint(4, 10) * 100
        if self.type_story == 'L':
            return random.randint(8, 20) * 100
        if self.type_story == 'XL':
            return random.randint(16, 40) * 100

    def get_target(self):
        return self.weight if not self.isStub else -1

    def check_complete(self):
        if self.tasks:
            self.isComplete = True
        else:
            self.isComplete = False
        return True if self.tasks else False
    def create_tasks(self):
        for task_id in range(self.count_task):
            div = self.count_task - task_id
            if(self.weight > 19):
                max_weight = 19
            else:
                max_weight = self.weight
            task = Task(task_id, self.id_story, self.weight//div, max_weight)
            self.weight -= task.weight
            self.tasks.append(task)




