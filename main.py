#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from player import Player
from goal import Goal
from bar import *
from starfield import Starfield
from transitions import Intro, Transition
from obstacles import BlackHole


class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self,level=1):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30
        self.gameOver = False
        self.userPlacedObjects = Group()
        self.startItems = RenderUpdates()
        self.playerGroup = RenderUpdates()
        self.tails = RenderUpdates()
        self.obstacles = RenderUpdates()
        self.goalCollide = Group()
        self.toolbar = OrderedUpdates()
        #self.intro_screen = Intro(0,0,self.startItems)
        self.bar = ToolBar(0,626,self.toolbar,self.screen,self)
        self.goal = Goal(573,372,self.goalCollide)
        self.player = Player(50,535,self.screen,(255,0,0),self.playerGroup,1000,750,self.tails)
        self.transition = Transition(-1314,0,self.screen,self.startItems)
        self.level = level
        self.levelUp = True
        self.stars = Starfield(self.screen,1000,626,200)
        BlackHole(339,70,self.obstacles,self.screen,80,71)


    def quit(self):
        self.gameOver = False
        self.done = True

   
    def level_0(self):
        self.clock.tick(self.fps)
        pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
        
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit()
                elif evt.key == K_RETURN:
                    self.intro_screen.begin()

       
        if self.intro_screen.next_level():
            self.level = 1
        
        self.startItems.update()
        self.startItems.update()
        self.stars.draw()
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.playerGroup.draw(self.screen)
        self.startItems.draw(self.screen)

        pygame.display.flip()

        

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
            if evt.type == MOUSEBUTTONDOWN:
                print pygame.mouse.get_pos()
            if evt.type == MOUSEBUTTONDOWN:
                self.bar.collision_test(pygame.mouse.get_pos(),self.player)
            if evt.type == MOUSEBUTTONUP:
                self.bar.clear_grabbed()
             

     
        self.stars.draw()
        self.obstacles.update()
        self.bar.update(pygame.mouse.get_pos())
        self.userPlacedObjects.update(self.screen)
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.player.drawTails()
        self.obstacles.draw(self.screen)
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)  

        if len(self.playerGroup) == 0 and self.player.lives > 0:
            self.bar.lives_update()
            self.bar.score.update(-200)
            pygame.time.wait(750)
            self.player.add(self.playerGroup)
        elif len(self.playerGroup) == 0:
            self.bar.lives_update()
                
        if pygame.sprite.spritecollideany(self.player, self.goalCollide) != None:
            self.next_level()
        elif pygame.sprite.spritecollideany(self.player,self.obstacles) != None:
            self.player.blackHoleCollision(True,False)

        pygame.display.flip()


    def next_level(self):
        self.transition.add_to_group()
        changed = False
        while True:
            self.clock.tick(self.fps)
            pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
            
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    self.quit()
                if evt.type == KEYDOWN:
                    if evt.key == K_ESCAPE:
                        self.quit()
                        
            if self.transition.rect.x >= -50 and not changed:
                self.goal.change_loc(600,60)
                self.goal.change_image(str('venus.png'))
                self.player.restart()
                change = True
                
                
            self.startItems.update()
            self.stars.draw()
            self.goalCollide.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.player.drawTails()
            self.obstacles.draw(self.screen)
            self.playerGroup.draw(self.screen)  
            self.startItems.draw(self.screen)
            if self.transition.rect.x > 1000:
                break


            pygame.display.flip()
        self.transition.reset(-1314)

    def gameOver_tick(self):
        self.clock.tick(self.fps)
        
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit()
                if evt.key == K_r:
                    self.gameOver = False


    def run(self,level=0):
        self.done = False
        self.clock = pygame.time.Clock()
        while not self.done:
            while self.level == 0 and not self.done:
                self.level_0()
            while self.level >= 1 and not self.done:
                self.tick()
            while self.gameOver:
                self.gameOver_tick()


Game().run()

'''TODO'''
####GRAVITY OBJECTS (PLACEABLE/predefined)
####OTHER OBSTACLES
#SAVING
#LOADING
#LEVELS


'''DONE(ish)'''
#PLAYER TRAIL
#PLAYER OBJECT
#GOAL
