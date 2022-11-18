import pygame
import numpy as np
import utils.config as cfg
from maths.vector3D import Vector3D
from maths.DWapproach import approach

from .object import Object
from graphics.quadrocopter import draw as draw_quadrocopter

"""
The class describes quadrocopter
"""

class Quadrocopter(Object):

    F = Vector3D(0, 0, 0)

    def __init__(self, x, y, angle, w, h, m, top_speed, angle_speed, color=pygame.Color('grey'), attached_seg=None, attached_rope=None, edges=None):
        self.m = m
        self.w = w
        self.h = h
        self.att_seg = attached_seg
        self.att_rope = attached_rope
        self.angle = angle #from top to right
        self.angle_speed = angle_speed
        self.angle_accel = 0
        self.a = Vector3D(0, 0, 0)
        self.a_forced = Vector3D(0, 0, 0)
        self.edges = edges

        self.counter = 0

        self.color = color

        self.pos = Vector3D(x, y, 0)  # position of the quadrocopter
        self.speed = Vector3D(top_speed * np.sin(angle), top_speed * -np.cos(angle), 0)  # the velocity of the quadrocopter

    def draw(self, surface):
        draw_quadrocopter(self, surface, self.color)
    
    def physics(self):
        approach(self, self.edges)

        if self.att_seg != None:
            self.att_seg.forced_a = self.a_forced - Vector3D(0, cfg.g, 0)

    def update(self):
        self.angle_speed += self.angle_accel * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps))
        self.angle += self.angle_speed * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps))
        
        self.a = self.a_forced - Vector3D(0, cfg.g, 0)
        self.speed += self.a * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps))
        self.pos += self.speed * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps))

    def getbounds(self):
        return ((self.pos.x - self.w/2, self.pos.y - self.h/2), (self.pos.x + self.w/2, self.pos.y - self.h/2), 
        (self.pos.x + self.w/2, self.pos.y + self.h/2), (self.pos.x - self.w/2, self.pos.y + self.h/2))