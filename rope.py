import pygame
import numpy as np

from poly_object import PolyObject
from rope_segment import Segment

"""
The class describes rope (also rope contains rope segments so there is part of their physics)
"""
class Rope(PolyObject):
    g = 9.8
    segments = []
    
    def __init__(self, segments):
        for s in segments:
            self.segments.append(s) #from head to tail
        segments[0].g = 0

    def draw(self, surface):
        for seg in self.segments:
            seg.draw(surface)
    
    def physics(self):
        f = np.zeros((len(self.segments)+1, len(self.segments)+1))
        s = np.zeros(len(self.segments)+1)
        """ for 2 segments it's like 
                F1          F2          F3          |   s
            1   sin(da1)    -sin(da0)   0           |   mg*cos(a1)*sin(da1)*sin(da0)            
            2   0           sin(da2)    -sin(da1)   |   mg*cos(a2)*sin(da2)*sin(da1)
            3   0           0           1           |   0
        """
        f[len(f)-1][len(f)-1] = 1
        self.segments[0].a1 = -self.segments[0].a2
        f[0][0] = 1
        f[0][1] = -1
        
        for i in range(len(f)-2, 0, -1):
            s1 = self.segments[i-1]
            s2 = self.segments[i]

            s[i] = s1.m * s1.g * (np.cos(s1.angle)*np.sin(s1.a2)  - np.sin(s1.angle)*np.cos(s1.a2)) + s2.m * s2.g * (np.cos(s2.angle)*np.sin(s2.a1)  - np.sin(s2.angle)*np.cos(s2.a1))
            f[i][i+1] = - np.sin(s2.a2) * np.sin(s2.a1) - np.cos(s2.a2) * np.cos(s2.a1)
            f[i][i] = - np.sin(s1.a2)**2 - np.cos(s1.a2)**2 + np.sin(s2.a1)**2 - np.cos(s2.a1)**2
            f[i][i-1] = np.sin(s1.a1) * np.sin(s1.a2) - np.cos(s1.a1) * np.cos(s1.a2)
        """
        for i in range(len(f)):
            for j in range(len(f)):
                print(f[i][j], end=' ')
            print(s[i], end='\n')
        """
        F = np.linalg.solve(f, s)

        for i in range(len(self.segments)):
            self.segments[i].F2 = F[i+1]
            self.segments[i].F1 = F[i]
    
    def update(self):
        self.segments[0].a1 = np.pi - self.segments[0].angle/2
        for i in range(1, len(self.segments)):
            self.segments[i-1].a2 = np.pi/2 - self.segments[i].angle/2 + self.segments[i-1].angle/2
            self.segments[i].a1 = self.segments[i-1].a2 

        for seg in self.segments:
            seg.update()