#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates
from gameobjects import Player, Goal


class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30
        self.gameOver = False
        self.playerGroup = RenderUpdates()
        self.tails = RenderUpdates()
        self.goalCollide = Group()
        self.goal = Goal(600,300,self.goalCollide)
        self.player = Player(50,535,self.screen,(255,0,0),self.playerGroup,1000,750,self.tails)

    def quit(self):
        self.gameOver = False
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
                
        self.goalCollide.draw(self.screen)
        self.player.drawTails()
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)  

        if len(self.playerGroup) == 0:
            pygame.time.wait(750)
            self.player.add(self.playerGroup)
                
        if pygame.sprite.spritecollideany(self.player, self.goalCollide) != None:
            self.done = True
            self.gameOver = True

        pygame.display.flip()

    def gameOver_tick(self):
        self.clock.tick(self.fps)
        
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit()


    def run(self):
        self.done = False
        self.clock = pygame.time.Clock()
        while not self.done:
            self.tick()
        while self.gameOver:
            self.gameOver_tick()

Game().run()



'''TODO'''
#GRAVITY OBJECTS (PLACEABLE/predefined)
#SCORE MECHANISM



'''DONE(ish)'''
#PLAYER TRAIL
#PLAYER OBJECT
#GOAL
