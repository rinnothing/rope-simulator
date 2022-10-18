import pygame
import utils.config as cfg

sc = cfg.scale


# convert from meters to pixels, invert OY axis
def convToUnit(cords):
    return round(cords[0] * sc), cfg.height - round(cords[1] * sc)


def draw(self, surface, color):
    pygame.draw.line(surface, color, convToUnit(self.getpos()[0]), convToUnit(self.getpos()[1]))