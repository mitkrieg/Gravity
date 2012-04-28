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
        self.rect.x = x
        self.rect.y = y
        self.group = group
        self.starting = False
        self.instructions = False
        self.add(group)

    def update(self):
        if self.starting and self.rect.y > -750:
            self.rect.y -= 30
        elif self.instructions and self.rect.x > -1000:
            self.rect.x -= 40
        elif not self.instructions and self.rect.x < 0:
            self.rect.x += 40
            

    def next_level(self):
        if self.starting and self.rect.y > -750:
            return False
        elif self.starting:
            self.kill()
            return True
        else:
            return False

    def begin(self):
        self.starting = True

    def instruct(self,boo):
        if boo:
            self.instructions = True
        else:
            self.instructions = False
        

class Instructions(Intro):
    def __init__(self,x,y,group,image=str('instructions.png')):
        Intro.__init__(self,x,y,group,image)
        

class Transition(Sprite):
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

class GameOverScreen(Sprite):
    image = None
    def __init__(self,x,y,surface,image=str('gameover.png')):
        Sprite.__init__(self)
        if self.image == None:
            self.image = load_graphics(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.surface = surface
        
    def update(self):
        pass

    def draw(self):
        self.surface.blit(self.image,(self.rect.x,self.rect.y))
