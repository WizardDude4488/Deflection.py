import pygame
import random

screen_width = 1024
screen_height = 576


class Particles:
    class Particle:
        def __init__(self, pos_x, pos_y, vel_x, vel_y, radius):
            self.pos_x, self.pos_y, self.vel_x, self.vel_y, self.radius = pos_x, pos_y, vel_x, vel_y, radius
            self.rect = pygame.Rect(pos_x, pos_y, 2 * radius, 2 * radius)
            self.rect.center = (pos_x, pos_y)
            self.damaged = False
            self.delete = False
            self.color = (5, 21, 214)
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

        print(tracking_list)

particlesObj = Particles()

i = 0
while i < 2000:
    particlesObj.spawn_particle()
    particlesObj.get_list()
    i += 1

particlesObj.get_list()
