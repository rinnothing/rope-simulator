import utils.config as cfg
from objects.segment import Segment
from objects.rope import Rope
from objects.edge import Edge
from utils.window import Window
from maths.vector3D import Vector3D
from objects.quadrocopter import Quadrocopter
import utils.manual_control as mancon

g = Window("Test, don't touch!!!", cfg.width, cfg.height, cfg.fps)

num = 50

segs = []
# every segment has these params: x, y, r, l, m, velx, vely
# !!!   Newton physics doesn't use "l" param, so it's highly important to keep an eye on input of the coordinates
# NB    in this physics setting "segments" represent a point masses on the ends of the "sticks" ->
#       -> the length of segment is counted based on the distance between the segments

for i in range(num):
    segs.append(Segment(25 - i * 0.2, 48 - i * 0.5, 0.5, 2, 0.04, 0, 0))

edge = Edge(0, 10, 50, 20)
edges = []
edges.append(edge)

segs[0].status = Segment.CONSTANT
segs[0].forced_a = Vector3D(-2, 0, 0)

r = Rope(segs, ph=Rope.PHYSICS_NEWTON)

quadr = Quadrocopter(segs[0].pos.x, segs[0].pos.y, 0, 1, 1/2, 10, 0, 0, attached_seg = segs[0], attached_rope=r, edges=edges)
g.objects.append(quadr)

g.objects.append(edge)
g.objects.append(r)

g.run()
