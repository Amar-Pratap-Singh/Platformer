import pygame
tile_size = 50

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size*1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y