#!/usr/bin/env python

import pygame
import utils
from pygame.sprite import Sprite, Group

class Player(Sprite):
    image = None
    def __init__(self,x,y,surf,color,group,maxX,maxY,tail):
        Sprite.__init__(self)
        if self.image == None:
            self.image = utils.load_graphics(str('player.png'))
        self.rect = self.image.get_rect()
        self.makeANew = False
        self.rect.x = x
        self.reset = x,y
        self.rect.y = y
        self.screen = surf
        self.goTo = [(4,-3),(4,-4),(4,-2),(4,-1),(4,-6)]
        self.maxX = maxX
        self.maxY = maxY
        self.group = group
        self.add(group)
        self.tailGroup = tail
        self.tailColorCounter = 0
        self.tailColors = [(0,0,255),(0,114,54),(255,255,0),(237,28,36),(199,178,153),(158,0,93)]
        self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])



    def update(self):
        self.alive = self.dead()
        if not self.alive:
            if self.tailColorCounter == len(self.tailColors)-1:
                self.tailColorCounter = 0
            else:
                self.tailColorCounter += 1
            pygame.time.delay(1000)
            self.rect.x, self.rect.y = self.reset
            self.makeANew = False
            self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])
            self.remove(self.group)
            
        elif self.makeANew:
            self.tail.newSpace(self.rect.x,self.rect.y)
            newX, newY = self.newplace
            self.rect.x += newX
            self.rect.y += newY
            
    def refresh(self,newplace):
        self.makeANew = True
        self.newplace = self.goTo[newplace]
        

    def dead(self):
        if self.rect.x > self.maxX or self.rect.x < 0:
            return False
        elif self.rect.y > self.maxY or self.rect.y < 0:
            return False
        else:
            return True

    def drawTails(self):
        for tail in self.tailGroup:
            color = tail.color
            for coordinates in tail.tail:
                x,y = coordinates
                pygame.draw.line(self.screen,color,(x+20,y+4),(x+20,y+4),3)              
            




class Tails(Sprite):
    def __init__(self,group,color):
        Sprite.__init__(self)
        self.tail = []
        self.add(group)
        self.color = color

    def newSpace(self,x,y):
        self.tail.append((x,y))
