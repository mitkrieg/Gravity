#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from gameobjects import Player, Goal, ToolBar, Star, Planet 


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
        self.planetGroup = Group()
        self.playerGroup = RenderUpdates()
        self.tails = RenderUpdates()
        self.goalCollide = Group()
        self.toolbar = OrderedUpdates()
        self.bar = ToolBar(0,626,self.toolbar,self.screen)
        self.goal = Goal(600,300,self.goalCollide)
        self.barGoal = Goal(605,696,self.toolbar)
        self.barGoal.resize(40,40)
        self.player = Player(50,535,self.screen,(255,0,0),self.playerGroup,1000,750,self.tails)
        self.planets = Planet(100,100,50,1,self.planetGroup)
        self.stars = Star(self.screen,1000,626,70)

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
            #if evt.type == MOUSEBUTTONDOWN:
            #   print pygame.mouse.get_pos()
            if evt.type == MOUSEBUTTONDOWN:
                self.bar.go_collision(pygame.mouse.get_pos(),self.player)

     
        self.stars.draw()
        self.planetGroup.update(self.screen)
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.player.drawTails()
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)  

        if len(self.playerGroup) == 0 and self.player.lives > 0:
            pygame.time.wait(750)
            self.bar.lives_update()
            self.player.add(self.playerGroup)
        elif len(self.playerGroup) == 0:
            self.bar.lives_update()
                
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
