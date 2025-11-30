import pygame
import math
import numpy as np
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#Screen dimensions
screen_width = 1024
screen_height = 576
screen_rect = (screen_width, screen_height)

#display
screen = pygame.display.set_mode(screen_rect)

#load fonts
text_font = pygame.font.Font("Retro Gaming.ttf", 30)

#load images
Menu_Select_Arrow = pygame.image.load('Menu_Select_Arrow.png')



#load sounds
Menu_Select_Sound = pygame.mixer.Sound('Menu_Select.wav')
Menu_Select_Sound.set_volume(0.75)

#helper function for drawing text to the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center = (x, y))
    screen.blit(img, rect)

#helper function for drawing an image to the screen from a file
#only updates the part of the screen containing the image
def draw_image(name, x, y, update):
    image = name
    image_rect = image.get_rect(center = (x, y))
    screen.blit(image, (x, y))
    if update:
        pygame.display.update(image_rect)
    else:
        pygame.display.flip()

#helper function for filling a rect with a color
#updates the area of the screen filled by the rect
def draw_rect(width, height, x, y, color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect)
    pygame.display.update(rect)

#cutscene function that uses the draw_image function
#will probably implement later but focusing on gameplay for now
#def cutscene(time, image_name, x, y, update):


#defining variables

#1 = 1 player, 2 = 2 player. This variable is for 1 or 2 player selection.
game_mode = 0

#game loop
running = True
start = True
player_select = False
waiting = True
playing = True

#frame rate stuff
FPS = 120
clock = pygame.time.Clock()


#main loop
while running:

    #start screen
    while start:

        #use the pygame text function to display the start menu text
        draw_text("Deflection", text_font, (5, 21, 214), screen_width / 2, screen_height / 2)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                    player_select = True
                    Menu_Select_Sound.play()




    screen.fill((0, 0, 0))
    pygame.display.flip()

    #1 or 2 player selection menu
    while player_select:

        #draws the text for the menu
        draw_text("1 Player", text_font, (5, 21, 214), screen_width / 2, screen_height / 2)
        draw_text("2 Player", text_font, (5, 21, 214), screen_width / 2, screen_height / 2 + 100)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start = False
                player_select = False
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    #select 2 player
                    draw_image(Menu_Select_Arrow, 300, 260, True)
                    draw_rect(50, 50, 300, 360, (0,0,0))
                    Menu_Select_Sound.play()
                    game_mode = 1
                    print(game_mode)
                if event.key == pygame.K_DOWN:
                    #select 1 player
                    draw_image(Menu_Select_Arrow, 300, 360, True)
                    draw_rect(50, 50, 300, 260, (0, 0, 0))
                    Menu_Select_Sound.play()
                    game_mode = 2
                    print(game_mode)
                if event.key == pygame.K_RETURN and game_mode > 0:
                    player_select = False

    if game_mode == 1 and waiting and running:
        screen.fill((0,0,0))
        draw_text("Player 1: AWD for directions, G to deflect.", text_font, (5, 21, 214), screen_width / 2, screen_height / 2)
        pygame.display.flip()
        Menu_Select_Sound.play()
        print("play")
        waiting = False
        playing = True
        pygame.time.delay(3000)
    if game_mode == 2 and waiting and running:
        screen.fill((0, 0, 0))
        draw_text("Player 1: WSD for directions, G to deflect.", text_font, (5, 21, 214), screen_width / 2, screen_height / 2 - 50)
        draw_text("Player 2: Arrows for directions, ctrl to deflect.", text_font, (5, 21, 214), screen_width / 2, screen_height / 2 + 50)
        pygame.display.flip()
        Menu_Select_Sound.play()
        print("play")
        waiting = False
        playing = True
        pygame.time.delay(3000)

    screen.fill((0,0,0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    while playing:
        #limit to 120 FPS
        clock.tick(FPS)

        #user input for directions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start = False
                player_select = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    #turn player one up
                    print("Left")
                    draw_image()
                if event.key == pygame.K_d:
                    #turn player one to the right
                    print("Forward")
                if event.key == pygame.K_s:
                    #turn player one down
                    print("Right")











