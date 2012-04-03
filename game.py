#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates
import os, sys


class Player(Sprite):
    def __init__(self,x,y,w,h,surf,color):
        Sprite.__init__(self)
        self.makeANew = False
        '''
        self.rect.x = x
        self.rect.y = y
        self.rect.w = w
        self.rect.h = h
        '''
        self.shaper = (x,y,w,h)
        self.screen = surf
        self.color = color
        self.goTo = [(4,-3),(4,-4),(4,-2),(4,-1),(4,-6)]

    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.shaper)

    def update(self):
        if self.makeANew:
            x, y, w, h = self.shaper
            newX, newY = self.newplace
            x += newX
            y += newY
            self.shaper = (x,y,w,h)

    def refresh(self,newplace):
        self.makeANew = True
        self.newplace = self.goTo[newplace]

    def die(self):
        pass

class Toolbar(Sprite):
    def __init__(self,x,y,image):
        Sprite.__init__(self)
        


class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30
        self.player = Player(50,535,30,30,self.screen,(255,0,0))

    def quit(self):
        self.done = True

        
    def tick(self):
        self.clock.tick(self.fps)
        pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))

        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit()
                if evt.key == K_q:
                    self.player.refresh(0)
                if evt.key == K_w:
                    self.player.refresh(1)
                if evt.key == K_e:
                    self.player.refresh(2)
                if evt.key == K_r:
                    self.player.refresh(3)
                if evt.key == K_t:
                    self.player.refresh(4)


        self.player.update()
        self.player.draw()
        
                
        pygame.display.flip()


    def run(self):
        self.done = False
        self.clock = pygame.time.Clock()
        while not self.done:
            self.tick()


Game().run()



#PLAYER TRAIL
#PLAYER OBJECT
#GRAVITY OBJECTS (PLACEABLE/predefined)
#GOAL
#SCORE MECHANISM
