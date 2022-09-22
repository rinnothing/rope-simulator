import pygame
import utils.config as cfg

sc = cfg.scale


# convert from meters to pixels, invert OY axis
def convToUnit(cords):
    return round(cords[0] * sc), cfg.height - round(cords[1] * sc)


"""def convertToWindow():"""


def draw(self, surface, color, between_color):
    tow = []
    bck = []

    for i in range(len(self.segments) - 1):
        pygame.draw.line(surface, between_color, convToUnit(self.segments[i].getpos()),
                         convToUnit(self.segments[i + 1].getpos()))

    for s in self.segments:
        pygame.draw.circle(surface, color, convToUnit(s.getpos()), s.r)
