#!/usr/bin/env python
import system
import pygame
from pygame.locals import *
import random
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
        self.newplace = self.goTo[0]



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

    def resize(self,w,h):
        self.image = pygame.transform.scale(self.image,(w,h))

    def change_loc(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def change_image(self,new_image=str('earth.png')):
        self.image = system.load_graphics(new_image)



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
        self.screen = place

class ToolBar(Bar):
    def __init__(self,x,y,friends,place,image=str('taskbar.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.lives = Lives(self.rect.x+402,self.rect.y+71,self.group,self.screen)
        self.goRect = pygame.Rect(717,658,118,75)
        self.barGoal = Goal(self.rect.x+605,self.rect.y+70,self.group)
        self.barGoal.resize(40,40)
        self.score = Score(250,665,friends,self.screen,1000,26,(0,0,0))
        self.menuWidget = MenuWidget(self.rect.x+690,723,self.group,self.screen)
        self.itemsTab = ItemsTab(self.rect.x-912,self.rect.y+15,self.group,self.screen,-917,-954,-3)
        self.grabbed = None
                

    def lives_update(self):
        self.lives.update()

    def update(self,pos):
        if self.grabbed != None:
            self.grabbed.update(pos,self)

    def clear_grabbed(self):
        if self.grabbed != None:
            self.grabbed.dropped()
            self.grabbed = None

    def collision_test(self,pos,player):
        if self.goRect.collidepoint(pos) and not self.itemsTab.open and not self.menuWidget.open:
            player.makeANew = True
        elif self.itemsTab.items_rect.collidepoint(pos):
            self.grabbed = self.itemsTab
        elif self.menuWidget.widget_rect.collidepoint(pos) and not self.itemsTab.open:
            self.grabbed = self.menuWidget
        
class Score(Sprite):
    def __init__(self,x,y,group,surf,start_score,size,color):
        Sprite.__init__(self)
        self.group = group
        self.surface = surf
        self.score = start_score
        self.size = size
        self.color = color
        self.image = system.text_return(str(self.score),self.color,self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(group)

    def update(self,loss):
        self.score += loss
        self.image = system.text_return(str(self.score),self.color,self.size)


class ItemsTab(Bar):
    def __init__(self,x,y,friends,place,x_open_offset,x_closed_offset,click_offset,image=str('items_tab.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.items_rect = pygame.Rect(1,643,40,104)
        self.open = False
        self.xOpenOffset = x_open_offset
        self.xClosedOffset = x_closed_offset
        self.clickOffset = click_offset

    def update(self,pos,other):
        newx, newy = pos
        if self.rect.x < 2 and self.rect.x >= -912 and not self.open:
            self.rect.x = newx-917
            self.items_rect.x = newx-self.clickOffset
        elif self.rect.x < 2 and self.rect.x >= -912 and self.open:
            self.rect.x = newx-954
            self.items_rect.x = newx-self.clickOffset
        elif self.rect.x > -400:
            self.rect.x = 1
            self.items_rect.x = 914
            self.open = True
            other.grabbed = None
        elif self.rect.x < -400:
            self.rect.x = -912
            self.open = False
            other.grabbed = None
        
    def dropped(self):
        if self.open == False:
            self.rect.x = 1
            self.items_rect.x = 914
            self.open = True
        else:
            self.rect.x = -912
            self.items_rect.x = 1
            self.open = False

class MenuWidget(Bar):
    def __init__(self,x,y,friends,place,image=str('widget.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.widget_rect = pygame.Rect(878,726,27,21)
        self.open = False
      
    def update(self,pos,other):
        newx, newy = pos
        if self.rect.y <= 723 and self.rect.y > 428 and not self.open:
            self.rect.y = newy-23
            self.widget_rect.y = newy-23
        elif self.rect.y <= 723 and self.rect.y > 428 and self.open:
            self.rect.y = newy+1
            self.widget_rect.y = newy-3
        elif self.rect.y > 575:
            self.rect.y = 723
            self.widget_rect.y = 726
            self.open = False
            other.grabbed = None
        elif self.rect.y < 575:
            self.rect.y = 429
            self.widget_rect.y = 431
            self.open = True
            other.grabbed = None

    def dropped(self):
        if not self.open:
            self.rect.y = 429
            self.widget_rect.y = 431
            self.open = True
        else:
            self.rect.y = 723
            self.widget_rect.y = 726
            self.open = False

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


class Starfield(object):
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

class Planet(Sprite):
    image = None
    def __init__(self,x,y,mass,imagetype,group):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.group = group
        self.add(self.group)
                #self.screen = place
        self.mass = mass

    def pullPlayer(self,x,y):
        dist = distance(self.x,self.y,x,y)
        self.pull = self.mass/dist**2
        return self.pull
        pass

    def movePlanet(self):
        pass
