#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates
import os, sys




class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30

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
