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
            self.image = system.load_graphics('earth.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group = group
        self.mass = mass
        self.add(group)

    def resize(self,w,h):
        self.image = pygame.transform.scale(self.image,(w,h))

    def change_loc(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def change_image(self,new_image=str('earth.png')):
        self.image = system.load_graphics(new_image)

