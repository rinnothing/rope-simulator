import numpy as np
import pygame

from rope_segment import Segment
from rope import Rope
from game import Game

g = Game("Test, don't touch!!!", 720, 720, 30)

a = Segment(360, 360, 50, 20, np.pi * (0/180), 10, color=pygame.Color('red'))
b = Segment(360, 360+50, 50, 10, np.pi * (45/180), 10, color=pygame.Color('blue'))

r = Rope([a, b])
g.objects.append(r)

g.run()