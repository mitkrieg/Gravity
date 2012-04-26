#!/usr/bin/env python
import system
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group
from goal import Goal
from user_items import UserPlanet


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
        self.nextPosition = 0
        self.images = [(str('venus.png'))]
        

class ToolBar(Bar):
    def __init__(self,x,y,friends,place,other,goal,image=str('taskbar.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.lives = Lives(self.rect.x+353,self.rect.y+71,self.group,self.screen,str('5lives.png'))
        self.goRect = pygame.Rect(717,658,118,75)
        self.barGoal = Goal(self.rect.x+605,self.rect.y+70,self.group)
        self.barGoal.resize(40,40)
        self.score = Score(250,665,friends,self.screen,2000,26,(0,0,0))
        self.arrow = Arrow(872,665,friends,self.screen)
        self.menuWidget = MenuWidget(self.rect.x+694,723,self.group,self.screen,self.arrow)
        self.itemsTab = ItemsTab(self.rect.x-912,self.rect.y+15,self.group,self.screen,-917,-954,-3)
        self.game = other
        self.grabbed = None
        self.item_one_reset()
        self.items_one_limit = 1
        self.items_one_placed = 0
        self.items_two_limit = 0
        self.items_two_placed = 0
        self.goal = goal
                
    def lives_over(self):
        self.lives.no_lives()

    def lives_update(self):
        self.lives.update()

    def reset_lives(self):
        self.lives.back_to_three(False)

    def reset_lives_over(self):
        self.lives.back_to_three(True)

    def update(self,pos=(0,0)):
        if self.grabbed != None:
            self.grabbed.update(pos,self)

    def clear_grabbed(self):
        if self.grabbed != None:
            self.grabbed.dropped()
            self.grabbed = None

    def collision_test(self,pos,player,button):
        if self.goRect.collidepoint(pos) and not self.itemsTab.open and not self.menuWidget.open and button == 1:
            player.makeANew = True
        elif self.goRect.collidepoint(pos) and not self.itemsTab.open and not self.menuWidget.open and button == 3:
            return True
        elif self.itemsTab.items_rect.collidepoint(pos) and not self.menuWidget.open:
            self.grabbed = self.itemsTab
        elif self.menuWidget.widget_rect.collidepoint(pos) and not self.itemsTab.open:
            self.grabbed = self.menuWidget
        elif self.menuWidget.quit_rect.collidepoint(pos):
            self.game.quit()
        elif self.items_one.collidepoint(pos) and self.itemsTab.open and self.items_one_placed < self.items_one_limit:
            x,y = pos
            x -= 30
            y -= 30
            self.grabbed = UserPlanet(x,y,60,60,25,self.game.userPlacedObjects,self.group,self.game.obstacles,self,player,1,self.goal,str('rockplanet.png'))
            self.items_one_placed += 1
            if self.items_one_placed >= self.items_one_limit:
                self.items_one.x = -30
                self.itemsTab.rock_item.dark()
        elif self.itemsTab.earth_item.rect.collidepoint(pos) and self.itemsTab.open and self.itemsTab.earth_item and self.items_two_placed < self.items_two_limit:
            x,y = pos
            x -= 30
            y -= 30
            self.grabbed = UserPlanet(x,y,65,65,30,self.game.userPlacedObjects,self.group,self.game.obstacles,self,player,2,self.goal,str('earth.png'))
            self.items_two_placed += 1
            print self.items_two_placed
            if self.items_two_placed >= self.items_two_limit:
                self.itemsTab.earth_item.dark()
        return False

    def item_one_reset(self):
        self.items_one_placed = 0
        self.items_one = pygame.Rect(119,667,55,45)
        self.itemsTab.rock_item.light()

    def item_two_reset(self):
        self.items_two_placed = 0
        self.itemsTab.earth_item.light()
        
    def next_level(self,level):
        self.barGoal.change_image(self.images[self.nextPosition])
        self.barGoal.resize(40,40)
        self.item_one_reset()
        self.reset_lives()
        self.score.update(2000)
        if level == 2:
            self.item_two_reset()
            self.items_two_limit = 1
        
    
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
        self.rock_item = RockItem(x+106,652,friends,place)
        self.earth_item = EarthItem(x+434,652,friends,place)
        self.venus_item = VenusItem(x+720,652,friends,place)

    def update(self,pos,other):
        newx, newy = pos
        if self.rect.x < 2 and self.rect.x >= -912 and not self.open:
            self.rect.x = newx-917
            self.items_rect.x = newx-self.clickOffset
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720
        elif self.rect.x < 2 and self.rect.x >= -912 and self.open:
            self.rect.x = newx-954
            self.items_rect.x = newx-self.clickOffset
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720
        elif self.rect.x > -400:
            self.rect.x = 1
            self.items_rect.x = 914
            self.open = True
            other.grabbed = None
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720
        elif self.rect.x < -400:
            self.rect.x = -912
            self.items_rect.x = 7
            self.open = False
            other.grabbed = None
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720
        
    def dropped(self):
        if self.open == False:
            self.rect.x = 1
            self.items_rect.x = 914
            self.open = True
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720
        else:
            self.rect.x = -912
            self.items_rect.x = 1
            self.open = False
            self.rock_item.rect.x = self.rect.x+106
            self.earth_item.rect.x = self.rect.x+422
            self.venus_item.rect.x = self.rect.x+720

class MenuWidget(Bar):
    def __init__(self,x,y,friends,place,arrow,image=str('widget.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.widget_rect = pygame.Rect(x+188,726,27,21)
        self.quit_rect = pygame.Rect(x+57,887,99,26)
        self.first_open = False
        self.open = False
        self.arrow = arrow
        
      
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
            if not self.first_open:
                self.arrow.kill()
                self.first_open = True
        else:
            self.rect.y = 723
            self.widget_rect.y = 726
            self.open = False

   
class Lives(Bar):
    def __init__(self,x,y,friends,place,image=str('3lives.png')):
        Bar.__init__(self,x,y,friends,place,image)
        self.next_life = 4
        self.five_lives = self.image
        self.life_image = [(str('1life.png')),(str('2lives.png')),
                           (str('3lives.png')),(str('4lives.png')),
                           (str('5lives.png'))]
        
    def update(self):
        self.image = system.load_graphics(self.life_image[self.next_life-1])
        self.next_life -= 1

    def reset(self):
        self.next_life = 4
        self.image = system.load_graphics(self.life_image[self.next_life])

    def back_to_three(self,re_group):
        self.next_life = 4
        self.image = system.load_graphics(self.life_image[self.next_life])
        if re_group:
            self.add(self.group)

    def no_lives(self):
        self.kill()

class Arrow(Bar):
    def __init__(self,x,y,friends,place,image=str('arrow.png')):
        Bar.__init__(self,x,y,friends,place,image)
        

class Item(Bar):
    def __init__(self,x,y,friends,place,image=str('locked_item.png')):
        Bar.__init__(self,x,y,friends,place,image)   
        locked = True

    def dark(self):
        locked = True
        self.image = system.load_graphics(self.img_txt[1])

    def light(self):
        locked = False
        self.image = system.load_graphics(self.img_txt[0])



class RockItem(Item):
    def __init__(self,x,y,friends,place,image=str('rock_item.png')):
        Item.__init__(self,x,y,friends,place,image)
        locked = False
        self.img_txt = [(str('rock_item.png')),(str('rock_item_dark.png'))]


class EarthItem(Item):
    def __init__(self,x,y,friends,place,image=str('locked_item.png')):
        Item.__init__(self,x,y,friends,place,image)
        self.img_txt = [str('earth_item.png'),str('earth_item_dark.png')]


class VenusItem(Item):
    def __init__(self,x,y,friends,place,image=str('locked_item.png')):
        Item.__init__(self,x,y,friends,place,image)
        self.img_txt = [(str('venus_item.png')),(str('venus_item_dark.png'))]
