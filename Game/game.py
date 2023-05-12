import pygame
import random
import sys
import math

from pygame import KEYDOWN, K_ESCAPE

from Game.bar import Bar
from Model.model import Model


class Game:

    path = '../Game/Views'
    def __init__(self):
        self.width = 1200
        self.height = 800

        self.model = Model()

        pass
        #self.window

    def init_window(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))#, pygame.FULLSCREEN)
        pygame.display.set_caption('My own little world')
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load(self.path+'/Background.jpg').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.bar = Bar(self.width, self.height, self.window)
        pygame.display.update()

    def game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = True
            self.window.blit(self.background_image, (0, 0))
            #pygame.display.update()
            self.clock.tick(60)
            self.bar.update(self.model)

    def update_model(self, model):
        pass

    def start(self):
        self.init_window()
        self.update_model(Model())
        self.game()