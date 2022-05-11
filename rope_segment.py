import pygame
import numpy as np

from game_object import GameObject

"""
The class describes rope segment
"""
class Segment(GameObject):
    g = 9.8
    fps = 30
    F1 = 0      #force between previous and this segment
    F2 = 0      #force between next and this segment
    a1 = 0      #angle between next and this segment's lines of symmetry
    a2 = 0      #angle between previous and this segment's lines of symmetry

    def __init__(self, x, y, l, d, angle, m, speed=(0, 0), w = 0, color=pygame.Color('black')):
        self.m = m                          #the mass 
        self.i = 2 * m * (l**2/3 + w**2/2)  #the impulse
        self.innerangle = np.arctan(d/l)    #angle between diagonal and perpendicular to the line of symmetry
        self.l = l                          #the length
        self.d = d                          #the diameter
        self.s = (l**2 + d**2)**(1/2)       #the diagonal

        self.color = color
        
        self.x = x                          #the x coordinate
        self.y = y                          #the y coordinate
        self.angle = angle                  #angle between vertical and the line of symmetry (clockwise)
        self.speed = speed                  #the speed (on x and y coordinate)
        self.w = w                          #the rotation speed (clockwise)
    
    def draw(self, surface):    #some magic that draws rope segment
        pygame.draw.polygon(surface, self.color, [
        (self.x + self.s/2 * np.sin(self.innerangle - self.angle), self.y - self.s/2 * np.cos(self.innerangle - self.angle)), 
        (self.x + self.s/2 * np.sin(self.angle + self.innerangle), self.y + self.s/2 * np.cos(self.angle + self.innerangle)), 
        (self.x - self.s/2 * np.sin(self.innerangle - self.angle), self.y + self.s/2 * np.cos(self.innerangle-self.angle)), 
        (self.x - self.s/2 * np.sin(self.innerangle + self.angle), self.y - self.s/2 * np.cos(self.innerangle + self.angle))])

    def update(self):
        a_parallel = (self.F1 * np.sin(self.a1) - self.F2 * np.sin(self.a2)) / self.m - self.g * np.cos(self.angle)
        a_perpendicular = (self.F1 * np.cos(self.a1) + self.F2 * np.cos(self.a2)) / self.m - self.g * np.sin(self.angle)
        self.speed = (self.speed[0] + a_parallel * np.sin(self.angle) - a_perpendicular * np.cos(self.angle), self.speed[1] -( a_parallel * np.cos(self.angle) + a_perpendicular * np.sin(self.angle)))
        self.w += (-self.F1 * np.cos(self.a1) + self.F2 * np.cos(self.a2)) / self.i 
        
        self.x += self.speed[0] * (1/self.fps)
        self.y += self.speed[1] * (1/self.fps)
        self.angle += self.w * (1/self.fps)
