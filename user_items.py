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
        self.reGroup = False
        self.group = group
        self.grabbed = True
        self.mouse_offset = ((26,26))
        self.temp = temp
        self.add(temp)
                
    def update(self,pos,other=None):
        xchange,ychange = pos
        xoff,yoff = self.mouse_offset
        newX = xchange-xoff
        newY = ychange-yoff
        if newX >= 1 and newX <= 999 and newY >= 1 and self.grabbed:
            self.rect.x = newX
            self.rect.y = newY
        if self.rect.y+self.rect.h < 620 and self.reGroup == False:
            self.reGroup = True
        
    def collision_test(self,pos):
        print 'testin'

    def dropped(self):
        self.grabbed = False
        self.kill()
        self.add(self.group)
    
    def grab(self,pos):
        x,y = pos
        xoffset = x-self.rect.x
        yoffset = y-self.rect.y
        self.mouse_offset = ((xoffset,yoffset))
        self.grabbed = True

    def drop(self):
        self.grabbed = False
        if self.rect.y > 628 and self.reGroup == True:
            self.kill()

    def draw(self,surf):
        surf.blit(self.image,(self.rect.x,self.rect.y))
