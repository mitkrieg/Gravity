#!/usr/bin/env python
import system
import random
from random import randrange


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

'''
class Planet(Sprite):
    image = None
    def __init__(self,x,y,mass,group,image=str('rockplanet.jpg')):
        Sprite.__init__(self)
        if self.image == None:
            self.image = system.load_graphics(image)
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
'''
