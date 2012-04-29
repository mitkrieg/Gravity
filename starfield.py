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
            color = randrange(170,250)
            star = [randrange(0,self.width-1),randrange(0,self.height-1),randrange(1,3)]
            star.append((color,color,color))
            self.stars.append(star)

    def draw(self):
        for star in self.stars:
            self.screen.fill(star[3],(star[0],star[1],star[2],star[2]))   

