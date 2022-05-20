import numpy as np
import pygame

from objects.segment import Segment
from objects.rope import Rope
from utils.window import Window

g = Window("Test, don't touch!!!", 720, 720, 30)

a = Segment(360, 360, 50, 20, np.pi * (90/180), 10)
b = Segment(360, 360+50, 50, 20, np.pi * (90/180), 10)

r = Rope([a, b])
g.objects.append(r)


g.run()
