#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

import math

GRAVITYCO = 1e2

class Player(Sprite):

    def __init__(self,vec,pos,color):
        self.vx,self.vy = vec
        self.vxi,self.vyi = vec
        self.xpos,self.ypos = pos
        self.xi,self.yi = pos
        self.color = color
        self.ax = 0
        self.ay = 0
    
    def resetAccel(self):
        self.ax=0
        self.ay=0
    
    def resetPos(self):
        self.xpos = self.xi
        self.ypos = self.yi
        self.vx = self.vxi
        self.vy = self.vyi
        self.resetAccel()

    def addAccel(self,planet):
        planx,plany = planet.rect.center 
        dx = planx - self.xpos
        dy = plany - self.ypos
        dsq = dx*dx + dy*dy
        dist = math.sqrt(dsq)
        force = GRAVITYCO*planet.mass/dsq if dsq>1e-10 else 0
        self.ax += force*dx/dist
        self.ay += force*dy/dist
        

    def update(self):
        self.xpos += self.vx
        self.ypos += self.vy
        self.vx += self.ax
        self.vy += self.ay
        self.resetAccel()

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(int(self.xpos),int(self.ypos)),2)

    def dead(self):
        pass

class Planet(Sprite):
    
    def __init__(self,mass,pos,color):
        self.mass = mass
        self.xpos,self.ypos = pos
        self.rect = Rect(self.xpos+(self.mass/2),self.ypos+(self.mass/2),self.mass,self.mass)
        self.color = color
    
    def update(self,screen,rect):
        self.rect = rect
        pygame.draw.rect(screen,self.color,rect)

