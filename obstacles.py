#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Sprite
import system

class BlackHole(Sprite):
    image = None
    def __init__(self,x,y,group,surf,w,h,mass,image=str('black_hole.png')):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(image)
        self.image = self.scale(w,h)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group = group
        self.add(self.group)
        self.mass = mass
        self.surface = surf

    def scale(self,w,h):
        return pygame.transform.scale(self.image, (w,h))
        
    def move(self,newx,newy):
        self.rect.x = newx
        self.rect.y = newy

    def update(self):
        pass
