import pygame
import numpy as np
from maths.vector3D import Vector3D
from objects.object import Object
from graphics.edge import draw as draw_edge

class Edge(Object):

    def __init__(self, x1, y1, x2, y2, color=pygame.Color('black')):
        self.color = color

        self.pos1 = Vector3D(x1, y1, 0)
        self.pos2 = Vector3D(x2, y2, 0)

    def draw(self, surface):
        draw_edge(self, surface, self.color)

    def getpos(self):
        return (self.pos1.x, self.pos1.y), (self.pos2.x, self.pos2.y)

    def distance(self, pos):
        return abs(((self.pos2.y-self.pos1.y)*pos.x - (self.pos2.x-self.pos1.y)*pos.y - self.pos2.y*self.pos1.x + self.pos2.x*self.pos1.y) / ( (self.pos2.y-self.pos1.y)**2 + (self.pos2.x-self.pos1.x)**2)**(1/2))

    def p_vec(self):
        return Vector3D(self.pos2.x-self.pos1.x, self.pos2.y-self.pos1.y, 0)