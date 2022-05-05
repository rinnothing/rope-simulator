import pygame
import numpy as np

from poly_object import PolyObject
from rope_segment import Segment

class Rope(PolyObject):
    g = 9.8
    
    def __init__(self, segments):
        self.segments = []
        for s in segments:
            self.segments.append(s) #from head to tail

    def draw(self, surface):
        for seg in self.segments:
            seg.draw(surface)
    
    def physics(self):
        f = np.zeros((len(self.segments)*2, len(self.segments)*2))
        s = np.zeros(len(self.segments)*2)
        """ for 2 segments it's like 
                F11 F12 F21         F22 |   s
            1   1   -1  0           0   |   0            
            2   0   -1  sin(a1-a2)  0   |   0
            3   2   -2  -2          2   |   m2g/cos(a2)
            4   0   0   0           1   |   0
        """
        f[len(f)-1][len(f)-1] = 1
        f[0][0] = 1
        f[0][1] = -1
        for i in range(len(f)-2, 0, -2):
                f[i-1][i-2] = 2
                f[i-1][i-1] = -2
                f[i-1][i] = -2
                f[i-1][i+1] = 2
                s[i-1] = self.segments[i//2].m * self.g / np.cos(self.segments[i//2].angle)

                f[i][i-1] = np.sin(self.segments[i//2].angle - self.segments[i//2-1].angle)
                f[i][i] = -1
        """
        for i in range(len(f)):
            for j in range(len(f)):
                print(f[i][j], end=' ')
            print(s[i], end='\n')
        """
        F = np.linalg.solve(f, s)

        for i in range(len(self.segments)):
            self.segments[i].F2 = F[i*2]
            self.segments[i].F1 = F[i*2+1]
    
    def update(self):
        for i in range(1, len(self.segments)):
            self.segments[i].a1 = self.segments[i-1].angle - self.segments[i].angle

        for seg in self.segments:
            seg.update()