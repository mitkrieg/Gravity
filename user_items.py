#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Sprite
import system

class UserPlanet(Sprite):
    image = None
    def __init__(self,x,y,w,h,start_mass,group,temp,image):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(image)
        self.image = pygame.transform.smoothscale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mass = start_mass
        self.group = group
        self.grabbed = True
        self.mouse_offset = 26
        self.add(temp)
        
        
    def update(self,pos,other=None):
        x,y = pos
        x -= self.mouse_offset
        y -= self.mouse_offset
        if x >= 1 and x <= 999 and y >= 1 and self.grabbed:
            self.rect.x = x
            self.rect.y = y

    def collision_test(self,pos):
        print 'testin'

    def dropped(self):
        self.grabbed = False
        self.kill()
        self.add(self.group)
    
    def grab(self):
        self.grabbed = True

    def drop(self):
        self.grabbed = False
