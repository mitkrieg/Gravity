#!/usr/bin/env python
import system
import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class Goal(Sprite):
    image = None
    def __init__(self,x,y,group,mass=0):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics('venus.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group = group
        self.mass = mass
        self.add(group)
        self.nextPosition = 0
        self.positions = [(638,135),(687,355),(680,400)]
        self.images = [(str('saturny.png')),(str('ring_planet.png')),
                       (str('earth.png'))]

    def resize(self,w,h):
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.transform.smoothscale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def change_loc(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def next_level(self,level):
        x,y = self.positions[level-2]
        self.image = system.load_graphics(self.images[level-2])
        self.rect.x = x
        self.rect.y = y
        self.nextPosition += 1

    def change_image(self,new_image=str('earth.png')):
        self.image = system.load_graphics(new_image)


    def new_mass(self,m):
        self.mass = m
