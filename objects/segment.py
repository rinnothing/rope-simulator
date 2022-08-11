import pygame
import numpy as np
import utils.config as cfg
from maths.vector3D import Vector3D

from . object import Object

"""
The class describes rope segment
right side attached to previous
left side attached to next
"""
class Segment(Object):
    F = Vector3D(0, 0, 0)
    status = 0 #if 0 - movable, if 1 - constant

    def __init__(self, x, y, r, l, m, velx, vely):
        self.m = m                          #the mass 
        self.i = m * (l**2 / 3 + 4 * r**2 / 8)  #the impulse #recalculate the impulse
        self.l = l                          #the length
        self.r = r                          #the radius
        
        self.pos = Vector3D(x, y, 0)        #position of the segment
        self.speed = Vector3D(velx, vely, 0)#the velocity of the segment

    def update(self):
        if self.status == 0:
            a = self.F / self.m * (cfg.sk / cfg.fps)
            self.pos += a * (cfg.sk / cfg.fps)
        
    def getpos(self):
        return (self.pos.x, self.pos.y)