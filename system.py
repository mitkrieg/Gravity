#!/usr/bin/env python 

import pygame
from pygame.locals import *
import os, sys


def load_graphics(filename):
    fullfname = os.path.join('assets', filename)
    try:
        image = pygame.image.load(fullfname)
    except pygame.error, message:
        print 'Cannot load', fullfname
        raise SystemExit, message
    return image
