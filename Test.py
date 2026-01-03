import pygame
import math

screen_width = 1024
screen_height = 576
screen_rect = (screen_width, screen_height)
FPS = 120

player_2_x = screen_width // 2
player_2_y = screen_height - 35 - 50
player_2_rect = pygame.Rect(player_2_x, player_2_y, 50, 50)
player_2_rect.center = (player_2_x, player_2_y)

list_a = [400, 379, 1, 1, False, 0]
list_b = [400, 379, 2, 2, False, 0]
list_c = [1, 1, 2, 3, False, 0]

#for list_2
list_d =  [0,0,0,0, True, 1]
list_e =  [0,0,0,0, True, 2]
list_f =  [0,0,0,0, True, 3]

list_2 = {1: 12, 2: 0, 3: 100, 4: 500}

mega_list = [list_a, list_b, list_c]

tracking_list = mega_list

# this method doesn't work if the tracking list would have zero entries, in the case of the start of gameplay
# the method won't try to run if there are no items in the tracking list
index = 0
while index < len(tracking_list):
    if len(tracking_list) > 0:
        i = 0
        # easier variable
        start_x = tracking_list[i][0]
        start_y = tracking_list[i][1]
        vel_x = tracking_list[i][2]
        vel_y = tracking_list[i][3]

        start_pos = (start_x, start_y)
        # create an endpoint that is arbitrarily far away from the start_pos to ensure none of the particles are "out of range" of the npc's vision
        end_pos = (vel_x * 2000 + start_x, vel_y * 2000 + start_y)
        # check whether this line will clip through the rect for player 2/npc
        if player_2_rect.clipline(start_pos, end_pos):
            tracking_list[i][4] = True
        else:
            tracking_list[i][4] = False

        # clipline method returns two tuples
        # the first tuple is the starting point of the line
        # the second tuple is the ending point of the line
        # the component distances are calculating by accessing the second tuple, and the respective indices of that tuple, then finding the distance between the values at those indices and the values at the start of the line
        # this essentially calculates the distance between where the particle currently is and where it would contact with the player_2_rect and cause the npc to die
        # this value is then divided by speed to calculate the time to intersect
        # the time is then added to the particle's list as another value
        # the particles are then reverse sorted by this value into another list
        # the npc methods will then tell the npc which direction to face at any given frame, and whether to deflect if the closest particle is within a certain range
        # absolutes are used to ensure that "negative" distances aren't sorted below positive distances
        # this is throwing an error because there aren't any intersections, so the code defaults to trying to access an empty tuple
        if player_2_rect.clipline(start_pos, end_pos):
            points = player_2_rect.clipline(start_pos, end_pos)
            d_x = abs(points[1][0] - player_2_rect.clipline(start_pos, end_pos)[0][0])
            d_y = abs(player_2_rect.clipline(start_pos, end_pos)[1][1] - player_2_rect.clipline(start_pos, end_pos)[0][1])
            distance = math.sqrt(d_x ** 2 + d_y ** 2)
            speed = (vel_x ** 2 + vel_y ** 2) ** 0.5
            # multiply by FPS to get the number of pixels per second
            # the "speed" value was originally in pixels per frame because that was how the speed was defined for the particles in the Particle.list
            time_to_intersect = (distance / speed) / FPS
            tracking_list[i][5] = time_to_intersect
            # increment loop
            index += 1


time_list = {}

for list_n in tracking_list:
    i = tracking_list.index(list_n)
    time_list[i] = (tracking_list[i])[5]

# basically, a new dictionary is created with the time_list indices as the keys
# this dictionary is based on the sorted version of the time_list dictionary
# when the sorted method is called, it converts each entry in the dictionary into a tuple with indices 0 and 1.
# index 0 holds the item name, and index 1 holds the value or definition
# the list is then sorted based on this lambda function, which tells the computer to sort using the value of index 1
time_list_sorted = list(sorted(time_list.items(), key = lambda item: item[1]))

# access the index of the highest threat particle
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

print(tracking_list)
#sorted method is working apparently
statement = list(sorted(list_2.items(), key = lambda item: item[1]))
print(statement)



