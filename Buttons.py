import pygame
screen_width = 1000
screen_height = 1000          

screen = pygame.display.set_mode((screen_width, screen_height))
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()

        #Check mouse and clicked cond
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            action = True
            self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            

        #Draw button
        screen.blit(self.image, self.rect)
        return action