#!/usr/bin/env python

import pygame
from pygame.locals import *
import math
import physicsobjects
from physicsobjects import *

#Colors
BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
GREEN = 0,255,0
GREY = 80,80,80

#Initial Conditions
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
playerpos = 300,300

#Initiate Screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Phyics")
screen.fill(BLACK)
bounds = screen.get_rect()
write = pygame.font.Font(None,60)

#Clock
FPS = 30
clock = pygame.time.Clock()

done = False
moving = False


#PlanetGroup
planetGroup = [Planet(16,(50,50),GREEN),Planet(50,(100,100),BLUE),Planet(30,(200,200),(90,90,0)),Planet(6,(6,6),(120,40,20))]
grabbed = None
player = Player((1,1),playerpos,RED)

while not done:
    #Input
    x,y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            for planet in planetGroup:
                rect = planet.rect
                if rect.collidepoint(pygame.mouse.get_pos()):
                    grabbed = planet 
                if grabbed:
                    planetGroup.remove(grabbed)
                    planetGroup.append(grabbed)
        elif event.type == MOUSEBUTTONUP:
            grabbed = None
                        
        if event.type == MOUSEBUTTONDOWN and x in range(0,70) and y in range(550,600):
            moving = True
            print moving
        elif event.type == MOUSEBUTTONDOWN and x in range (680,800) and y in range (550,600):
            player.resetPos()
            moving = False
                

    #Update
                
    player.resetAccel()
    if moving:
        for planet in planetGroup:
            player.addAccel(planet)
        player.update()
        player.resetAccel()
    for planet in planetGroup:
        if planet.rect.collidepoint(player.xpos,player.ypos):
            moving = False
            player.resetAccel()
    if player.xpos <= 1 or player.xpos >=799:
        moving = False
        player.resetAccel()
    elif player.xpos <= 1 or player.ypos >=599:
        moving = False
        player.resetAccel()
        

    #Draw
    screen.fill(BLACK)

    pygame.draw.rect(screen,GREY,(0,550,70,50))
    text = write.render("GO", True, BLACK,GREY)
    location = text.get_rect()
    location.bottomleft = bounds.bottomleft
    screen.blit(text, location)

    pygame.draw.rect(screen,GREY,(680,550,120,50))
    text = write.render("RESET", True, BLACK,GREY)
    location = text.get_rect()
    location.bottomright = bounds.bottomright
    screen.blit(text, location)    

    

    for planet in planetGroup:
        others = planetGroup[:]
        others.remove(planet)
        if planet == grabbed:
            planet.rect.center = pygame.mouse.get_pos()
            planet.rect.clamp_ip(bounds) #ip means in place, keeps rectangle w/in bounds
        planet.update(screen,planet.rect)


    player.draw(screen)


    #Refresh
    pygame.display.flip()
    clock.tick()

print "END"
