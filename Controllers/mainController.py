from Model.Robots.robot import Robot
from Model.Tasks.story import Story
from Model.Tasks.task import Task
import random


class Controller:

    def __init__(self, model):
        self.model = model
        self.max_sub = 8

    def start_release(self):
        if check_complete_story():
            self.model.status.working_story = get_reward()

    # Взаимодействие с офисом
    def buy_robot(self):
        if self.model.status.money > 0:
            self.model.status.money -= self.model.office.cost_robot
            self.model.office.count_robot += 1
            self.model.status.max_power += 10
            return True
        return False

    # Взаимодействие с тасками
    def create_two_easy_task(self):
        if self.model.status.money > 0 and len(self.model.status.backlog < 5):
            cost_tasks = 80000
            if cost_tasks < self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.backlog.append(Story(len(self.model.status.backlog), 'S'))
                self.model.status.backlog.append(Story(len(self.model.status.backlog), 'S'))
                return True
        return False

    def create_one_hard_task(self):
        if self.model.status.money > 0 and len(self.model.status.backlog < 6):
            cost_tasks = 160000
            chance = random.randint(1, 100)
            if chance <= 25:
                typetask = 'M'
            elif 25 < chance <= 75:
                typetask = 'L'
            else:
                typetask = 'XL'
            if cost_tasks < self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.backlog.append(Story(len(self.model.status.backlog), typetask))
                self.counter_id += 1
                return True
        return False

    def decomposition_tasks(self, index):  #
        if self.model.status.money > 0 and index >= 0:
            if self.model.status.current_power + self.model.office.count_robot <= self.model.status.max_power:
                self.model.status.current_power += self.model.office.count_robot
                story = self.model.status.backlog.pop(index)
                change_id_stories_in_backlog()
                for task in story.tasks:
                    self.model.status.list_tasks.append(task)   #!@#!@#!@#
                    task.id = len(self.model.status.list_tasks) #!@#!@#!@#
                return True
        return False

    # Взаимодействие с подзадачами
    def select_task(self, index):
        if self.model.status.money > 0 and index >= 0:
            task = self.model.status.list_tasks[index]
            if not task.isWorking:
                self.model.status.current_power += task.weight
                task.isWorking = True
                return True
        return False

    def unselect_task(self, id): # не надо по идее
        task = self.model.status.list_tasks[id]
        if self.model.status.money > 0 and id != -1 and task.isWorking:
            if task.id_subtask == id:
                self.model.status.list_tasks[id].isWorking = False
                self.model.status.current_power -= task.weight
                # break
                return True
        # else:
        return False

    # Взаимодействие со спринтами
    def start_sprint(self):
        if self.model.status.money > 0 and self.model.status.users > 0 and self.model.status.loyal > 0:

            if self.model.status.current_power <= self.model.status.max_power:

                if check_working_tasks():
                    self.model.status.count_blank_sprint = 0
                    for story in self.model.status.working_story:
                        if not story.tasks:
                            story.isComplete = True
                        else:
                            for task in story.tasks: # возможно корявые проценты!!!
                                if task.isWorking:
                                    story.percent_complete += task.part_percent
                            change_id_tasks()
                else:
                    self.model.status.count_blank_sprint += 1
                self.model.status.number_sprint += 1
                self.model.status.money = increase_money(self.model)
                self.model.status.current_power = 0

                if self.model.status.count_blank_sprint > 1:
                    count_blank_sprint = self.model.status.count_blank_sprint
                    self.model.status.loyal = decrease_loyal(count_blank_sprint, self.model)
                    self.model.status.users = decrease_users(count_blank_sprint, self.model)
                return True
        # else:
        return False


# вспомогательные методы
def increase_money(model):
    cost_robot = 0
    if model.status.count_blank_sprint == 0:
        cost_robot = model.office.check_status_robot() * 10000
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


def get_reward():
    clear_list = []
    for story in self.model.status.working_story:
        if story.isComplete:
            self.model.status.loyal = story.loyal
            self.model.status.users = story.users
        else:
            clear_list.append(story)
    return clear_list


def change_id_stories_in_backlog():
    for story_id in range(len(self.model.status.backlog)):
        self.model.status.backlog[id_story] = story_id
        for task in self.model.status.backlog[id_story].tasks:
            task.id_story = story_id

def change_id_tasks():
    clear_list_tasks = []
    for story_id in range(len(self.model.status.working_story)):
        clear_list_story = []
        story = self.model.status.working_story[story_id]
        for task_id in range(len(self.model.status.working_story[story_id].tasks)):
            if not story.tasks[task_id].isWorking:
                clear_list_story.append(story[task_id])
                clear_list_tasks.append(story[task_id])
        self.model.status.working_story[story_id] = clear_list_story
    self.model.status.list_tasks = clear_list_tasks

def check_working_tasks():
    for task in self.model.status.list_tasks:
        if task.isWorking:
            return True
    return False


def check_complete_story():
    for story in self.model.status.working_story:
        if story.isComplete:
            return True
    return False
