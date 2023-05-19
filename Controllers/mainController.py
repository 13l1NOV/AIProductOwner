from Model.Robots.robot import Robot
from Model.Tasks.task import Task
from Model.Tasks.subtask import SubTask
import random

class Controller:

    def __init__(self, model):
        self.model = model
        self.counter_id = 0
        self.counter_subtask = 0
        self.max_sub = 8

    # Взаимодействие с офисом
    def buy_robot(self):
        if self.model.status.money > 0:
            self.model.status.money -= self.model.office.cost_robot
            self.model.office.count_robot += 1
            max_power = 0
            for room in self.model.office.list_rooms:
                max_power += 10 * room.count_robots
            self.model.status.max_power = max_power
            return True
        else:
            return False

    # Взаимодействие с тасками
    def create_two_easy_task(self):
        if self.model.status.money > 0:
            cost_tasks = 80000
            if cost_tasks < self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.available_tasks.append(Task(self.counter_id, 'S'))
                self.counter_id += 1
                self.model.status.available_tasks.append(Task(self.counter_id, 'S'))
                self.counter_id += 1
                return True
        return False

    def create_one_hard_task(self):
        if self.model.status.money > 0:
            cost_tasks = 160000
            chance = random.randint(1, 100)
            if chance <= 25:
                typeTask = 'M'
            elif 25 < chance <= 75:
                typeTask = 'L'
            else:
                typeTask = 'XL'
            if cost_tasks < self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.available_tasks.append(Task(self.counter_id, typeTask))
                self.counter_id += 1
                return True
        return False

    '''def move_task_to_selected_list(self, id):
        if self.model.status.money > 0 and id != -1:
            for task in self.model.status.available_tasks:
                if task.id_task == id:
                    self.model.status.available_tasks.remove(task)
                    self.model.status.selected_tasks.append(task)
                    self.model.status.current_power += self.model.office.check_status_robot()
                    return True
        return False

    def move_task_to_available_list(self, id):
        if self.model.status.money > 0 and id != -1:
            for task in self.model.status.selected_tasks:
                if task.id_task == id:
                    self.model.status.selected_tasks.remove(task)
                    self.model.status.available_tasks.append(task)
                    self.model.status.current_power -= self.model.office.check_status_robot()
                    #break
                    return True
        #else:
        return False
'''
    def decomposition_tasks(self):
        if self.model.status.money > 0:
            if self.model.status.current_power <= self.model.status.max_power:

                while self.model.status.selected_tasks:
                    task = self.model.status.selected_tasks.pop(0)
                    self.model.status.working_tasks.append(task)

                    while task.weight > 0:
                        max_weight = random.randint(1, 19)
                        subtask = SubTask(self.counter_subtask, task.id_task, max_weight)
                        self.counter_subtask += 1
                        self.model.status.available_subtasks.append(subtask)
                        task.weight -= subtask.weight

                        subtask2 = SubTask(self.counter_subtask, task.id_task, 19-max_weight+1)
                        self.counter_subtask += 1
                        self.model.status.available_subtasks.append(subtask2)
                        task.weight -= subtask2.weight
                return True
        #else:
        return False

    # Взаимодействие с подзадачами
    def move_subtask_to_selected_list(self, id):
        if self.model.status.money > 0  and id != -1:
            for subtask in self.model.status.available_subtasks:
                if subtask.id_task == id:
                    self.model.status.available_subtasks.remove(subtask)
                    self.model.status.selected_subtasks.append(subtask)
                    self.model.status.current_power += subtask.weight
                    #break
                    return True
        #else:
        return False

    def move_subtask_to_available_list(self, id):
        if self.model.status.money > 0 and id != -1:
            for subtask in self.model.status.selected_subtasks:
                if subtask.id_subtask == id:
                    self.model.status.selected_subtasks.remove(subtask)
                    self.model.status.available_subtasks.append(subtask)
                    self.model.status.current_power -= subtask.weight
                    #break
                    return True
        #else:
        return False

    # Взаимодействие со спринтами
    def start_sprint(self):
        if self.model.status.money > 0 and self.model.status.users > 0 and self.model.status.loyal > 0:

            if self.model.status.current_power <= self.model.status.max_power:

                if self.model.status.selected_subtasks:
                    self.model.status.count_blank_sprint = 0
                    self.model.status.selected_subtasks = []
                else:
                    self.model.status.count_blank_sprint += 1

                for task in self.model.status.working_tasks:
                    if get_reward(task, self.model):
                        self.model.status.loyal += task.loyal
                        self.model.status.users += task.users

                self.model.status.number_sprint += 1
                self.model.status.money = increase_money(self.model)
                self.model.status.current_power = 0

                if self.model.status.count_blank_sprint > 1:
                    count_blank_sprint = self.model.status.count_blank_sprint
                    self.model.status.loyal = decrease_loyal(count_blank_sprint, self.model)
                    self.model.status.users = decrease_users(count_blank_sprint, self.model)
                return True
        #else:
        return False


# вспомогательные методы
def increase_money(model):
    cost_robot = 0
    if model.status.count_blank_sprint == 0:
        cost_robot = model.office.check_status_robot()*10000
    users = model.status.users
    loyal = model.status.loyal
    money = model.status.money
    debt = model.status.debt
    if debt > 0:
        k = min(9000, debt)
        model.status.debt -= k
    else:
        k = 0
    return int(money + loyal * users * 0.3 - k - cost_robot)


def decrease_loyal(count_blank_sprint, model):
    loyal = model.status.loyal
    return max(loyal - 0.05 * (count_blank_sprint - 1), 0)


def decrease_users(count_blank_sprint, model):
    users = model.status.users
    return max(users - 500 * (count_blank_sprint - 1), 0)


def get_reward(task, model):
    id_task = task.id_task
    for subtask in model.status.small_tasks:
        if subtask.id_task == id_task and not subtask.is_selected:
            return False
    return True
