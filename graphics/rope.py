import pygame

def draw(self, surface, color, between_color):
    tow = []
    bck = []

    for i in range(len(self.segments)-1):
        pygame.draw.line(surface, between_color, self.segments[i].getpos(), self.segments[i+1].getpos())

    for s in self.segments:
        pygame.draw.circle(surface, color, s.getpos(), s.r)