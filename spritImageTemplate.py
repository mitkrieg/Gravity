#!/usr/bin/env python


import os, sys
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, RenderUpdates


def load_graphics(filename):
    fullfname = os.path.join('DIRECTORY_NAME(CHANGE_ME)', filename)
    try:
        image = pygame.image.load(fullfname)
    except pygame.error, message:
        print 'Cannot load', fullfname
        raise SystemExit, message
    return image


class ExampleSprite(Sprite):
    image = None
    def __init__(self,x,y,surf):
        Sprite.__init__(self)
        if self.image is None:
            self.image = load_graphics('IMAGE_FILE(CHANGE_ME).png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.surface = surf
