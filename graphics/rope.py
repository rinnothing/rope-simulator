import pygame

def draw(self, surface, color, between_color):
    tow = []
    bck = []

    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]
        pygame.draw.polygon(surface, between_color, (s1.bot_left, s1.bot_right, s2.top_left, s2.top_right))

    for s in self.segments:
        pygame.draw.polygon(surface, color, (s.top_left, s.bot_left, s.bot_right, s.top_right))