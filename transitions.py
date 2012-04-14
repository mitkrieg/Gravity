#!/usr/bin/env python

import pygame
from system import *
from pygame.locals import *
from pygame.sprite import Sprite


class Intro(Sprite):
    def __init__(self,x,y,group,image=str('title.png')):
        Sprite.__init__(self)
        self.image = load_graphics(image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.group = group
        self.move = False
        self.add(group)

    def update(self):
        if self.move and self.rect.y > -750:
            self.rect.y -= 30
            

    def next_level(self):
        if self.move and self.rect.y > -750:
            return False
        elif self.move:
            self.kill()
            return True
        else:
            return False

    def begin(self):
        self.move = True
        
        

class Transition(Intro):
    def __init__(self,x,y,surface,group,image=str('transition.png')):
        Sprite.__init__(self)
        self.image = load_graphics(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.surface = surface
        self.move = False
        self.group = group
    
  
    def update(self):
        if self.rect.x < 1005:
            self.rect.x += 60

    def over(self):
        if self.rect.x > 1005:
            return True
        else:
            return False

    def reset(self,x):
        self.rect.x = x 

    def add_to_group(self):
        self.add(self.group)
