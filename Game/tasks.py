import pygame
import time
from pygame.locals import Rect
from Game.task import Task

from Model.Tasks import task as ModelTask

from Game.button import Button


class Tasks:
    path = '../Game/Views'
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.game = game
        self.heading_font = pygame.font.SysFont("arial", 20)
        self.heading_font_bold = pygame.font.SysFont("arial", 20, True)
        self.heading_small_font_bold = pygame.font.SysFont("arial", 16, True)

        self.game_tasks = pygame.image.load(self.path + '/Notebook.png').convert()
        self.game_tasks = pygame.transform.scale(self.game_tasks, (self.width/4, self.height/4*2))
        self.game.background_image.blit(self.game_tasks, (0, self.height / 4 ))

        self.game_tasks = pygame.image.load(self.path + '/Notebook.png').convert()
        self.game_tasks = pygame.transform.scale(self.game_tasks, (self.width / 4, self.height / 4 * 2))
        self.game.background_image.blit(self.game_tasks, (self.width * 0.75, self.height / 4))

        self.init_button()
        #rec = pygame.Rect((200, 200, 200, 200))
        #pygame.draw.rect(self.game_bar, (255, 0, 0), rec)

        self.rect_tasks = Rect(10, 500, self.width / 1.5, self.height * 0.2)


    def update(self, model):
        self.set_data(model)
        self.update_data()

    def set_data(self, model):
        self.view_small_tasks = model.status.small_tasks
        self.work_tasks = model.status.working_tasks


    def update_data(self):
        self.update_tasks_bar()
        self.update_tasks_button()

    def update_tasks_button(self):
        columnWidth = 4
        remove = []
        for t in self.task_buttons:
            remove_after_sprint = [t.subtask.id == small.id for small in self.view_small_tasks]
            if not any(remove_after_sprint):
                remove.append(t)
        for t in remove:
            self.task_buttons.remove(t)
            self.game.buttons.remove(t)

        for i, task in enumerate(self.view_small_tasks):
            task_button = None
            for t in self.task_buttons:
                if t.subtask.id == task.id:
                    task_button = t

            if task_button is None:
                #print("create TASK view id:" + str(task.id))
                task_button = Task(0, 0, task, self.move_task)
                self.task_buttons.append(task_button)
                self.game.buttons.append(task_button)

            x = (15 + (i % columnWidth) * (Task.width + 10))
            y = self.height / 10 * (3.15 + (i // columnWidth))
            task_button.updateButtonRect(x, y)
            if task.is_selected:
                task_button.select_this()

            self.game.window.blit(task_button.buttonSurface, task_button.buttonRect)

    def update_tasks_bar(self):
        x = self.width * 0.95
        y = self.height * 0.35
        for i, task in enumerate(self.work_tasks):
            color = Task.getColor(task.id_task)
            # task reward bar
            rec_reward = Rect(x - x / 5, y + i * 50 - 20, 100, 100)
            label_task_reward = self.heading_small_font_bold.render("Лояльность: " + str(task.loyal) + ", Пользователи: " + str(task.users), True, color)
            self.game.window.blit(label_task_reward, rec_reward)

            # task progress bar
            rec_bar = Rect(x - x / 5, y + i * 50, 100, 100)
            progress_task = self.heading_font_bold.render(self.get_bar(18, task.max_weight - task.weight, task.max_weight), True, color)
            self.game.window.blit(progress_task, rec_bar)

    def get_bar(self, max, current, target):
        x = int(min(1, current / target) * max)
        return ('▄'*x).ljust(max, '─')

    def move_task(self, task):
        self.game.controller.move_small_task_to_selected_list(task.subtask.id)


    def init_button(self):
        self.task_buttons = []
        button_sprint = Button(50, self.height / 10 * 7.5, "СПРИНТ", self.game.controller.start_sprint2)
        button_create_tasks = Button(50, self.height / 10 * 1, "СОЗДАТЬ ТАСКИ", self.game.controller.create_four_easy_task)
        button_decomp = Button(50, self.height / 10 * 1.75, "ДЕКОМПОЗИРОВАТЬ", self.game.controller.decomposition_tasks)

        self.game.background_image.blit(button_sprint.buttonSurface, button_sprint.buttonRect)
        self.game.background_image.blit(button_decomp.buttonSurface, button_decomp.buttonRect)
        self.game.background_image.blit(button_create_tasks.buttonSurface, button_create_tasks.buttonRect)

        self.game.buttons.append(button_sprint)
        self.game.buttons.append(button_decomp)
        self.game.buttons.append(button_create_tasks)