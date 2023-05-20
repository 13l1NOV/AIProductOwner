import random


def set_weight(min_weight, max_weight):
    return random.randint(min_weight, max_weight)


class Task:

    def __init__(self, id_task, id_story, min_weight, max_weight):
        self.isStub = False
        self.id = id_task
        self.id_story = id_story
        self.weight = set_weight(min_weight, max_weight)
        self.part_percent = self.weight*38/100
        self.isWorking = False


    def get_target(self):
        return self.weight if not self.isStub else -1
