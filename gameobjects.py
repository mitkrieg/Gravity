#!/usr/bin/env python

import pygame
import system
import random
from physics import vec_comp,vector,vec_add,distance
from random import randrange
from pygame.sprite import Sprite, Group

class Player(Sprite):
    image = None
    def __init__(self,x,y,surf,color,group,maxX,maxY,tail):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(str('pnvscaled.png'))
        self.rect = self.image.get_rect()
        self.makeANew = False
        self.rect.x = x
        self.reset = x,y
        self.rect.y = y
        self.screen = surf
        self.goTo = [(4,-3),(3,-3),(3,-1),(3,-1),(1,-3)]
        self.maxX = maxX
        self.maxY = maxY
        self.group = group
        self.add(group)
        self.lives = 3
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
            self.lives -= 1
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
        if self.rect.x > self.maxX-self.rect.w or self.rect.x < 0:
            return False
        elif self.rect.y > self.maxY-self.rect.h or self.rect.y < 0:
            return False
        else:
            return True

    def drawTails(self):
        for tail in self.tailGroup:
            color = tail.color
            for coordinates in tail.tail:
                x,y = coordinates
                pygame.draw.line(self.screen,color,(x+17,y+6),(x+17,y+6),3)

    def getPlayerPos(self):
        return self.rect.x, self.rect.y
            

class Tails(Sprite):
    def __init__(self,group,color):
        Sprite.__init__(self)
        self.tail = []
        self.add(group)
        self.color = color

    def newSpace(self,x,y):
        self.tail.append((x,y))


class Goal(Sprite):
    image = None
    def __init__(self,x,y,group):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics('earth.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.group = group
        self.add(group)



class Bar(Sprite):
    image = None
    def __init__(self,x,y,friends,place,image=str('taskbar.png')):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(friends)
        self.group = friends
        self.score = 1000
        self.screen = place

class ToolBar(Bar):
    def __init__(self,x,y,friends,place,image=str('taskbar.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.lives = Lives(402,697,self.group,self.screen)

    def lives_update(self):
        self.lives.update()
        

class Lives(Bar):
    def __init__(self,x,y,friends,place,image=str('3lives.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.next_life = 2
        self.three_lives = self.image
        self.two_lives = system.load_graphics('2lives.png')
        self.one_life = system.load_graphics('1life.png')
        
    def update(self):
        if self.next_life == 2:
            self.image = self.two_lives
        elif self.next_life == 1:
            self.image = self.one_life
        else:
            self.kill()
        self.next_life -= 1



class Star(object):
    def __init__(self,screen,screenw,screenh,max_stars):
        self.stars = []
        self.screen = screen
        self.height = screenh
        self.width = screenw
        self.max_stars = max_stars
        for i in range(self.max_stars):
            star = [randrange(0,self.width-1),randrange(0,self.height-1),2]
            star.append((170,170,170))
            self.stars.append(star)

    def draw(self):
        for star in self.stars:
            self.screen.fill(star[3],(star[0],star[1],star[2],star[2]))   

class Planet(Sprite)
    image = None
    def __init__(self,x,y,mass,imagetype):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.screen = place
        self.mass = mass

    def pullPlayer(self,x,y):
        dist = distance(self.x,self.y,x,y)
        self.pull = self.mass/dist**2
        return self.pull

    def movePlanet(self):
        pass

    def draw(self):
        pass
