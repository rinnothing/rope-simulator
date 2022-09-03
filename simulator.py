import numpy as np
import pygame

import utils.config as cfg
from objects.segment import Segment
from objects.rope import Rope
from utils.window import Window

g = Window("Test, don't touch!!!", cfg.width, cfg.height, cfg.fps)

num = 10

segs = []
for i in range(int(num/2)):
    segs.append(Segment(360-i*30, 360+i*40, 10, 50, 10, 0, 0))
for i in range(int(num/2), num):
    segs.append(Segment(360-i*30, 360+(num-i)*40, 10, 50, 10, 0, 0))
'''
a = Segment(360, 360, 100, 20, np.pi * (90/180), 1000)
b = Segment(360, 360+50, 100, 20, np.pi * (0/180), 1000)
c = Segment(360, 360, 100, 20, np.pi * (-90/180), 1000)
'''
segs[0].status = 1
segs[num-1].status = 1
r = Rope(segs, ph=Rope.PHYSICS_NEWTON)

g.objects.append(r)


g.run()
