import numpy as np
from maths.vector3D import Vector3D
import utils.config as cfg

def physics_rotation(self):
    for s in self.segments:
        s.F = s.m * cfg.g * np.sin(s.angle)

    x, y = self.x, self.y

    for s in self.segments:
        s.w += -1 * (1/cfg.fps) * s.F * s.l/2 / s.i
        s.angle += s.w * (1/cfg.fps)

        s.set_top_mid(x, y)
        x, y = s.bot_mid

def physics_elasticity(self):
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]

        spring = s1.pos - s2.pos
        springlength = spring.length

        if springlength != 0:
            force = -(spring / springlength) * (springlength - (s1.l + s2.l)/2) * cfg.k

            s1.F += force
            s2.F += -force

    g = Vector3D(0, cfg.g, 0)
    for s in self.segments:
        s.F += g * s.m

def physics_newton(self):
    g = Vector3D(0, cfg.g, 0)
    for s in self.segments:
        s.F = g * s.m
    
    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]
        if s1.status == 1: 
            continue

        line = s1.pos - s2.pos
        pr = line.project(s1.F)
        
        s1.F -= pr
        s2.F += pr

    for i in range(len(self.segments)-1)[::-1]:
        s1 = self.segments[i-1]
        s2 = self.segments[i]
        if s1.status == 1:
            continue

        line = s1.pos - s2.pos
        pr = line.project(s1.F)

        s1.F -= pr
        s2.F += pr