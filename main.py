#!/usr/bin/env python

import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates, OrderedUpdates
from player import Player
from bar import *
from starfield import Starfield
from transitions import Intro, Transition, GameOverScreen, Instructions
from obstacles import *
from user_items import UserPlanet
import sys, os
import system


class Game(object):
    title = 'Gravity'
    screen_size = 1000, 750
    
    def __init__(self,level=0):
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_size)
        if self.title:
            pygame.display.set_caption(self.title)
        self.fps = 30

        #group definitions
        self.userPlacedObjects = Group()
        self.startItems = RenderUpdates()
        self.playerGroup = RenderUpdates()
        self.tails = RenderUpdates()
        self.blackHoles = RenderUpdates()
        self.obstacles = RenderUpdates()
        self.masslessObstacles = RenderUpdates()
        self.goalCollide = Group()
        self.toolbar = OrderedUpdates()

        #level/transition/player & enemy/obstacle creation hocus pocus
        self.goal = Goal(573,372,self.goalCollide,30)
        self.bar = ToolBar(0,626,self.toolbar,self.screen,self,self.goal)
        self.player = Player(50,535,self.screen,(255,0,0),self.playerGroup,1000,624,(2,-2),self.tails,self)
        
        self.level = level
        self.levelUp = True
        self.stars = Starfield(self.screen,1000,626,200)
        BlackHole(339,70,self.blackHoles,self.screen,80,71,16)
        temp = EarthRounder(513,313,self.masslessObstacles,self.screen,40,0)
        temp.rotate(55)
        temp = Alien(60,188,self.masslessObstacles,self.screen,34,1)
        temp.rotate(-15)
        temp = Alien(107,268,self.masslessObstacles,self.screen,35,1)
        temp.rotate(-75)
        temp = Alien(816,533,self.masslessObstacles,self.screen,39,0)
        temp.rotate(-13)
        temp = BlueUpAnDown(811,227,self.masslessObstacles,self.screen,34,1,97,239)
        temp.rotate(80)
        self.obstacles.add(self.blackHoles)
        self.obstacles.add(self.goalCollide)
        self.freeb = False
        self.gotoLevel = level

        if system.thereIsASaveFile() and level == 0:
            self.intro_screen = Intro(0,0,self.startItems,str('title_w_file.png'))
            self.thereIsAFile = True
        elif level == 0:
            self.intro_screen = Intro(0,0,self.startItems)
            self.thereIsAFile = False
      
    def quit(self):
        self.done = True
   
    def level_0(self):
        self.clock.tick(self.fps)
        pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
        
        for evt in pygame.event.get():
            if evt.type == MOUSEBUTTONDOWN:
                print pygame.mouse.get_pos()
            if evt.type == QUIT:
                self.quit()
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    self.quit()
                elif evt.key == K_RETURN:
                    if not self.thereIsAFile:
                        self.transition = Transition(-1314,0,self.screen,self.startItems)
                        self.intro_screen.begin()
                    else:
                        loadingDial = system.Loading()
                        pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
                        self.startItems.draw(self.screen)
                        loadingDial.draw(self.screen)
                        pygame.display.flip()
                        self.loadFile(system.loadFile())
                        
                elif evt.key == K_RIGHT:
                    self.intro_screen.instruct(True)
                elif evt.key == K_LEFT:
                    self.intro_screen.instruct(False)
                elif evt.key == K_n:
                    if self.thereIsAFile:
                        self.intro_screen.begin()
                elif evt.key == K_d:
                    if self.thereIsAFile:
                        os.remove('save.txt')
                        self.thereIsAFile = False
                        self.startItems.empty()
                        self.intro_screen = Intro(0,0,self.startItems)

       
        if self.intro_screen.next_level():
            self.level = 1
        
        
        self.startItems.update()
        self.stars.draw()
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
        self.masslessObstacles.draw(self.screen)
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
                elif evt.key == K_ESCAPE and self.bar.grabbed == None:
                    self.bar.itemsTab.dropped()
                    self.bar.menuWidget.dropped()
                                        
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
            elif evt.type == MOUSEBUTTONUP:
                self.bar.clear_grabbed()
                for obj in self.userPlacedObjects:
                    obj.drop(self.blackHoles)
             

        if self.player.makeANew:
            self.masslessObstacles.update()

     
        self.stars.draw()
        self.player.drawTails()
        self.blackHoles.update()
        self.bar.update(pos)
        self.blackHoles.draw(self.screen)
        self.userPlacedObjects.update(pos)
        self.userPlacedObjects.draw(self.screen)
        self.masslessObstacles.draw(self.screen)
        self.goalCollide.draw(self.screen)
        self.toolbar.draw(self.screen)
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
                
        if pygame.sprite.collide_mask(self.player, self.goal):
            self.next_level()

        for obj in self.blackHoles:
            if pygame.sprite.collide_mask(self.player,obj):
                self.player.blackHoleCollision(True,False)

        for obj in self.masslessObstacles:
            if  pygame.sprite.collide_mask(self.player,obj):
                self.player.update(True)
        
        for obj in self.userPlacedObjects:
            if pygame.sprite.collide_mask(self.player,obj) and not obj.grabbed:
                self.player.update(True)
        

        pygame.display.flip()


    def next_level(self,add_score_bool=True,trans_effect=True):
        if self.level < 2:
            self.level += 1
        if trans_effect: self.transition.add_to_group()
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
                        
            if not trans_effect or self.transition.rect.x >= -50 and not changed:
                if self.level == 2:
                    self.make_level_two(add_score_bool)
                if self.level == 3:
                    self.make_level_three(add_score_bool)
                    print "level 3"

                if add_score_bool:
                    self.bar.score.update(2000)


                self.player.restart(add_score_bool)
                changed = True      

            if not trans_effect:
                break
                
            self.startItems.update()
            self.stars.draw()
            self.player.drawTails()
            self.goalCollide.draw(self.screen)
            self.masslessObstacles.draw(self.screen)
            self.userPlacedObjects.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.blackHoles.draw(self.screen)
            self.playerGroup.draw(self.screen)  
            self.startItems.draw(self.screen)
            if self.transition.rect.x > 1000:
                self.transition.kill()
                break


            pygame.display.flip()
        if trans_effect:
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
            
            
            for obj in self.blackHoles:
                if pygame.sprite.collide_mask(self.player,obj):
                    self.player.blackHoleCollision(True,False)

            for obj in self.masslessObstacles:
                if  pygame.sprite.collide_mask(self.player,obj):
                    self.player.update(True)
        
            for obj in self.userPlacedObjects:
                if pygame.sprite.collide_mask(self.player,obj) and not obj.grabbed:
                    self.player.update(True)
            

            self.startItems.update()
            self.masslessObstacles.update()
            self.stars.draw()
            self.player.drawTails()
            self.goalCollide.draw(self.screen)
            self.masslessObstacles.draw(self.screen)
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
        self.bar.update()
        self.toolbar.draw(self.screen)
        self.over_screen.draw()
        pygame.display.flip()
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
            
            
        
        self.player.add(self.playerGroup)
        self.bar.reset_lives_over()
        self.player.restart()
        self.over_screen.kill()

    def inStructionees(self):
        self.instructions = Instructions(0,-750,self.startItems)
        self.instructions.instruct(True)

        while True:
            self.clock.tick(self.fps)
            pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))

            if self.instructions.instruct and self.instructions.rect.y < 0:
                self.instructions.rect.y += 50

            elif not self.instructions.instruct and self.instructions.rect.y > -750:
                self.instructions.rect.y -= 50
            elif not self.instructions.instruct and self.instructions.rect.y <= -750:
                self.instructions.kill()
                return
            
            
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    self.quit()
                    return
                elif evt.type == KEYDOWN:
                    if evt.key == K_RETURN:
                        self.instructions.instruct = False
                    elif evt.key == K_ESCAPE:
                        self.quit()
                        return

            self.stars.draw()
            self.player.drawTails()
            self.goalCollide.draw(self.screen)
            self.masslessObstacles.draw(self.screen)
            self.userPlacedObjects.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.blackHoles.draw(self.screen)
            self.playerGroup.draw(self.screen)  
            self.startItems.draw(self.screen)
                
            pygame.display.flip()
    
    def saveFile(self):
        save_confirm = GameOverScreen(293,161,self.screen,str('filesaved.png'))
        save_confirm.draw()
        self.bar.menuWidget.dropped()
        system.saveFile(self.level,self.player.lives,self.bar.score.score)
        pygame.display.flip()
        while True:
            self.clock.tick(self.fps)
            pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))

            for evt in pygame.event.get():
                if evt.type == QUIT:
                    self.quit()
                    return
                elif evt.type == KEYDOWN:
                    if evt.key == K_RETURN:
                        return
                    elif evt.key == K_ESCAPE:
                        self.quit()
                        return

            
    def loadFile(self,file_tuple):
        gotoLevel,gotoLives,gotoScore = file_tuple
        self.level = gotoLevel
        self.player.lives = gotoLives
        self.bar.lives.next_life = gotoLives+1
        self.bar.lives_update()
        self.bar.score.reset(gotoScore)
        if gotoLevel != 1:
            self.level -= 1
            self.next_level(False,False)
        self.startItems.empty()
        self.intro_screen = Intro(0,0,self.startItems,str('title_w_file.png'))
        self.intro_screen.begin()
        self.transition = Transition(-1314,0,self.screen,self.startItems)

        while True:
            self.clock.tick(self.fps)
            pygame.draw.rect(self.screen,(0,0,0),((0,0),(1000,750)))
            
            
            if self.intro_screen.next_level():
                break
            
            self.startItems.update()
            self.startItems.update()
            self.stars.draw()
            self.goalCollide.draw(self.screen)
            self.toolbar.draw(self.screen)
            self.masslessObstacles.draw(self.screen)
            self.playerGroup.draw(self.screen)
            self.blackHoles.draw(self.screen)
            self.startItems.draw(self.screen)
            
            
            pygame.display.flip()

        
        
        
    def run(self,level=0):
        self.done = False
        self.clock = pygame.time.Clock()
        if self.gotoLevel > 1 and self.gotoLevel < 4:
            self.transition = Transition(-1314,0,self.screen,self.startItems)
            self.tick()
            self.level = self.gotoLevel
            self.next_level()
        while not self.done:
            while self.level == 0 and not self.done:
                self.level_0()
            while self.level >= 1 and not self.done:
                self.tick()


    def make_level_two(self,reset_lives_bool):
        self.goal.next_level(self.level)
        self.bar.next_level(self.level,reset_lives_bool)
        self.userPlacedObjects.empty()
        self.blackHoles.empty()
        self.obstacles.empty()
        self.freeb = False
        self.bar.itemsTab.earth_item.light()
        self.masslessObstacles.empty()
        temp = Alien(55,143,self.masslessObstacles,self.screen,39,1)
        temp.rotate(-66)
        temp = Alien(189,98,self.masslessObstacles,self.screen,36,1)
        temp.rotate(23)
        temp = Alien(107,228,self.masslessObstacles,self.screen,32,1)
        temp.rotate(17)
        temp = BlueUpAnDown(249,244,self.masslessObstacles,self.screen,41,1,204,245)
        temp.rotate(80)
        temp = TwitchyOnes(898,541,self.masslessObstacles,self.screen,45,2)
        temp.rotate(22)
        temp = TwitchyOnes(730,545,self.masslessObstacles,self.screen,40,2)
        temp.rotate(-30)
        temp = Rotator(525,121,self.masslessObstacles,self.screen,50,0,-70)
        BlackHole(842,388,self.blackHoles,self.screen,80,71,16)
        hole = BlackHole(388,189,self.blackHoles,self.screen,80,71,16)
        hole.flip()
        self.obstacles.add(self.blackHoles)
        self.obstacles.add(self.goal)

    def make_level_three(self,reset_lives_bool):
        self.goal.next_level(self.level)
        self.bar.next_level(self.level,reset_lives_bool)
        self.userPlacedObjects.empty()
        self.blackHoles.empty()
        self.obstacles.empty()
        self.freeb = False
        self.bar.itemsTab.earth_item.light()
        self.masslessObstacles.empty()

        self.obstacles.add(self.goal)

    def make_level_four(self,reset_lives_bool):
        self.goal.next_level(self.level)
        self.bar.next_level(self.level,reset_lives_bool)
        self.userPlacedObjects.empty()
        self.blackHoles.empty()
        self.obstacles.empty()
        self.freeb = False
        self.bar.itemsTab.earth_item.light()
        self.masslessObstacles.empty()
        
        self.obstacles.add(self.goal)

        
    

if len(sys.argv) > 1:
    level = sys.argv[1]
else:
    level = 0

level = int(level)

Game(level).run()

'''////////////Pylygon Methods
#http://www.pygame.org/project-pylygon-1718-.html

////////////TODO
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
