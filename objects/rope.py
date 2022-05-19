import pygame
import numpy as np

from . object import Object
from . segment import Segment
from graphics.rope import draw as draw_rope
from physics.rope import physics as physics_rope

"""
The class describes rope (also rope contains rope segments so there is part of their physics)
"""


class Rope(Object):
    g = 9.8
    segments = []

    def __init__(self, segments, color=pygame.Color('black')):
        for s in segments:
            self.segments.append(s)  # from head to tail
        self.x, self.y = self.segments[0].mid_right
        self.color = color

    def draw(self, surface):
        draw_rope(self, surface, self.color)

    def physics(self):
        physics_rope(self)
   
    def update(self):
        for seg in self.segments:
            seg.update()
