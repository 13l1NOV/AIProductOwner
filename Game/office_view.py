import pygame


class Office_View:
    path = '../Game/Views'

    def __init__(self, width, height, game):
        self.count_robots = [0, 0, 0, 0, 0, 0, 0, 0]
        self.heading_font = pygame.font.SysFont("arial", 20)

        self.width = width
        self.height = height
        self.game = game
        self.room_x = 270
        self.room_y = 100
        self.room1 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room1, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room2 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room2, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room3 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room3, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room4 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room4, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room5 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room5, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room6 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room6, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room7 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room7, (255, 255, 255), (0, 0, self.room_x, self.room_y))
        self.room8 = pygame.Surface((self.room_x, self.room_y))
        pygame.draw.rect(self.room8, (255, 255, 255), (0, 0, self.room_x, self.room_y))

        self.office_image = pygame.image.load(self.path + '/office.png').convert()
        self.office_image = pygame.transform.scale(self.office_image, (self.width // 2, self.height // 1.5))
        self.x = self.width // 2 - self.office_image.get_width() // 2
        self.y = self.height - self.office_image.get_height()

        self.draw_rooms()
        self.game.background_image.blit(self.office_image, (self.x, self.y))
        pygame.display.update()

    def update(self, model):
        self.update_data(model)
        pygame.display.update()

    def update_data(self, model):
        sx = 420
        sy = 310
        space_x = 20
        space_y = 10
        office = model.office.list_rooms
        for i in range(len(office)):
            self.count_robots[i] = office[i].count_robots

        label = self.heading_font.render("роботов: " + str(self.count_robots[7]), True, (73, 168, 70))
        self.game.window.blit(label, (sx, sy))

        label = self.heading_font.render("роботов: " + str(self.count_robots[6]), True, (73, 168, 70))
        self.game.window.blit(label, (sx+self.room_x+space_x, sy))

        label = self.heading_font.render("роботов: " + str(self.count_robots[5]), True, (73, 168, 70))
        self.game.window.blit(label, (sx, sy+self.room_y+space_y))

        label = self.heading_font.render("роботов: " + str(self.count_robots[4]), True, (73, 168, 70))
        self.game.window.blit(label, (sx+self.room_x+space_x, sy+self.room_y+space_y))

        label = self.heading_font.render("роботов: " + str(self.count_robots[3]), True, (73, 168, 70))
        self.game.window.blit(label, (sx, sy+2*self.room_y+space_y+space_y))

        label = self.heading_font.render("роботов: " + str(self.count_robots[2]), True, (73, 168, 70))
        self.game.window.blit(label, (sx+self.room_x +space_x, sy+2*self.room_y+space_y))

        label = self.heading_font.render("роботов: " + str(self.count_robots[1]), True, (73, 168, 70))
        self.game.window.blit(label, (sx, sy+3*self.room_y+space_y))

        label = self.heading_font.render("роботов: " + str(self.count_robots[0]), True, (73, 168, 70))
        self.game.window.blit(label, (sx+self.room_x+space_x, sy+3*self.room_y+space_y))

    def draw_rooms(self):
        left_x = 25
        up_y = 8
        space_x = 20
        space_y = 10
        self.office_image.blit(self.room8, (left_x, up_y))
        self.office_image.blit(self.room7, (20 + self.room_x + space_x, up_y))
        self.office_image.blit(self.room6, (left_x, up_y + space_y + self.room_y))
        self.office_image.blit(self.room5, (20 + self.room_x + space_x, up_y + space_y + self.room_y))
        self.office_image.blit(self.room4, (left_x, space_y + 2 * (up_y + self.room_y)))
        self.office_image.blit(self.room3, (20 + self.room_x + space_x, space_y + 2 * (up_y + self.room_y)))
        self.office_image.blit(self.room2, (left_x, space_y + 3 * (up_y + self.room_y)))
        self.office_image.blit(self.room1, (20 + self.room_x + space_x, space_y + 3 * (up_y + self.room_y)))
