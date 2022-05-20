import numpy as np

def physics(self):
    for s in self.segments:
        s.F = s.m * s.g * np.sin(s.angle)

    x, y = self.x, self.y

    for s in self.segments:
        s.w += -1 * s.fps * s.F * s.l/2 / s.i
        s.angle += s.w * (1/s.fps)

        s.set_mid_right(x, y)
        x, y = s.mid_left