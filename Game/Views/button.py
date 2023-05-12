import pygame


class Button():
    def __init__(self, x, y, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = 200
        self.height = 50
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.SysFont("arial", 20, True)
        self.buttonSurface.fill((195, 25, 124))
        self.buttonSurf = self.font.render(buttonText, True, (255, 255, 255))

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])

    def process(self):
        #self.buttonSurface.fill(self.fillColors['hover'])

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            #self.buttonSurface.fill(self.fillColors['pressed'])

            if not self.alreadyPressed:
                self.onclickFunction()
            self.alreadyPressed = True
        else:
            self.alreadyPressed = False