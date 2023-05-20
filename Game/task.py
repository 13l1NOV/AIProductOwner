import pygame

class Task():
    width = 60
    height = 60
    def __init__(self, x, y, task, onclickFunction=None):
        self.subtask = task
        self.color = Task.getColor(self.subtask.id_story)

        self.x = x
        self.y = y
        self.width = Task.width
        self.height = Task.height
        self.font = pygame.font.SysFont("arial", 20, True)

        self.onclickFunction = onclickFunction
        self.alreadyPressed = False

        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonSurface2 = pygame.Surface((self.width * 1.5, self.height * 1.5))
        self.buttonSurface.fill(self.color)

        self.drawWeigth()

    def updateButtonRect(self, x, y):
        self.x = x
        self.y = y
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

    def select_this(self):
        self.buttonSurface.fill((25, 25, 25))
        self.buttonSurface.fill(self.color, (self.width * 0.1, self.height * 0.1, self.width * 0.8, self.height * 0.8))
        self.drawWeigth()

    def drawWeigth(self):
        self.buttonSurf = self.font.render(str(self.subtask.weight), True, (0, 0, 0))
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])

    def process(self):
        mousePos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0]:

                if not self.alreadyPressed:
                    self.onclickFunction(self)
                self.alreadyPressed = True
            else:
                self.alreadyPressed = False

    def getColor(id):

        r = 100 + ((id * 53) % 55)
        g = 100 + ((id * 17) % 155)
        b = 100 + (100 + id * 83) % 155
        return (r, g, b)