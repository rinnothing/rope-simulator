import pygame
import numpy as np

from game_object import GameObject

class Segment(GameObject):
    g = 9.8
    fps = 30

    def __init__(self, x, y, l, w, angle, m, speed=(0, 0), b = 0, color=pygame.Color('black')):
        self.speed = speed
        self.b = b
        self.angle = angle
        self.innerangle = np.arctan(l/w) #we need it just for drawing
        self.color = color
        self.m = m
        self.x = x
        self.y = y
        self.d = (x**2 + y**2)**(1/2)
        self.l = l
        self.w = w
        self.i = 2 * m * (l**2/3 + w**2/2)
        self.F1 = 0
        self.F2 = 0
        self.a1 = 0
    
    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, [(self.x + self.d/2 * np.sin(self.innerangle - self.angle), self.y - self.d/2 * np.cos(self.innerangle - self.angle)), 
        (self.x + self.d/2 * np.sin(self.angle + self.innerangle), self.y + self.d/2 * np.cos(self.angle + self.innerangle)), 
        (self.x - self.d/2 * np.sin(self.innerangle - self.angle), self.y + self.d/2 * np.cos(self.innerangle-self.angle)), 
        (self.x - self.d/2 * np.sin(self.innerangle + self.angle), self.y - self.d/2 * np.cos(self.innerangle + self.angle))])

    def update(self):
        self.speed = (self.speed[0] + (self.F1-self.F2)*np.sin(self.angle)/self.m*(1/self.fps), self.speed[1] + ((self.F2-self.F1)*np.cos(self.angle)/self.m + self.g)*(1/self.fps))
        self.b += self.F1*np.cos(self.a1) 
        
        self.x += self.speed[0] * (1/self.fps)
        self.y += self.speed[1] * (1/self.fps)
        self.b += self.angle * (1/self.fps)
