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
    PHYSICS_NEWTON = 3

    def __init__(self, segments, color=pygame.Color('black'), between_color = pygame.Color('Red'), ph=PHYSICS_ROTATION):
        self.segments = []
        for s in segments:
            self.segments.append(s)  # from head to tail
        self.phy = ph
        self.color = color
        self.between_color = between_color

    def draw(self, surface):
        draw_rope(self, surface, self.color, self.between_color)

    def physics(self):
        if self.phy == 1:
            phys.physics_rotation(self)
        elif self.phy == 2:
            phys.physics_elasticity(self)
        elif self.phy == 3:
            phys.physics_newton(self)

    def update(self):
        for seg in self.segments:
            seg.update()
