import pygame
import pickle
from os import path
import sounds
from World import *


class Player():
    def __init__(self, x, y):
        self.reset(x, y)        

    def update(self, game_over, screen, world):
        dx = 0
        dy = 0
        walk_cooldown = 2   # variable to allow player to move 
        col_thresh = 20

        if game_over == 0:
            # key presses
            key = pygame.key.get_pressed()


            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:       
                sounds.jump_fx.play()
                self.vel_y = -22
                self.jumped = True

            if key[pygame.K_SPACE] == False:      
                self.jumped = False

            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1

            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1 or self.direction == 0:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


    # Handling animations
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


    #Adding gravity
            self.vel_y += 2
            if (self.vel_y > 10):
                self.vel_y = 10
                        
            dy += self.vel_y
                
            # Check for collision
            self.in_air = True
            for tile in world.tile_list:
                # Check for collision in x-direction 
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0


                # Check for collision in y-direction --> jumping or falling
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #Collision while jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #Collision while falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0  
                        self.in_air = False

            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                sounds.game_over_fx.play()
                game_over = -1

            # Check for collision with Lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                sounds.game_over_fx.play()

            
            # Check for collision with Exit Gate
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
                sounds.you_win_fx.play()

            #Check for collision with platforms
            for platform in platform_group:
                #Check for the collision with x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #CHeck for collision in y-direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #Check if below platform
                    
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                        
                    #Check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0

                    #Move sideways along with the platform
                    if platform.move_x == 1:
                        self.rect.x += platform.move_direction



            #Update player coordinates
            self.rect.x += dx
            self.rect.y += dy
            # if self.rect.bottom > screen_height:
            #     self.rect.bottom = screen_height 
            #     dy = 0 

        elif game_over == -1:
            self.image = self.dead_image
            self.rect.y -= 15
#Draw player on screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0        #Speed of the animation

        for num in range(1,5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)           # pygame.transform.flip(image, flip abt y-axis, flip abt x -axis)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False 
        self.direction = 0
        self.in_air = True