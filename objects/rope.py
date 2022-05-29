import pygame
import numpy as np

from objects.object import Object
from objects.segment import Segment
from graphics.rope import draw as draw_rope
import physics.rope as phys

"""
The class describes rope (also rope contains rope segments so there is part of their physics)
"""


class Rope(Object):
    PHYSICS_ROTATION = 1
    PHYSICS_ELASTICITY = 2
    
    phy = 0

    segments = []

    def __init__(self, segments, color=pygame.Color('black'), between_color = pygame.Color('Red'), ph=PHYSICS_ROTATION):
        for s in segments:
            self.segments.append(s)  # from head to tail
        self.x, self.y = self.segments[0].top_mid
        global phy
        phy = ph
        self.color = color
        self.between_color = between_color

    def draw(self, surface):
        draw_rope(self, surface, self.color, self.between_color)

    def physics(self):
        global phy
        if phy == 0:
            phys.physics_rotation(self)
        elif phy == 1:
            phys.physics_elasticity(self)

    def update(self):
        for seg in self.segments:
            seg.update()
