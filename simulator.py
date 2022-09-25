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

segs[0].status = Segment.CONSTANT
segs[num-1].status = Segment.CONSTANT
r = Rope(segs, ph=Rope.PHYSICS_NEWTON)

g.objects.append(r)

segsn = []
for i in range(int(num/2)):
    segsn.append(Segment(360-i*30, 360+i*40, 10, 50, 10, 0, 0))
for i in range(int(num/2), num):
    segsn.append((Segment(360-i*30, 360+(num-i)*40, 10, 50, 10, 0, 0)))

segsn[0].status = Segment.CONSTANT
segsn[num-1].status = Segment.CONSTANT
rn = Rope(segsn, ph=Rope.PHYSICS_ELASTICITY, color=pygame.Color('green'), between_color=pygame.Color('blue'))

g.objects.append(rn)

g.run()
