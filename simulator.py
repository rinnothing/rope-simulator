import utils.config as cfg
from objects.segment import Segment
from objects.rope import Rope
from utils.window import Window

g = Window("Test, don't touch!!!", cfg.width, cfg.height, cfg.fps)

num = 50

segs = []
# every segment has these params: x, y, r, l, m, velx, vely
# !!!   Newton physics doesn't use "l" param, so it's highly important to keep an eye on input of the coordinates
# NB    in this physics setting "segments" represent a point masses on the ends of the "sticks" ->
#       -> the length of segment is counted based on the distance between the segments

for i in range(num):
    segs.append(Segment(25 - i * 0.5, 48, 0.5, 2, 0.04, 0, 0))

segs[0].status = Segment.CONSTANT
r = Rope(segs, ph=Rope.PHYSICS_NEWTON)

g.objects.append(r)

g.run()
