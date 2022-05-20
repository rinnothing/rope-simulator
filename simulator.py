import numpy as np
import pygame

from objects.segment import Segment
from objects.rope import Rope
from utils.window import Window

g = Window("Test, don't touch!!!", 720, 720, 30)

a = Segment(360, 360, 100, 20, np.pi * (90/180), 1000)
b = Segment(360, 360+50, 100, 20, np.pi * (0/180), 1000)
c = Segment(360, 360, 100, 20, np.pi * (-90/180), 1000)

r = Rope([a, b, c])
g.objects.append(r)


g.run()
