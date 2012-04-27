#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from player import Player
#from goal import Goal
from bar import *
from starfield import Starfield
from transitions import Intro, Transition, GameOverScreen
from obstacles import BlackHole
from user_items import UserPlanet
import sys


class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self,level=1):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30
        self.userPlacedObjects = Group()
        self.startItems = RenderUpdates()
        self.playerGroup = RenderUpdates()
        self.tails = RenderUpdates()
        self.blackHoles = RenderUpdates()
        self.obstacles = RenderUpdates()
        self.goalCollide = Group()
        self.toolbar = OrderedUpdates()
        if level == 0:
            self.intro_screen = Intro(0,0,self.startItems)
        self.goal = Goal(573,372,self.goalCollide,30)
        self.bar = ToolBar(0,626,self.toolbar,self.screen,self,self.goal)
        self.player = Player(50,535,self.screen,(255,0,0),self.playerGroup,1000,624,(2,-2),self.tails,self)
        self.transition = Transition(-1314,0,self.screen,self.startItems)
        self.level = level
        self.levelUp = True
        self.stars = Starfield(self.screen,1000,626,200)
        BlackHole(339,70,self.blackHoles,self.screen,80,71,16)
        self.obstacles.add(self.blackHoles)
        self.obstacles.add(self.goalCollide)
        self.freeb = False
        self.gotoLevel = level
      
    def quit(self):
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
                elif evt.key == K_RIGHT:
                    self.intro_screen.instruct(True)
                elif evt.key == K_LEFT:
                    self.intro_screen.instruct(False)

       
        if self.intro_screen.next_level():
            self.level = 1
        
        self.startItems.update()
        self.startItems.update()
        self.stars.draw()
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.playerGroup.draw(self.screen)
        self.blackHoles.draw(self.screen)
        self.startItems.draw(self.screen)
        

        pygame.display.flip()

        

    def tick(self):
        self.clock.tick(self.fps)
        pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
        pos = pygame.mouse.get_pos()

        #inputs queue
        for evt in pygame.event.get():
            if evt.type == QUIT:
                self.quit()
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE and not self.bar.itemsTab.open and self.bar.grabbed == None:
                    self.bar.menuWidget.dropped()
                    #self.quit()
                #    self.bar.grabbed = self.bar.menuWidget
                if evt.key == K_z:
                    print self.bar.items_one_placed   
            #elif evt.type == KEYUP:
                #if evt.key == K_ESCAPE:
                 #   self.bar.clear_grabbed()
            elif evt.type == MOUSEBUTTONDOWN:
                print pos
                should_freebie = self.bar.collision_test(pos,self.player,evt.button)
                if should_freebie and not self.freeb:
                    self.freebie()
                    self.freeb = True
                if evt.button == 1:
                    for obj in self.userPlacedObjects:
                        if obj.rect.collidepoint(pos) and not self.player.makeANew and not self.bar.menuWidget.open:
                            obj.grab(pos)
                elif evt.button == 3:
                    for obj in self.userPlacedObjects:
                        if obj.rect.collidepoint(pos) and not self.player.makeANew and not self.bar.menuWidget.open:
                            obj.remove()
                #print evt.button
            elif evt.type == MOUSEBUTTONUP:
                self.bar.clear_grabbed()
                for obj in self.userPlacedObjects:
                    obj.drop(self.blackHoles)
             

     
        self.stars.draw()
        self.blackHoles.update()
        self.bar.update(pos)
        self.blackHoles.draw(self.screen)
        self.userPlacedObjects.update(pos)
        self.userPlacedObjects.draw(self.screen)
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.player.drawTails()
        self.playerGroup.update()
        self.playerGroup.draw(self.screen)  

        if len(self.playerGroup) == 0 and self.player.lives >1:
            self.bar.lives_update()
            self.bar.score.update(-200)
            pygame.time.wait(750)
            self.player.lives -= 1
            self.player.add(self.playerGroup)
        elif len(self.playerGroup) == 0:
            self.bar.score.update(-200)
            self.bar.lives_update()
            self.over_screen = GameOverScreen(293,161,self.screen)
            self.gameOver()
                
        if pygame.sprite.spritecollideany(self.player, self.goalCollide) != None:
            self.next_level()
        elif pygame.sprite.spritecollideany(self.player,self.blackHoles) != None:
            self.player.blackHoleCollision(True,False)

        for obj in self.userPlacedObjects:
            if pygame.sprite.collide_mask(self.player,obj) and not obj.grabbed:
                self.player.update(True)
        pygame.display.flip()


    def next_level(self):
        if self.level < 2:
            self.level += 1
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
                if self.level == 2:
                    self.goal.next_level(self.level)
                    self.bar.next_level(self.level)
                    self.userPlacedObjects.empty()
                    self.freeb = False
                    self.bar.itemsTab.earth_item.light()
                    for hole in self.blackHoles:
                        hole.move(842,388)
                    hole = BlackHole(388,189,self.blackHoles,self.screen,80,71,16)
                    hole.flip()

                self.player.restart()
                changed = True
                
                
            self.startItems.update()
            self.stars.draw()
            self.goalCollide.draw(self.screen)
            self.userPlacedObjects.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.player.drawTails()
            self.blackHoles.draw(self.screen)
            self.playerGroup.draw(self.screen)  
            self.startItems.draw(self.screen)
            if self.transition.rect.x > 1000:
                self.transition.kill()
                break


            pygame.display.flip()
        self.transition.reset(-1314)

    
    def freebie(self):
        groupus = Group()
        groupus.add(self.blackHoles,self.goal)
        self.player.makeANew = True
        self.player.addTail = False
        while True:
            self.clock.tick(self.fps)
            pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
            
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    self.quit()
                if evt.type == KEYDOWN:
                    if evt.key == K_ESCAPE:
                        self.quit()
            
                        
            if pygame.sprite.spritecollideany(self.player,self.blackHoles) != None:
                self.player.blackHoleCollision(True,False)

            self.startItems.update()
            self.stars.draw()
            self.player.drawTails()
            self.goalCollide.draw(self.screen)
            self.userPlacedObjects.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.blackHoles.draw(self.screen)
            self.player.update(False,groupus)
            self.playerGroup.draw(self.screen)  
            self.startItems.draw(self.screen)
            if len(self.playerGroup) < 1:
                self.player.addTail = True
                pygame.time.wait(750)
                self.player.add(self.playerGroup)
                break
            pygame.display.flip()
            

    def gameOver(self):
        overing = True
        #self.bar.lives_update()
        self.bar.update()
        self.toolbar.draw(self.screen)
        self.over_screen.draw()
        while overing:
            self.clock.tick(self.fps)
            
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    overing = False
                    self.quit()
                if evt.type == KEYDOWN:
                    if evt.key == K_ESCAPE:
                        overing = False
                        self.quit()
                    if evt.key == K_RETURN:
                        overing = False
            
            pygame.display.flip()
        
        self.player.add(self.playerGroup)
        self.bar.reset_lives_over()
        self.player.restart()
        self.over_screen.kill()
                
                    

    def run(self,level=0):
        self.done = False
        self.clock = pygame.time.Clock()
        if self.gotoLevel > 1 and self.gotoLevel < 3:
            self.tick()
            self.level = self.gotoLevel
            self.next_level()
        while not self.done:
            while self.level == 0 and not self.done:
                self.level_0()
            while self.level >= 1 and not self.done:
                self.tick()




if len(sys.argv) > 1:
    level = sys.argv[1]
else:
    level = 1

level = int(level)

Game(level).run()

'''////////////Pylygon Methods
#http://www.pygame.org/project-pylygon-1718-.html

////////////TODO
#INSTRUCTIONS OPTION IN MENU WIDGET
#WARNING FOR ITEM LIMIT###
#RIGHT CLICK FOR EDITING OBJECT
OTHER OBSTACLES (enemy ships, asteroids, comets)
SAVING
LOADING
LEVELS

////////////BUGS
##SQUASHED BUGS
USER PLACING OBJECT ON TOP OF PLAYER, FREAKS OUT!

////////////DONE(ish)
PLAYER TRAIL
PLAYER OBJECT
GOAL
'''
