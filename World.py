import pygame
from Exit_gate import *
from Platforms import *
from Enemy import *
from Coin import *


blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

#Dummy coin beside the score
score_coin = Coin(tile_size//2, tile_size//2)
coin_group.add(score_coin)

class World:
    def __init__(self, data):
        self.tile_list = []
        
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        # lava_img = pygame.image.load('img/lava.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count*tile_size, row_count*tile_size+15)
                    blob_group.add(blob)
                if tile == 4:   # Horizontol
                    platform = Platform(col_count*tile_size, row_count*tile_size, 1, 0) 
                    platform_group.add(platform)
                if tile == 5:   # Vertical
                    platform = Platform(col_count*tile_size, row_count*tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count*tile_size, row_count*tile_size+tile_size//2)
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count*tile_size + (tile_size // 2), row_count*tile_size + tile_size//2)
                    coin_group.add(coin)
                if tile == 8:
                    exi = Exit(col_count*tile_size, row_count*tile_size- (tile_size//2))
                    exit_group.add(exi)
                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1]) 