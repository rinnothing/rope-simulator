import pygame
import utils.config as cfg
from maths.vector3D import Vector3D
import numpy as np

sc = cfg.scale


# convert from meters to pixels, invert OY axis
def convToUnit(cords):
    return round(cords[0] * sc), cfg.height - round(cords[1] * sc)

def draw(self, surface, color):
    pre_points = self.getbounds()
    points = []
    for i in range(len(pre_points)):
        points.append([0, 0])
        points[i][0] = self.pos.x + (pre_points[i][0] - self.pos.x) * np.cos(self.angle) + (pre_points[i][1] - self.pos.y) * np.sin(self.angle)
        points[i][1] = self.pos.y + (pre_points[i][1] - self.pos.y) * np.cos(self.angle) - (pre_points[i][0] - self.pos.x) * np.sin(self.angle)
        points[i] = convToUnit(points[i])

    pygame.draw.polygon(surface, color, points)