#!usr/bin/env python

import math
from math import sin,cos,tan

def vec_comp(vec):
    mag,angle = vec
    x = mag*cos(angle)
    y = mag*sin(angle)
    return x,y

def vec_add(*vects):
    xlist = []
    ylist = []
    for vec in vects:
        x,y = vec_comp(vec)
        xlist.append(x)
        ylist.append(y)
    for i in xlist:
        xadd += xlist[i]
        yadd += ylist[i]
    return xadd,yadd

def vector(x,y):
    mag = math.sqrt(x**2+y**2)
    ang = tan(y/x)
    return mag,ang
        
def distance((x1,y1),(x2,y2)):
    dist = math.sqrt((y1-y2)**2+(x1-x2)**2)
    return dist