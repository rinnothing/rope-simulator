import pygame

def draw(self, surface, color):
    tow = []
    bck = []

    for s in self.segments:
        tow.append(s.top_left)
        tow.append(s.bot_left)

        bck.append(s.top_right)
        bck.append(s.bot_right)

        pygame.draw.polygon(surface, color, (s.top_left, s.bot_left, s.bot_right, s.top_right))

    pygame.draw.polygon(surface, color, tow + bck[::-1])