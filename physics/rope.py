import numpy as np
from maths.vector3D import Vector3D
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
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]

        spring = s1.pos - s2.pos
        springlength = spring.length

        if springlength != 0:
            force = -(spring / springlength) * (springlength - (s1.l + s2.l)/2) * cfg.k

            s1.F += force
            s2.F += -force

    g = Vector3D(0, cfg.g, 0)
    for s in self.segments:
        s.F += g * s.m

def physics_newton(self):
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    g = Vector3D(0, cfg.g, 0)
    x = Vector3D(1, 0, 0)
    y = Vector3D(0, -1, 0)

    n = len(self.segments)
    
    F = np.zeros((3*n-1, 3*n-1))
    S = np.zeros((3*n-1))

    for i in range(n-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]
        line = (s1.pos - s2.pos).direction()

        if i != 0:
            F[i][3*i-1] = line.project_k((self.segments[i-1].pos-s1.pos).direction())
            
        if i+1 != n-1:
            F[i][3*i+2] = line.project_k((s2.pos-self.segments[i+2].pos).direction())

        F[i][3*i+2] = -2

        F[i][3*i] = line.project_k(x) #x and y are already directions
        F[i][3*i+1] = line.project_k(y)
        F[i][3*(i+1)] = -line.project_k(x)
        F[i][3*(i+1)+1] = -line.project_k(y)
        S[i] = line.project_k((s1.m - s2.m)*g) - line.perpendicular(s2.speed).lengthsq() / (s1.pos-s2.pos).length * s2.m + line.perpendicular(s1.speed).lengthsq() / (s1.pos-s2.pos).length * s1.m

    for i in range(n):
        s = self.segments[i]

        if s.status != 1:
            F[n-1+i*2][3*i] = 1
            F[n-1+i*2+1][3*i+1] = 1
            continue

        if i != 0:
            F[n-1+i*2][3*i-1] = x.project_k((self.segments[i-1].pos-s.pos).direction())
            F[n-1+i*2+1][3*i-1] = y.project_k((self.segments[i-1].pos-s.pos).direction())

        if i != n-1:
            F[n-1+i*2][3*i+2] = -x.project_k((s.pos-self.segments[i+1].pos).direction())
            F[n-1+i*2+1][3*i+2] = -y.project_k((s.pos-self.segments[i+1].pos).direction())

        F[n-1+i*2][3*i] = 1 # = x.project_k(x)
        F[n-1+i*2+1][3*i+1] = 1 # = y.project_k(y)
        S[n-1+i*2+1] = s.m * cfg.g

    Forces = np.linalg.solve(F, S)

    for i in range(n):
        s = self.segments[i]

        if i != 0:
            line = self.segments[i-1].pos - s.pos
            s.F += line.direction() * Forces[3*i-1]
        
        if i != n-1:
            line = s.pos-self.segments[i+1].pos
            s.F -= line.direction() * Forces[3*i+2]

        s.F += x * Forces[3*i]
        s.F += y * Forces[3*i+1]
        s.F += s.m * g