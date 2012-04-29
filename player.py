#!/usr/bin/env python
import system
import pygame
import math
from pygame.locals import *
from pygame.sprite import Sprite, Group

class Player(Sprite):
    gravity_co = 1e2
    image = None
    def __init__(self,x,y,surf,color,group,maxX,maxY,start_vec,tail,game):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(str('pnvscaled.png'))
        self.rect = self.image.get_rect()
        self.makeANew = False
        self.rect.x = x
        self.reset = x,y
        self.rect.y = y
        self.screen = surf
        self.maxX = maxX
        self.maxY = maxY
        self.group = group
        self.add(group)
        self.lives = 5
        self.tailGroup = tail
        self.tailColorCounter = 0
        self.tailColors = [(0,0,255),(0,114,54),(255,255,0),(237,28,36),(199,178,153),(158,0,93)]
        self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])
        self.addTail = True
        self.alive = True
        self.shrink = False
        self.shrinkw = self.rect.w
        self.shrinkh = self.rect.h
        self.shrinkx = self.rect.x
        self.shrinky = self.rect.y
        self.shrinkTime = True
        self.backup = self.image
        self.start_vec = start_vec
        self.vx,self.vy = start_vec
        self.vxi,self.vyi = start_vec
        self.ax = 0
        self.ay = 0
        self.game = game
        self.imageBackup = self.image
            
    def resetAccel(self):
        self.ax=0
        self.ay=0
        
    def addAccel(self,planet):
        planx,plany = planet.rect.center 
        dx = planx - self.rect.x
        dy = plany - self.rect.y
        dsq = dx*dx + dy*dy
        dist = math.sqrt(dsq)
        force = self.gravity_co*planet.mass/dsq if dsq>1e-10 else 0
        self.ax += force*dx/dist
        self.ay += force*dy/dist

    def update(self,boo=False,accel_group = None):
        self.dead(boo)
        if self.shrink and self.shrinkw > 5:
            if self.shrinkTime:
                self.shrinkw -= 1
                self.shrinkh -= 1
                foo = pygame.transform.scale(self.image,(self.shrinkw,self.shrinkh))
                foo = pygame.transform.rotate(foo,30)
                self.rect.x += self.ax
                self.rect.y += self.ay
                self.image = foo
                self.shrinkTime = False
                return
            else:
                self.shrinkTime = True
        elif self.shrink:
            self.image = self.backup
            self.shrinkReset()
            self.blackHoleCollision(False,True,True)

            if self.tailColorCounter == 5:
                self.tailColorCounter = 0
            else:
                self.tailColorCounter += 1
            pygame.time.delay(1000)
            self.rect.x, self.rect.y = self.reset
            self.makeANew = False
            self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])
            self.remove(self.group)
            self.resetAccel()
            self.vx,self.vy = self.start_vec
            self.vxi,self.vyi = self.start_vec
            self.alive = True

        if not self.alive:
            self.image = self.imageBackup
            if self.tailColorCounter == 5:
                self.tailColorCounter = 0
            else:
                self.tailColorCounter += 1
            pygame.time.delay(1000)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.reset
            self.makeANew = False
            self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])
            self.remove(self.group)
            self.resetAccel()
            self.vx,self.vy = self.start_vec
            self.vxi,self.vyi = self.start_vec
            self.alive = True
           
            
        elif self.makeANew:
            if accel_group == None:
                grouposo = self.game.obstacles
            else:
                grouposo = accel_group
            
            self.resetAccel()
            for planet in grouposo:
                self.addAccel(planet)
            if self.addTail:
                self.tail.newSpace(self.rect.x,self.rect.y,self.ax,self.ay)
            
            slope = (self.vy-self.ay)/(self.vx-self.ax)
            self.angle = ((math.atan(slope)*(180/math.pi))+45)
            
            #print rot
            if not self.shrink:
                centaur = self.rect.center
                self.image = pygame.transform.rotate(self.imageBackup,(self.angle*-1))
                self.rect = self.image.get_rect()
                self.rect.center = centaur
            self.rect.x += self.vx
            self.rect.y += self.vy
            self.vx += self.ax
            self.vy += self.ay
            
            
    def refresh(self,newplace):
        self.newplace = self.goTo[newplace]

    def blackHoleCollision(self,shrink,tail,boo=False):
        self.shrink = shrink
        self.addTail = tail
        self.update(boo)
        

    def dead(self, boo):
        if self.rect.x > self.maxX-self.rect.w or self.rect.x < 0:
            self.alive = False
            #print "oob"
        elif self.rect.y > self.maxY-self.rect.h or self.rect.y < 0:
            self.alive = False
            #print "oob"
        elif not boo:
            self.alive =  True
        else:
            self.alive = False

    def drawTails(self):
        for tail in self.tailGroup:
            color = tail.color
            for coordinates in tail.tail:
                x,y,w,h = coordinates
                pygame.draw.line(self.screen,color,(x+17,y+6),(x+18,y+8),3)

    def getPlayerPos(self):
        return self.rect.x, self.rect.y

    def shrinkReset(self):
        self.shrinkTime = True
        self.shrinkw = self.rect.w
        self.shrinkh = self.rect.h
            
    def restart(self):
        self.image = self.imageBackup
        self.rect = self.image.get_rect()
        x,y = self.reset
        self.rect.x = x
        self.rect.y = y
        self.tailGroup.empty()
        self.tail = Tails(self.tailGroup,self.tailColors[self.tailColorCounter])
        self.makeANew = False
        self.addTail = True  
        self.lives = 5
        self.resetAccel()
        self.vx,self.vy = self.start_vec
        self.vxi,self.vyi = self.start_vec


class Tails(Sprite):
    def __init__(self,group,color):
        Sprite.__init__(self)
        self.tail = []
        self.add(group)
        self.color = color

    def newSpace(self,x,y,w,h):
        self.tail.append((x,y,w,h))

    def reset(self):
        self.tail = []
