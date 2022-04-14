import pygame
from pygame import mixer
import pickle
from os import path
from sounds import *
from Buttons import *
from Players import *
from Exit_gate import *
from Platforms import *
from Enemy import *
from Coin import *
from World import *


pygame.mixer.pre_init(44100, -16, 2, 512)                   # mixer.pre_init(frequency of wave, size, channels, buffer)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 50

#GAME WINDOW
screen_width = 1000
screen_height = 1000          

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Super Mario')


#DEFINE FONT
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font_score_dis = pygame.font.SysFont('Bauhaus 93', 50)

#LOCAL GAME VARIABLES
tile_size = 50
game_over = 0                         # game_over = -1 --> Game is over, 0--> Game is running 
main_menu = True
level = 1
max_levels = 5
score = 0
x = 1         #x for changing bgd image

#DEFINE COLORS
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

#LOAD IMAGES
bg_img = pygame.image.load(f'img/sky{x}.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
sun_img = pygame.image.load('img/sun.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')


#TO DRAW TEXT ON SCREEN
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

 
# Function to reset level
def reset_level(level):
    player.reset(100, screen_height-130)        #(width, height)---> width: positive x-axis,  height: negative y-axis
    blob_group.empty()
    lava_group.empty()
    coin_group.empty()
    coin_group.add(score_coin)                   # Adding a dummy coin to be shown beside the score count
    exit_group.empty()
    platform_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        # world_data=[]
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world

player = Player(screen_width, screen_height-130)
player.reset(100, screen_height-130)

if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#Buttons
restart_button = Button(screen_width//2 - 50, screen_height//2 + 100, restart_img)
restart2_button = Button(screen_width - 130, 2, restart_img)
start_button = Button(screen_width//2 - 350, screen_height//2, start_img)
exit_button = Button(screen_width//2 + 150, screen_height//2, exit_img)

run = True
while (run):
    clock.tick(fps)
    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))
    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            pygame.mixer.music.play(-1, 0.0, 0)          
            main_menu = False

    
    else:  
        world.draw(screen)
        if game_over == 0:
            blob_group.update()
            platform_group.update()
            #update score
            #Check the collision b/w a coin and the palyer
            if pygame.sprite.spritecollide(player, coin_group, True):
                coin_fx.play()
                score += 1

            if restart2_button.draw():
                world_data = []
                world = reset_level(level)
                score = 0

            draw_text('X ' + str(score), font_score, white, tile_size-10, 18)
            draw_text(f'LEVEL {level}', font_score, white,screen_width//2 - 50, 18)
             

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        game_over = player.update(game_over, screen, world) 
            
        #if Player died
        if game_over == -1:
            draw_text('GAME OVER!', font, (255, 0, 0), screen_width//2 - 140, screen_height//2)
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0
        
        if game_over == 1:
            #Reset game and move to next level
            level += 1
            if x==1:
                x=2
            else: 
                x=1
            if level <= max_levels:
                bg_img = pygame.image.load(f'img/sky{x}.png')
                bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, (0,0,255),screen_width//2 -120, screen_height//2)
                draw_text(f'SCORE: {score}', font_score_dis, (255,255,255), screen_width//2 - 90, 12)
                #Restart game
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

                                                            # blit() where we have to add pictures
    for event in pygame.event.get():                # pygame.event contains events of diffrent types, like cross click, minimize click, mouse cursor 
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()