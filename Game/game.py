import pygame
import random
import sys
import math


from pygame import KEYDOWN, K_ESCAPE

from Controllers.mainController import Controller
from Game.bar import Bar
from Game.office_view import Office_View
from Game.tasks import Tasks
from Model.model import Model


class Game:

    path = '../Game/Views'
    def __init__(self):
        self.width = 1200
        self.height = 800

        self.buttons = []
        self.model = Model()
        self.controller = Controller(self.model)

        #self.window

    def init_window(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        pygame.display.set_caption('Product Owner AI')
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load(self.path+'/Background.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.bar = Bar(self.width, self.height, self)
        self.tasks = Tasks(self.width, self.height, self)
        #self.window.blit(self.background_image, (0, 0))
        self.bar = Bar(self.width, self.height, self)

        self.init_office()

        self.window.blit(self.background_image, (0, 0))
        pygame.display.update()

    def init_office(self):
        self.office = Office_View(self.width, self.height, self)

    def game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True
            for button in self.buttons:
                button.process()
            #self.window.blit(self.background_image, (0, 0))
            #pygame.display.update()

            self.window.blit(self.background_image, (0, 0)) # прошлое окно перересовывается пустым

            self.office.update(self.model)
            self.bar.update(self.model)
            self.tasks.update(self.model)

            pygame.display.update() # обновляем все изменения
            self.clock.tick(30)
    def update_model(self, model):
        pass

    def start(self):
        self.init_window()
        self.update_model(Model())
        self.game()