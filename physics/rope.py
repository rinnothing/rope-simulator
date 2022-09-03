import numpy as np
from maths.vector3D import Vector3D
import utils.config as cfg

def physics_elasticity(self):
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    for i in range(len(self.segments)-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]

        #finding the vector of the spring
        spring = s1.pos - s2.pos
        springlength = spring.length

        #force = dl * k
        if springlength != 0:
            force = -(spring / springlength) * (springlength - (s1.l + s2.l)/2) * cfg.k

            s1.F += force
            s2.F += -force

    g = Vector3D(0, cfg.g, 0)
    for s in self.segments:
        if s.status == s.CONSTANT:
            s.F = Vector3D(0, 0, 0) #if s is constant the force is zero
        else:
            s.F += g * s.m #adding gravity force
            s.F -= s.speed * cfg.ak #adding air resistance force

def physics_newton(self):
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    g = Vector3D(0, cfg.g, 0)
    x = Vector3D(1, 0, 0) #x direction (direction is kind of vector that if you multiply it and number you'll get vector that collinear to direction and has length of number you have multiplied)
    y = Vector3D(0, -1, 0) #y direction (because pygame counts pixels from top left the y coordinate is reverse)

    n = len(self.segments)
    
    #in order to find forces in system we fill the table
    F = np.zeros((3*n-1, 3*n-1))
    S = np.zeros((3*n-1))

    #because there are inextensible string between segments projection of their accelerations on line of string are equal (i will lable projections as smb_p)
    #so a1_p = a2_p => f0_p - f1 + m1g_p = f1 - f2_p + m2g_p => f0_p + f2_p - 2 * f1 = (m2 - m1)g_p but there should be centripetal force
    #so because f1 should increase if centripetal force increased it would be: f0_p + f2_p - 2 * f1 = (m2 - m1)g_p - centr.force

    for i in range(n-1):
        s1 = self.segments[i]
        s2 = self.segments[i+1]
        line = (s1.pos - s2.pos).direction()
        l = (s1.pos-s2.pos).length

        if i != 0:
            F[i][3*i-1] = line.project_k((self.segments[i-1].pos-s1.pos).direction()) #f0_p
            
        if i+1 != n-1:
            F[i][3*i+5] = line.project_k((s2.pos-self.segments[i+2].pos).direction()) #f2_p

        F[i][3*i+2] = -2 # 2 * f1

        #these forces are forces that are used for making constant segments constant, for movable segments their are zero
        F[i][3*i] = line.project_k(x) #x and y are already directions
        F[i][3*i+1] = line.project_k(y)
        F[i][3*(i+1)] = -line.project_k(x)
        F[i][3*(i+1)+1] = -line.project_k(y)
        S[i] = line.project_k((s2.m - s1.m)*g) - line.perpendicular(s1.speed - s2.speed).lengthsq() * 2 / l * s1.m * s2.m / (s1.m + s2.m)
    for i in range(n):
        s = self.segments[i]

        #making forces of compensation zero to movable segments
        if s.status != s.CONSTANT:
            F[n-1+i*2][3*i] = 1
            F[n-1+i*2+1][3*i+1] = 1
            continue
        
        #making constant segmants constant
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

        #adding forces to segments
        if i != 0:
            line = self.segments[i-1].pos - s.pos
            s.F += line.direction() * Forces[3*i-1]
        
        if i != n-1:
            line = s.pos-self.segments[i+1].pos
            s.F -= line.direction() * Forces[3*i+2]

        s.F += x * Forces[3*i]
        s.F += y * Forces[3*i+1]
        s.F += s.m * g #adding gravity force
        s.F -= s.speed * cfg.ak #adding air resistance force