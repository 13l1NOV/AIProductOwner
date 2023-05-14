import random


def set_weight(max_weight):
    return random.randint(1, max_weight)


class SubTask:
    def __init__(self):
        self.isStub = True
        self.is_selected = False

    def __init__(self, id_subtask, id_task, max_weight):
        self.isStub = False
        self.is_selected = False
        self.id = id_subtask
        self.id_task = id_task
        self.weight = max_weight#set_weight(max_weight)


    def get_target(self):
        return self.weight if not self.isStub else -1
