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

        s1.speed = (s1.speed[0] - (s1.F2*cos)/s1.m * cfg.ak * (1/cfg.fps), s1.speed[1] - ((s1.F2*sin)/s1.m - cfg.g/2) * cfg.ak * (1/cfg.fps))
        s2.speed = (s2.speed[0] + (s2.F1*cos)/s2.m * cfg.ak * (1/cfg.fps), s2.speed[1] + ((s2.F1*sin)/s1.m + cfg.g/2) * cfg.ak * (1/cfg.fps))

        s2.angle = 0
        if s1.x != s2.x: 
            tg = (s1.y - s2.y)/(s1.x - s2.x)
            s1.angle += (np.pi/2 - np.arctan(tg))/2
            s2.angle += (np.pi/2 - np.arctan(tg))/2

    self.segments[0].speed = (0, 0)

    for s in self.segments:
        s.x += s.speed[0] * (1/cfg.fps)
        s.y += s.speed[1] * (1/cfg.fps)

def physics_newton(self):
    V = np.zeros((len(self.segments)+1, len(self.segments)+1))
    S = np.zeros(len(self.segments)+1)
    a = np.zeros(len(self.segments)+1)
    for i in range(1, len(self.segments)):
        a[i] = np.pi - (self.segments[i-1].angle-self.segments[i].angle)
    a[0] = np.pi - a[1]

    """ for 3 pieces:

        F1  F2  F3  S
    1   
    2
    3

    """
    #first force is (bad code) (we dont need it)
    V[0][0] = 1
    V[0][1] = np.cos(a[1])
    S[0] = self.segments[0].m * cfg.g * np.cos(self.segments[0].angle)
    #last force is zero
    V[len(V)-1][len(V)-1] = 1
    for i in range(1, len(self.segments)):
        s1 = self.segments[i-1]
        s2 = self.segments[i]

        V[i][i-1] = (-np.cos(a[i-1])*np.sin(a[i]/2) -np.sin(a[i-1])*np.cos(a[i]/2)) / s1.m
        V[i][i] = (np.cos(a[i])*np.sin(a[i]/2) -np.sin(a[i])*np.cos(a[i]/2)) / s1.m + (np.cos(a[i])*np.sin(a[i]/2) -np.sin(a[i])*np.cos(a[i]/2)) / s2.m
        V[i][i+1] = (-np.cos(a[i+1])*np.sin(a[i]/2) -np.sin(a[i]+1)*np.cos(a[i]/2)) / s2.m
        S[i] = -(-np.cos(s1.angle)*np.sin(a[i]/2) +np.sin(s1.angle)*np.cos(a[i]/2) +np.cos(s2.angle)*np.sin(a[i]/2) +np.sin(s2.angle)*np.cos(a[i]/2)) * cfg.g

    F = np.linalg.solve(V, S)

    for i in range(len(F)-1):
        self.segments[i].F1 = F[i]
        self.segments[i].F2 = F[i+1]

    s = self.segments[0] 
    b = (s.F2 * np.sin(a[1])*s.l - s.m*cfg.g*np.sin(s.angle)*s.l/2)/s.i
    s.w += b * (1/cfg.fps)
    s.angle += s.w * (1/cfg.fps)
    s.set_top_mid(self.x, self.y)

    for i in range(1, len(self.segments)):
        s = self.segments[i]
        
        ax = (-s.F1*np.cos(a[i]) +s.F2*np.cos(a[i+1])) * np.sin(s.angle) - (s.F1*np.sin(a[i]) +s.F2*np.sin(a[i]+1)) * np.cos(s.angle)
        ay = (-s.F1*np.cos(a[i]) +s.F2*np.cos(a[i+1])) * np.cos(s.angle) + (s.F1*np.sin(a[i]) +s.F2*np.sin(a[i]+1)) * np.sin(s.angle) + cfg.g
        b = (-s.F1*np.sin(a[i])+s.F2*np.sin(a[i+1])) * s.l/2 / s.i

        s.speed = (s.speed[0] + ax*(1/cfg.fps), s.speed[1] + ay*(1/cfg.fps))
        s.w += b * (1/cfg.fps)

        s.x += s.speed[0]*(1/cfg.fps)
        s.y += s.speed[1]*(1/cfg.fps)
        s.angle += s.w*(1/cfg.fps)