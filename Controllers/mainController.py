from Model.Robots.robot import Robot
from Model.Tasks.story import Story
from Model.Tasks.task import Task
import random


class Controller:

    def __init__(self, model):
        self.model = model
        self.max_sub = 8
        self.count_story = 0
        self.count_tasks = 0
        self.max_count_story = 6

    def start_release(self):
        for i in range(self.model.status.working_story.get_len()):
            story = self.model.status.working_story.get(i)
            if story is not None and story.isComplete:
                self.model.status.loyal = story.loyal
                self.model.status.users = story.users
                self.model.status.working_story.remove(i)

    def buy_robot(self):
        if self.model.status.money > 0:
            self.model.status.money -= self.model.office.cost_robot
            self.model.office.count_robot += 1
            self.model.status.max_power += 10
            return True
        return False

    def create_two_easy_task(self):
        if self.model.status.money > 0 and self.model.status.backlog.can_add(2):
            cost_tasks = 80000
            if cost_tasks <= self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.backlog.add(Story(self.count_story, 'S'))
                self.model.status.backlog.add(Story(self.count_story + 1, 'S'))
                self.count_story += 2
                return True
        return False

    def create_one_hard_task(self):
        if self.model.status.money > 0 and self.model.status.backlog.can_add(1):
            cost_tasks = 160000
            chance = random.randint(1, 100)
            if chance <= 25:
                typetask = 'M'
            elif 25 < chance <= 75:
                typetask = 'L'
            else:
                typetask = 'XL'
            if cost_tasks <= self.model.status.money:
                self.model.status.money -= cost_tasks
                self.model.status.backlog.add(Story(self.count_story, typetask))
                self.self.count_story += 1
                return True
        return False

    # =-================================
    def decomposition_tasks(self, index):  #
        if self.model.status.money > 0 and index >= 0 and index < self.max_count_story:
            if self.model.status.current_power + self.model.office.count_robot <= self.model.status.max_power:
                self.model.status.current_power += self.model.office.count_robot
                story = self.model.status.backlogg.get(index)
                if story is not None \
                        and self.model.status.working_story.can_add(1) \
                        and self.model.status.list_tasks.can_add(len(story.tasks)):
                    self.model.status.backlog.remove(story)
                    self.model.status.working_story.add(story)
                    for task in story.tasks:
                        self.model.status.list_tasks.add(task)
                    return True
        return False

    # Взаимодействие с подзадачами
    def select_task(self, index):
        if self.model.status.money > 0 and index >= 0:
            task = self.model.status.list_tasks.get(index)
            if task is not None and not task.isWorking:
                self.model.status.current_power += task.weight
                task.isWorking = True
                return True
        return False

    # def unselect_task(self, id): # не надо по идее
    #     if self.model.status.money > 0 and id != -1 and task.isWorking:
    #         task = self.model.status.list_tasks.get(id)
    #         if task.id_subtask == id:
    #             self.model.status.list_tasks.get(id).isWorking = False
    #             self.model.status.current_power -= task.weight
    #             # break
    #             return True
    #     # else:
    #     return False

    # =-================================
    # Взаимодействие со спринтами
    def start_sprint(self):
        if self.model.status.money > 0 and self.model.status.users > 0 and self.model.status.loyal > 0:

            if self.model.status.current_power <= self.model.status.max_power:

                if check_working_tasks():
                    self.model.status.count_blank_sprint = 0

                    remove = []
                    for i in range(self.model.status.working_story.get_len()):
                        story = self.model.status.working_story.get(i)
                        if story is not None:
                            for task in story.tasks: # возможно корявые проценты!!!
                                if task.isWorking:
                                    story.weight_complete += task.weight
                                    story.remove(task)
                                if not story.tasks:
                                    story.isComplete = True
                                remove.append(task)
                    for task in remove:
                        self.model.status.list_tasks.remove(task)
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


# def change_id_stories_in_backlog():
#     for story_id in range(len(self.model.status.backlog)):
#         self.model.status.backlog[id_story] = story_id
#         for task in self.model.status.backlog[id_story].tasks:
#             task.id_story = story_id

# def change_id_tasks():
#     clear_list_tasks = []
#     for story_id in range(len(self.model.status.working_story)):
#         clear_list_story = []
#         story = self.model.status.working_story[story_id]
#         for task_id in range(len(self.model.status.working_story[story_id].tasks)):
#             if not story.tasks[task_id].isWorking:
#                 clear_list_story.append(story[task_id])
#                 clear_list_tasks.append(story[task_id])
#         self.model.status.working_story[story_id] = clear_list_story
#     self.model.status.list_tasks = clear_list_tasks

def check_working_tasks():
    for i in range(self.model.status.list_tasks.get_len()):
        task = self.model.status.list_tasks.get(i)
        if task is not None and task.isWorking:
            return True
    return False
#
#
# def check_complete_story():
#     for story in self.model.status.working_story:
#         if story.isComplete:
#             return True
#     return False
