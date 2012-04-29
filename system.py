#!/usr/bin/env python 

import pygame
from pygame.locals import *
import os, sys
import pickle


def load_graphics(filename):
    fullfname = os.path.join('assets', filename)
    try:
        image = pygame.image.load(fullfname)
    except pygame.error, message:
        print 'Cannot load', fullfname
        raise SystemExit, message
    return image


def text_render(text,x,y,color,size, surface):
    font = pygame.font.Font(None, size)
    rend = font.render(text, True, color)
    surface.blit(rend, (x,y))

def text_return(text,color,size):
    font = pygame.font.Font(None, size)
    rend = font.render(text, True, color)
    return rend


def thereIsASaveFile():
    try:
        fil = open('save.txt')
        return True
    except:
        return False


def loadFile():
    if thereIsASaveFile():
        fil = open('save.txt')
        
        p = fil.readline()
        ret = pickle.loads(p)
        return ret 

    return None


def saveFile(level,lives,score):
    if thereIsASaveFile():
        fil = open('save.txt','w')
        
        saveInfo = [level,lives,score]
        s = pickle.dumps(saveInfo)

        fil.write(s)
        fil.close()
        
