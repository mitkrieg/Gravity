#!/usr/bin/env python
import system
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from goal import Goal


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
    def __init__(self,x,y,friends,place,other,image=str('taskbar.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.lives = Lives(self.rect.x+402,self.rect.y+71,self.group,self.screen)
        self.goRect = pygame.Rect(717,658,118,75)
        self.barGoal = Goal(self.rect.x+605,self.rect.y+70,self.group)
        self.barGoal.resize(40,40)
        self.score = Score(250,665,friends,self.screen,1000,26,(0,0,0))
        self.menuWidget = MenuWidget(self.rect.x+690,723,self.group,self.screen)
        self.itemsTab = ItemsTab(self.rect.x-912,self.rect.y+15,self.group,self.screen,-917,-954,-3)
        self.game = other
        self.grabbed = None
                

    def lives_update(self):
        self.lives.update()

    def reset_lives(self):
        self.lives.reset()

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
        elif self.itemsTab.items_rect.collidepoint(pos) and not self.menuWidget.open:
            self.grabbed = self.itemsTab
        elif self.menuWidget.widget_rect.collidepoint(pos) and not self.itemsTab.open:
            self.grabbed = self.menuWidget
        elif self.menuWidget.quit_rect.collidepoint(pos):
            self.game.quit()
        
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
            self.items_rect.x = 7
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
        self.quit_rect = pygame.Rect(747,887,99,26)
        self.open = False
      
    def update(self,pos,other):
        newx, newy = pos
        if self.rect.y <= 723 and self.rect.y > 428 and not self.open:
            self.rect.y = newy-23
            self.widget_rect.y = newy-23
            self.quit_rect.y = 637
        elif self.rect.y <= 723 and self.rect.y > 428 and self.open:
            self.rect.y = newy+1
            self.widget_rect.y = newy-3
            self.quit_rect.y = 1000
        elif self.rect.y > 575:
            self.rect.y = 723
            self.widget_rect.y = 726
            self.open = False
            other.grabbed = None
        elif self.rect.y < 575:
            self.rect.y = 429
            self.widget_rect.y = 431
            self.open = True
            self.quit_rect.y = 642
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

    def reset(self):
        self.next_life = 2
        self.image = self.three_lives
