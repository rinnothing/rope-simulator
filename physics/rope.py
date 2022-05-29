import numpy as np
import utils.config as cfg

def physics_rotation(self):
    for s in self.segments:
        s.F = s.m * cfg.g * np.sin(s.angle)

    x, y = self.x, self.y

    for s in self.segments:
        s.w += -1 * (1/cfg.fps) * s.F * s.l/2 / s.i
        s.angle += s.w * (1/cfg.fps)

        s.set_top_mid(x, y)
        x, y = s.bot_mid

def physics_elasticity(self):
    self.segments[0].angle = 0
    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]

        s1.F2 = cfg.k * (((s1.x-s2.x)**2 + (s1.y-s2.y)**2)**(1/2) - (s1.l/2+s2.l/2))
        s2.F1 = s1.F2

        cos = (s1.x - s2.x) / ((s1.x-s2.x)**2 + (s1.y-s2.y)**2)**(1/2)
        sin = (s1.y - s2.y) / ((s1.x-s2.x)**2 + (s1.y-s2.y)**2)**(1/2)

        s1.speed = (s1.speed[0] - (s1.F2*cos)/s1.m * (1/cfg.fps), s1.speed[1] - (s1.F2*sin)/s1.m * (1/cfg.fps))
        s2.speed = (s2.speed[0] + (s2.F1*cos)/s2.m * (1/cfg.fps), s2.speed[1] + (s2.F1*sin)/s1.m * (1/cfg.fps))

        s2.angle = 0
        if s1.x != s2.x: 
            tg = (s1.y - s2.y)/(s1.x - s2.x)
            s1.angle += (np.pi/2 - np.arctan(tg))/2
            s2.angle += (np.pi/2 - np.arctan(tg))/2

    self.segments[0].speed = (0, -self.segments[0].m * cfg.g)

    for s in self.segments:
        s.x += s.speed[0] * (1/cfg.fps)
        s.y += (s.speed[1] + s.m * cfg.g) * (1/cfg.fps)