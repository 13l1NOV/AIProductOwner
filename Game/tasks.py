import pygame
from pygame.locals import Rect

from Game.button import Button


class Tasks:
    path = '../Game/Views'
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.game = game
        self.heading_font = pygame.font.SysFont("arial", 20)
        self.heading_font_bold = pygame.font.SysFont("arial", 20, True)

        self.game_tasks = pygame.image.load(self.path + '/Notebook.png').convert()
        self.game_tasks = pygame.transform.scale(self.game_tasks, (self.width/4, self.height/4*2))
        self.game.background_image.blit(self.game_tasks, (0, self.height / 4 ))

        self.init_button()
        #rec = pygame.Rect((200, 200, 200, 200))
        #pygame.draw.rect(self.game_bar, (255, 0, 0), rec)

        self.rect_tasks = Rect(10, 500, self.width / 1.5, self.height * 0.2)


    def update(self, model):
        self.set_data(model)
        self.update_data()

    def set_data(self, model):
        self.tasks = len(model.status.available_tasks)


    def update_data(self):
        self.label_tasks = self.heading_font.render("Тасков: " + str(self.tasks), True, (73, 168, 70))
        self.game.window.blit(self.label_tasks, self.rect_tasks)

    def init_button(self):
        button_sprint = Button(50, self.height / 10 * 7.5, "СПРИНТ", self.game.controller.start_sprint)
        button_create_tasks = Button(50, self.height / 10 * 1, "СОЗДАТЬ ТАСКИ", self.game.controller.create_two_easy_task)
        button_decomp = Button(50, self.height / 10 * 1.75, "ДЕКОМПОЗИРОВАТЬ", self.game.controller.decomposition_tasks)

        self.game.background_image.blit(button_sprint.buttonSurface, button_sprint.buttonRect)
        self.game.background_image.blit(button_decomp.buttonSurface, button_decomp.buttonRect)
        self.game.background_image.blit(button_create_tasks.buttonSurface, button_create_tasks.buttonRect)

        self.game.buttons.append(button_sprint)
        self.game.buttons.append(button_decomp)
        self.game.buttons.append(button_create_tasks)