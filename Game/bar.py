import pygame
from pygame.locals import Rect


class Bar:
    path = '../Game/Views'
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.game = game
        self.heading_font = pygame.font.SysFont("arial", 20)
        self.heading_font_bold = pygame.font.SysFont("arial", 20, True)

        self.game_bar = pygame.image.load(self.path + '/header.png').convert()
        self.game_bar = pygame.transform.scale(self.game_bar, (self.width, self.height/10))
        self.game.background_image.blit(self.game_bar, (0, 0))

        rec = pygame.Rect((200, 200, 200, 200))
        pygame.draw.rect(self.game_bar, (255, 0, 0), rec)


        self.init_base(self.game_bar)

    def init_base(self, bar):
        self.money = 0
        self.loyal = 0
        self.people = 0
        self.debet = 0
        self.progress = 0
        self.sprints = 1

        x = bar.get_width()
        y = bar.get_height()

        self.rect_money = Rect(x - x / 5, y / 4, self.width / 1.5, self.height * 0.2)
        self.rect_debet = Rect(x - x / 5, y / 2, self.width / 1.5, self.height * 0.2)
        self.rect_loyal = Rect(x / 20, y / 4, self.width / 1.5, self.height * 0.2)
        self.rect_people = Rect(x / 20, y / 2, self.width / 1.5, self.height * 0.2)

        self.rect_sprints = Rect(x / 4, y / 4, self.width / 1.5, self.height * 0.2)

        self.rect_target = Rect(x - x / 2.75, y / 4, self.width / 1.5, self.height * 0.2)
        self.rect_progress = Rect(x / 4, y / 2, self.width / 1.5, self.height * 0.2)

        self.label_money = self.heading_font.render("Денег: " + str(self.money) + "$", True, (73, 168, 70))
        self.game.window.blit(self.label_money, self.rect_money)

        self.label_loyal = self.heading_font.render("Лояльность: " + str(self.loyal), True, (73, 168, 70))
        self.game.window.blit(self.label_loyal, self.rect_loyal)

    def update(self, model):
        self.set_data(model)
        self.update_data()
        pygame.display.update()

    def set_data(self, model):
        self.money = model.status.money
        self.debet = model.status.debt
        self.loyal = model.status.loyal
        self.people = model.status.users
        self.target = model.status.target
        self.sprints = model.status.number_sprint

    def update_data(self):
        self.label_money = self.heading_font.render("Денег: " + str(self.money) + "$", True, (73, 168, 70))
        self.game.window.blit(self.label_money, self.rect_money)

        self.label_loyal = self.heading_font.render("Лояльность: " + str(self.loyal), True, (73, 168, 70))
        self.game.window.blit(self.label_loyal, self.rect_loyal)

        label_people = self.heading_font.render("Пользователи: " + str(self.people), True, (73, 168, 70))
        self.game.window.blit(label_people, self.rect_people)

        label_debet = self.heading_font.render("Долг: " + str(self.debet) + "$", True, (73, 168, 70))
        self.game.window.blit(label_debet, self.rect_debet)

        label_target = self.heading_font.render("Цель: " + str(self.target) + "$", True, (0, 0, 0))
        self.game.window.blit(label_target, self.rect_target)

        label_sprints = self.heading_font_bold.render("Спринты: " + str(self.sprints), True, (0, 0, 255))
        self.game.window.blit(label_sprints, self.rect_sprints)

        count = 60
        x = int((self.money / self.target) * count)
        label_progress = self.heading_font_bold.render(('▄'*x).ljust(count, '_'), True, (0, 0, 0))
        self.game.window.blit(label_progress, self.rect_progress)

        pygame.display.update()