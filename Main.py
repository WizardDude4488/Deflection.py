import pygame
import math
import numpy as np
from pygame import mixer
import random

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
menu_font = pygame.font.Font("Retro Gaming.ttf", 30)
game_font = pygame.font.Font("Retro Gaming.ttf", 15)


#load images
Menu_Select_Arrow = pygame.image.load('Menu_Select_Arrow.png')

Small_Arrow_Left = pygame.image.load('Small_Arrow_Left.png')
Small_Arrow_Up = pygame.image.load('Small_Arrow_Up.png')
Small_Arrow_Right = pygame.image.load('Small_Arrow_Right.png')
Small_Arrow_Down = pygame.image.load('Small_Arrow_Down.png')

Horizontal_Deflect_Bar = pygame.image.load('Horizontal_Deflect_Bar.png')
Vertical_Deflect_Bar = pygame.image.load('Vertical_Deflect_Bar.png')



#load sounds
Menu_Select_Sound = pygame.mixer.Sound('Menu_Select.wav')
Menu_Select_Sound.set_volume(0.75)

#helper function for drawing text to the screen
def draw_text(text, font, text_col, x, y, bg_color):
    img = font.render(text, True, text_col)
    rect = img.get_rect(center = (x, y))
    pygame.draw.rect(screen, bg_color, rect)
    screen.blit(img, rect)
    pygame.display.update(rect)

#helper function for drawing an image to the screen from a file
#only updates the part of the screen containing the image
def draw_image(image, x, y, update):
    image_rect = image.get_rect(center = (x,y))
    if update:
        pygame.draw.rect(screen, (0,0,0), image_rect)
        screen.blit(image, image_rect)
        pygame.display.update(image_rect)
    else:
        screen.blit(image, image_rect)
        pygame.display.flip()

#helper function for filling a rect with a color
#updates the area of the screen filled by the rect
#change these helper functions so that they are x, y, width, height, like the pygame built in methods
def draw_rect(width, height, x, y, color):
    rect = pygame.Rect(x, y, width, height)
    rect.center = (x, y)
    pygame.draw.rect(screen, color, rect)
    pygame.display.update(rect)

def draw_with_rect(rect, color):
    pygame.draw.rect(screen, color, rect)
    pygame.display.update(rect)

def clear_image(image, x, y, color, centered):
    match centered:
        case True:
            image_rect = image.get_rect(center = (x, y))
        case False:
            image_rect =image.get_rect()

    pygame.draw.rect(screen, color, image_rect)
    pygame.display.update(image_rect)

#player variables
player_1_direction = ""
player_1_deflection = ""
player_2_direction = ""
player_2_deflection = ""

#globals for player 1 and 2 x and y positions
#make sure to create player objects after variable declaration so interpreter knows what value to assign for the new object's parameters
player_1_x = screen_width // 2
player_1_y = 35 + 50

player_2_x = screen_width // 2
player_2_y = screen_height - 35 - 50

#creating the rects for the different objects in the game that the particles can collide with
#added a little bit of buffer so it's more forgiving for the players
#used floor division to make sure all values are of type integer, not floats
#player 1
player_1_rect = pygame.Rect(player_1_x, player_1_y, 50, 50)
player_1_rect.center = (player_1_x, player_1_y)
player_1_left_rect = pygame.Rect(player_1_x - 30, player_1_y, 10, 44)
player_1_left_rect.center = (player_1_x - 30, player_1_y)
player_1_down_rect = pygame.Rect(player_1_x, player_1_y + 30, 44, 10)
player_1_down_rect.center = (player_1_x, player_1_y + 30)
player_1_right_rect = pygame.Rect(player_1_x + 30, player_1_y, 10, 44)
player_1_right_rect.center = (player_1_x + 30, player_1_y)

#player 2
player_2_rect = pygame.Rect(player_2_x, player_2_y, 50, 50)
player_2_rect.center = (player_2_x, player_2_y)
player_2_left_rect = pygame.Rect(player_2_x - 30, player_2_y, 10, 44)
player_2_left_rect.center = (player_2_x - 30, player_2_y)
player_2_up_rect = pygame.Rect(player_2_x, player_2_y - 30, 44, 10)
player_2_up_rect.center = (player_2_x, player_2_y - 30)
player_2_right_rect = pygame.Rect(player_2_x + 30, player_2_y, 10, 44)
player_2_right_rect.center = (player_2_x + 30, player_2_y)

#walls
#remember the first pixel is 0, not 1
wall_left_rect = pygame.Rect(2, screen_height // 2, 5, screen_height - 100)
wall_left_rect.center = (2, screen_height // 2)
wall_top_rect = pygame.Rect(screen_width // 2, 49, screen_width, 5)
wall_top_rect.center = (screen_width // 2, 49)
wall_bottom_rect = pygame.Rect(screen_width // 2, screen_height - 50, screen_width, 5)
wall_bottom_rect.center = (screen_width // 2, screen_height - 50)
wall_right_rect = pygame.Rect(screen_width - 3, screen_height // 2, 5, screen_height - 100)
wall_right_rect.center = (screen_width - 3, screen_height // 2)

collideable_list = [player_1_rect, player_1_left_rect, player_1_right_rect, player_1_down_rect,
                    player_2_rect, player_2_left_rect, player_2_right_rect, player_2_up_rect,
                    wall_left_rect, wall_top_rect, wall_bottom_rect, wall_right_rect]

#player life values

player_1_dead = False
player_1_score = 0
player_2_dead = False
player_2_score = 0


#classes for player functions like checking whether a deflection bar should be displaying on a certain frame

class Player1:
    def __init__(self, player_x, player_y):
        self.frame = 0
        self.player_x = player_x
        self.player_y = player_y
        self.score_x = 0 + 49
        self.score_y = 0 + 25

    def check_bar_for_frame(self):
        if self.frame == 0.4 * FPS:
            global player_1_deflection
            print(player_1_deflection)
            player_1_deflection = ""
            self.frame = 0
            #this clears out any graphical remains of the deflection bars
            draw_rect(4, 44, self.player_x + 30, self.player_y, (0, 0, 0))
            draw_rect(4, 44, self.player_x - 30, self.player_y, (0, 0, 0))
            draw_rect(44, 4, self.player_x, self.player_y + 30, (0, 0, 0))
        else:
            self.frame += 1
    def print_score(self):
        global player_1_score
        draw_text("Score:" + " " + str(player_1_score), game_font, (5, 21, 214), self.score_x, self.score_y, (0,0,0))


class Player2:
    def __init__(self, player_x, player_y):
        self.frame = 0
        self.player_x = player_x
        self.player_y = player_y
        self.score_x = 0 + 49
        self.score_y = screen_height - 25

    def check_bar_for_frame(self):
        if self.frame == 0.4 * FPS:
            global player_2_deflection
            player_2_deflection = ""
            self.frame = 0
            # this clears out any graphical remains of the deflection bars
            clear_image(Vertical_Deflect_Bar, self.player_x + 30, self.player_y, (0, 0, 0), True)
            clear_image(Vertical_Deflect_Bar, self.player_x - 30, self.player_y, (0, 0, 0), True)
            clear_image(Horizontal_Deflect_Bar, self.player_x, self.player_y - 30, (0,0,0), True)
        else:
            self.frame += 1
    def print_score(self):
        global player_1_score
        draw_text("Score:" + " " + str(player_1_score), game_font, (5, 21, 214), self.score_x, self.score_y, (0,0,0))


#class for managing the list of particles
class Particles:
    class Particle:
        def __init__(self, pos_x, pos_y, vel_x, vel_y, radius):
            self.pos_x, self.pos_y, self.vel_x, self.vel_y, self.radius = pos_x, pos_y, vel_x, vel_y, radius
            self.rect = pygame.Rect(pos_x, pos_y, 2 * radius, 2 * radius)
            self.rect.center = (pos_x, pos_y)
            self.damaged = False
            self.delete = False
            self.color = (5, 21, 214)
            pygame.draw.circle(screen, (1,1,1), (self.pos_x, self.pos_y), self.radius)
            pygame.display.update(self.rect)
        def move(self):
            #draw over the previous position with black
            draw_with_rect(self.rect, (0,0,0))
            #update position based on velocity
            self.pos_x = self.pos_x + self.vel_x
            self.pos_y = self.pos_y + self.vel_y
            #update rect
            #
            self.rect = pygame.Rect(self.pos_x, self.pos_y, 2 * self.radius, 2 * self.radius)
            #draw new rectangle and update the area of its rect
            draw_with_rect(self.rect, self.color)
            pygame.display.update(self.rect)
        def check_collision(self):
            global player_1_deflection
            # put the list for the collideable objects here
            match self.rect.collidelist(collideable_list):
                case 0:
                    global player_1_dead
                    global player_1_score
                    match self.damaged:
                        case False:
                            player_1_dead = True
                            print("Player 1 Dead:", player_1_dead)
                            self.delete = True
                        #if the game doesn't stop because of the player death, a new particle won't be spawned to take this particles place because the specific particle that killed the player can possibly pass through the bound of the map and be in the player's rect at the same time, which leads to the particle not being despawned
                        #maybe add another if statement just for deleting particles that are out of bounds, but add it before the switch case statement so the particle isn't deleted before it can be checked for collision
                        #damaged particles become coins that you can collect for score
                        case True:
                            player_1_score += 1
                            player_1.print_score()
                            self.delete = True

                case 1:
                    if player_1_deflection == "Left":
                        # flip x-velocity and offset by 5 - 8 pixels
                        self.pos_x = self.pos_x - random.randint(5, 8)
                        self.vel_x = -self.vel_x
                        if self.damaged:
                            # I think this might cause issues because this would create an empty indice in the particles list which the check_list function in the outer class would try to use its respective .move() etc methods on which is incorrect and would produce an error since there is no longer an object in that list indice
                            # Could solve this by having a while loop that removes any empty entries from the list before checking for collisions and moving, which would prevent any other possible problems of this type as well
                            self.delete = True
                        else:
                            # make the particle red to represent it being damaged
                            #convert to gold color
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 2:
                    if player_1_deflection == "Right":
                        # flip x-velocity
                        self.pos_x = self.pos_x + random.randint(5, 8)
                        self.vel_x = -self.vel_x
                        if self.damaged:
                            self.delete = True
                        else:
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 3:
                    if player_1_deflection == "Down":
                        # flip y-velocity
                        self.pos_y = self.pos_y + random.randint(5, 8)
                        self.vel_y = -self.vel_y
                        if self.damaged:
                            self.delete = True
                        else:
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 4:
                    global player_2_dead
                    global player_2_score
                    match self.damaged:
                        case False:
                            player_2_dead = True
                            print("Player 2 Dead:", player_2_dead)
                            self.delete = True
                        # if the game doesn't stop because of the player death, a new particle won't be spawned to take this particles place because the specific particle that killed the player can possibly pass through the bound of the map and be in the player's rect at the same time, which leads to the particle not being despawned
                        # maybe add another if statement just for deleting particles that are out of bounds, but add it before the switch case statement so the particle isn't deleted before it can be checked for collision
                        # damaged particles become coins that you can collect for score
                        case True:
                            player_2_score += 1
                            player_2.print_score()
                            self.delete = True
                case 5:
                    if player_2_deflection == "Left":
                        # flip x-velocity
                        self.pos_x = self.pos_x - random.randint(5, 8)
                        self.vel_x = -self.vel_x
                        if self.damaged:
                            self.delete = True
                        else:
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 6:
                    if player_2_deflection == "Right":
                        #flip x-velocity
                        self.pos_x = self.pos_x + random.randint(5, 8)
                        self.vel_x = -self.vel_x
                        if self.damaged:
                            self.delete = True
                        else:
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 7:
                    if player_2_deflection == "Up":
                        # flip y-velocity
                        self.pos_y = self.pos_y - random.randint(5, 8)
                        self.vel_y = -self.vel_y
                        if self.damaged:
                            self.delete = True
                        else:
                            self.color = (255, 215, 0)
                            self.damaged = True
                case 8:
                    # random numbers create varying particle paths for better gameplay
                    self.pos_x = self.pos_x + random.randint(3, 7)
                    self.vel_x = -self.vel_x
                case 9:
                    self.pos_y = self.pos_y + random.randint(3, 7)
                    self.vel_y = -self.vel_y
                case 10:
                    self.pos_y = self.pos_y - random.randint(3, 7)
                    self.vel_y = -self.vel_y
                case 11:
                    self.pos_x = self.pos_x - random.randint(3, 7)
                    self.vel_x = -self.vel_x

            # check if particle is out of bounds, if so, delete
            if self.rect.x == 0 + 1 or self.rect.y == 0 + 1 or self.rect.x == screen_width - 1 or self.rect.y == screen_height - 1:
                self.delete = True

            # deletion statement at end so code doesn't try to reference itself when it doesn't exist
            if self.delete:
                del self
    def __init__(self):
        self.list = []
        self.frame = 0
    def spawn_particle(self):
        #I think this should append a new particle to the list in the outer class, but it doesn't appear to be working
        #When it works, I should be able to reference each of the particles by their index in the list found in the outer class, rather than having to reference each by a unique name
        #I could also try using a dictionary instead, but I think this is better since I'll be able to iterate through the list with a for loop using simple integer iteration
        random_velocities = [-1, 1]
        if self.frame == 120:
            particle = Particles.Particle(screen_width / 2, screen_height / 2, random.choice(random_velocities), random.choice(random_velocities), 5)
            if len(self.list) < 7:
                self.list.append(particle)
            self.frame = 0
        else:
            self.frame += 1

    def check_list(self):
        index = 0
        while index < len(self.list):
            #check collisions for item in list, then move the item using the move() method
            #this is intended to be called every frame
            #self.list[i] accesses the object at that index
            #need to access the index in the list in the for loop rather than the object, because pop() only works on items in a list, not objects
            self.list[index].check_collision()

            #this prevents the code from deleting an item from the list then trying to use .move() on the deleted indice, which would no longer exist
            if self.list[index].delete:
                # draw another black rectangle over the position to prevent uncleared rectangles from remaining at the locations where the particles got removed from the list for being out of bounds
                draw_with_rect(self.list[index].rect, (0, 0, 0))
                pygame.display.update(self.list[index].rect)
                del self.list[index]
            else:
                self.list[index].move()
            index += 1
    def get_list(self):
        #function that returns the list of particles with component positions and velocities

        index = 0
        #empty list that has the particles and their data added to it
        tracking_list = []

        while index < len(self.list):
            x = self.list[index].pos_x
            y = self.list[index].pos_y
            Vx = self.list[index].vel_x
            Vy = self.list[index].vel_y
            #null values (implemented using "None" in python) are added to have the correct list size for reassignment during the npc's protect_self method
            entry = [x, y, Vx, Vy, None, None]

            tracking_list.append(entry)
            index += 1

        return(tracking_list)



            #we can just assume that all the surfaces in the game can only be collided with horizontaly or vertically, not both, so this should make things easier.


class npc:
    def __init__(self):
        self.pos_x = player_2_x
        self.pos_y = player_2_y
        self.rect = player_2_rect
        #could add a difficulty attribute here that would be set by the player upon starting the 1 player mode
    def protect_self(self):
        tracking_list = particlesObj.get_list()

        #this method doesn't work if the tracking list would have zero entries, in the case of the start of gameplay
        #the method won't try to run if there are no items in the tracking list
        if len(tracking_list) > 0:
            index = 0

            #loops through the values and produces their respective time to intersect if needed

            while index < len(tracking_list):
                #easier variable
                i = index
                start_x = tracking_list[i][0]
                start_y = tracking_list[i][1]
                vel_x = tracking_list[i][2]
                vel_y = tracking_list[i][3]

                start_pos = (start_x, start_y)
                #create an endpoint that is arbitrarily far away from the start_pos to ensure none of the particles are "out of range" of the npc's vision
                end_pos = (vel_x * 2000 + start_x, vel_y * 2000 + start_y)
                #check whether this line will clip through the rect for player 2/npc
                if self.rect.clipline(start_pos, end_pos):
                    tracking_list[i][4] = True
                #clipline method returns two tuples
                #the first tuple is the starting point of the line
                #the second tuple is the ending point of the line
                #the component distances are calculating by accessing the second tuple, and the respective indices of that tuple, then finding the distance between the values at those indices and the values at the start of the line
                #this essentially calculates the distance between where the particle currently is and where it would contact with the player_2_rect and cause the npc to die
                #this value is then divided by speed to calculate the time to intersect
                #the time is then added to the particle's list as another value
                #the particles are then reverse sorted by this value into another list
                #the npc methods will then tell the npc which direction to face at any given frame, and whether to deflect if the closest particle is within a certain range
                #absolutes are used to ensure that "negative" distances aren't sorted below positive distances

                    d_x = abs(player_2_rect.clipline(start_pos, end_pos)[1][0] -
                              player_2_rect.clipline(start_pos, end_pos)[0][0])
                    d_y = abs(player_2_rect.clipline(start_pos, end_pos)[1][1] -
                              player_2_rect.clipline(start_pos, end_pos)[0][1])
                    distance = math.sqrt(d_x ** 2 + d_y ** 2)
                    speed = math.sqrt(vel_x ** 2 + vel_y ** 2)
                    # multiply by FPS to get the number of pixels per second
                    # the "speed" value was originally in pixels per frame because that was how the speed was defined for the particles in the Particle.list
                    time_to_intersect = (distance / speed) * FPS
                    tracking_list[i][5] = time_to_intersect
                else:
                    tracking_list[i][4] = False

            time_list = {}

            for i in tracking_list:
                #if they intersect, add their time
                if tracking_list[i][4]:
                    time_list[i] = tracking_list[i][5]
                #if not, add a large enough value that they will be sorted to the back
                else:
                    time_list[i] = 10000

            # basically, a new dictionary is created with the time_list indices as the keys
            # this dictionary is based on the sorted version of the time_list dictionary
            # when the sorted method is called, it converts each entry in the dictionary into a tuple with indices 0 and 1.
            # index 0 holds the item name, and index 1 holds the value or definition
            # the list is then sorted based on this lambda function, which tells the computer to sort using the value of index 1
            time_list_sorted = list(sorted(time_list.items(), key=lambda item: item[1]))

            # access the index of the highest threat particle
            # I think this should be [0] not [0][0]
            time_list_closest_index = time_list_sorted[0][0]
            # access the particles info list at that index
            tracking_list_closest = tracking_list[time_list_closest_index]

            # access the x-pos from the list
            closest_x = tracking_list_closest[0]
            closest_y = tracking_list_closest[1]
            closest_vel_x = tracking_list_closest[2]
            closest_vel_y = tracking_list_closest[3]

            closest_stop_x = closest_vel_x * 2000 + closest_x
            closest_stop_y = closest_vel_y * 2000 + closest_y

            closest_pos = (closest_x, closest_y)
            closest_stop = (closest_stop_x, closest_stop_y)

            # determining which deflect bar the line from the particle to the npc collides with
            global player_2_direction
            global player_2_deflection
            if player_2_left_rect.clipline(closest_pos, closest_stop):
                player_2_direction = "Left"
            if player_2_up_rect.clipline(closest_pos, closest_stop):
                player_2_direction = "Up"
            if player_2_right_rect.clipline(closest_pos, closest_stop):
                player_2_direction = "Right"
            else:
                player_2_direction = "Up"

            # if the particle gets within a certain time to collision, use the deflect bar
            if tracking_list_closest[0][5] < 0.3 * FPS:
                player_2_deflection = player_2_direction


#create an object of the Particles class
particlesObj = Particles()


#creating player 1 and 2 objects
player_1 = Player1(player_1_x, player_1_y)
player_2 = Player2(player_2_x, player_2_y)

#creating npc object
computer = npc()



#cutscene function that uses the draw_image function
#will probably implement later but focusing on gameplay for now
#def cutscene(time, image_name, x, y, update):


#defining variables

#1 = 1 player vs. AI, 2 = 2 player couch multiplayer. This variable is for 1 or 2 player selection.
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
        draw_text("Deflection", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2, (0,0,0))
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
        draw_text("1 Player", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2, (0,0,0))
        draw_text("2 Player", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2 + 100, (0,0,0))
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
                    draw_image(Menu_Select_Arrow, 300, 275, True)
                    draw_rect(50, 50, 300, 375, (0,0,0))
                    Menu_Select_Sound.play()
                    game_mode = 1
                    print(game_mode)
                if event.key == pygame.K_DOWN:
                    #select 1 player
                    draw_image(Menu_Select_Arrow, 300, 375, True)
                    draw_rect(50, 50, 300, 275, (0, 0, 0))
                    Menu_Select_Sound.play()
                    game_mode = 2
                    print(game_mode)
                if event.key == pygame.K_RETURN and game_mode > 0:
                    player_select = False

    if game_mode == 1 and waiting and running:
        screen.fill((0,0,0))
        draw_text("Player 1: AWD for directions, F to deflect.", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2, (0,0,0))
        pygame.display.flip()
        Menu_Select_Sound.play()
        print("play")
        waiting = False
        playing = True
        pygame.time.delay(3000)
    if game_mode == 2 and waiting and running:
        screen.fill((0, 0, 0))
        draw_text("Player 1: WSD for directions, F to deflect.", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2 - 50, (0,0,0))
        draw_text("Player 2: Arrows for directions, ctrl to deflect.", menu_font, (5, 21, 214), screen_width / 2, screen_height / 2 + 50, (0,0,0))
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
    match game_mode:
        case 1:

            while playing:

                #limit to 120 FPS
                clock.tick(FPS)

                #user input for directions
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        start = False
                        player_select = False
                        playing = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            #turn player one to the left
                            print("Left")
                            player_1_direction = "Left"
                        if event.key == pygame.K_s:
                            #turn player one down
                            print("Down")
                            player_1_direction = "Down"
                        if event.key == pygame.K_d:
                            #turn player to the right
                            print("Right")
                            player_1_direction = "Right"
                        if event.key == pygame.K_f:
                            #direction is always going to be some value since it doesn't get reset
                            #Use deflection instead since that gets cleared by check_bar_for_frame()
                            if player_1_deflection == "":
                                if player_1_direction == "Left":
                                    draw_image(Vertical_Deflect_Bar, player_1_x - 30, player_1_y, True)
                                    player_1_deflection = player_1_direction
                                if player_1_direction == "Down":
                                    draw_image(Horizontal_Deflect_Bar, player_1_x, player_1_y + 30, True)
                                    player_1_deflection = player_1_direction
                                if player_1_direction == "Right":
                                    draw_image(Vertical_Deflect_Bar, player_1_x + 30, player_1_y, True)
                                    player_1_deflection = player_1_direction

                computer.protect_self()

                match player_1_direction:
                    case "Left":
                        draw_image(Small_Arrow_Left, player_1_x, player_1_y, True)
                    case "Right":
                        draw_image(Small_Arrow_Right, player_1_x, player_1_y, True)
                    case "Down":
                        draw_image(Small_Arrow_Down, player_1_x, player_1_y, True)
                    case _:
                        draw_image(Small_Arrow_Down, player_1_x, player_1_y, True)

                match player_2_direction:
                    case "Left":
                        draw_image(Small_Arrow_Left, player_2_x, player_2_y, True)
                    case "Right":
                        draw_image(Small_Arrow_Right, player_2_x, player_2_y, True)
                    case "Up":
                        draw_image(Small_Arrow_Up, player_2_x, player_2_y, True)
                    case _:
                        draw_image(Small_Arrow_Up, player_2_x, player_2_y, True)

                player_2.check_bar_for_frame()

                player_1.check_bar_for_frame()
                draw_with_rect(wall_left_rect, (0, 50, 0))
                draw_with_rect(wall_top_rect, (0, 50, 0))
                draw_with_rect(wall_bottom_rect, (0, 50, 0))
                draw_with_rect(wall_right_rect, (0, 50, 0))

                particlesObj.spawn_particle()
                particlesObj.check_list()


                        #need a function or method to display the deflection bar for a certain number of frames
                        #method takes in image name, x, y, and number of frames
                        #the method will run until it reaches a targeted frame
                        #the targeted frame will be based on the current frame when the method is first called, plus some number of frames
                        #each frame, the game will iterate through the while loop, and check to see if the current frame is equal to the targeted frame
                        #if so, it will clear the image and assign a value of false to a global variable for whether the player is blocking on that side
                        #if not, it will not return any value
        case 2: #2 player mode)
            while playing:
                # limit to 120 FPS
                clock.tick(FPS)

                #draw the walls
                draw_with_rect(wall_left_rect, (0, 50, 0))
                draw_with_rect(wall_top_rect, (0, 50, 0))
                draw_with_rect(wall_bottom_rect, (0, 50, 0))
                draw_with_rect(wall_right_rect, (0, 50, 0))

                #initialize UI
                player_1.print_score()
                player_2.print_score()


                # user input for directions
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        start = False
                        player_select = False
                        playing = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            # turn player one to the left
                            print("Left")
                            player_1_direction = "Left"
                        if event.key == pygame.K_s:
                            # turn player one down
                            print("Down")
                            player_1_direction = "Down"
                        if event.key == pygame.K_d:
                            # turn player to the right
                            print("Right")
                            player_1_direction = "Right"
                        if event.key == pygame.K_f:
                            # direction is always going to be some value since it doesn't get reset
                            # Use deflection instead since that gets cleared by check_bar_for_frame()
                            if player_1_deflection == "":
                                if player_1_direction == "Left":
                                    draw_image(Vertical_Deflect_Bar, player_1_x - 30, player_1_y, True)
                                    player_1_deflection = player_1_direction
                                if player_1_direction == "Down":
                                    draw_image(Horizontal_Deflect_Bar, player_1_x, player_1_y + 30, True)
                                    player_1_deflection = player_1_direction
                                if player_1_direction == "Right":
                                    draw_image(Vertical_Deflect_Bar, player_1_x + 30, player_1_y, True)
                                    player_1_deflection = player_1_direction
                        if event.key == pygame.K_LEFT:
                            # turn player one to the left
                            print("Left")
                            player_2_direction = "Left"
                        if event.key == pygame.K_UP:
                            # turn player one down
                            print("Up")
                            player_2_direction = "Up"
                        if event.key == pygame.K_RIGHT:
                            # turn player to the right
                            print("Right")
                            player_2_direction = "Right"
                        #right control for player 2
                        if event.key == pygame.K_RCTRL:
                            # direction is always going to be some value since it doesn't get reset
                            # Use deflection instead since that gets cleared by check_bar_for_frame()
                            if player_2_deflection == "":
                                if player_2_direction == "Left":
                                    draw_image(Vertical_Deflect_Bar, player_2_x - 30, player_2_y, True)
                                    player_2_deflection = player_2_direction
                                if player_2_direction == "Up":
                                    draw_image(Horizontal_Deflect_Bar, player_2_x, player_2_y - 30, True)
                                    player_2_deflection = player_2_direction
                                if player_2_direction == "Right":
                                    draw_image(Vertical_Deflect_Bar, player_2_x + 30, player_2_y, True)
                                    player_2_deflection = player_2_direction

                match player_1_direction:
                    case "Left":
                        draw_image(Small_Arrow_Left, player_1_x, player_1_y, True)
                    case "Right":
                        draw_image(Small_Arrow_Right, player_1_x, player_1_y, True)
                    case "Down":
                        draw_image(Small_Arrow_Down, player_1_x, player_1_y, True)
                    case _:
                        draw_image(Small_Arrow_Down, player_1_x, player_1_y, True)

                match player_2_direction:
                    case "Left":
                        draw_image(Small_Arrow_Left, player_2_x, player_2_y, True)
                    case "Right":
                        draw_image(Small_Arrow_Right, player_2_x, player_2_y, True)
                    case "Up":
                        draw_image(Small_Arrow_Up, player_2_x, player_2_y, True)
                    case _:
                        draw_image(Small_Arrow_Up, player_2_x, player_2_y, True)




                particlesObj.spawn_particle()
                particlesObj.check_list()

                #checking I-frames
                player_1.check_bar_for_frame()
                player_2.check_bar_for_frame()












