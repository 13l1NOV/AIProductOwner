import pygame
from pygame.locals import Rect


class Bar:

    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.window = window
        self.heading_font = pygame.font.SysFont("arial", 20)
        self.rect_bar = Rect(0, 0, self.width / 1.5, self.height*0.2)
        pygame.draw.rect(self.window, (255, 255, 0), self.rect_bar)
        pygame.display.update()
        self.init_money()

    def init_money(self):
        self.money = 0
        self.rect_money = Rect(0, 0, self.width / 1.5, self.height*0.2)

    def update(self, model):
        self.set_data(model)
        self.update_data()
        pygame.display.update()

    def set_data(self, model):
        self.money = model.status.money

    def update_data(self):
        label = self.heading_font.render("Денег: " + str(self.money) + "$", True, (73, 168, 70))
        self.window.blit(label, self.rect_money)