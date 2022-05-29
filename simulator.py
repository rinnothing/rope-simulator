import numpy as np
import pygame

import utils.config as cfg
from objects.segment import Segment
from objects.rope import Rope
from utils.window import Window

g = Window("Test, don't touch!!!", cfg.width, cfg.height, cfg.fps)

num = 10

segs = []
for i in range(num):
    segs.append(Segment(360 + i*10, 360, 10, 10, np.pi * (90/180), 10))
'''
a = Segment(360, 360, 100, 20, np.pi * (90/180), 1000)
b = Segment(360, 360+50, 100, 20, np.pi * (0/180), 1000)
c = Segment(360, 360, 100, 20, np.pi * (-90/180), 1000)
'''
r = Rope(segs, ph = 1)
g.objects.append(r)


g.run()
