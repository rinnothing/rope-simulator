import math

import numpy as np
from maths.vector3D import Vector3D
import utils.config as cfg


# OX axis is oriented from left side of the screen to the right
# OY axis is oriented from bottom side of the screen to the top

def calc_newton(self):
    for s in self.segments:
        s.F = Vector3D(0, 0, 0)

    g = Vector3D(0, cfg.g, 0)
    x = Vector3D(1, 0,
                 0)  # unit vector along OX axis (vector such that if you multiply it by a number N you'll get a vector
    # that is collinear to the vector and has a length of N)
    y = Vector3D(0, 1, 0)  # unit vector along OY axis

    n = len(self.segments)

    # The string between two segments is considered inextensible
    # therefore projections of segments' accelerations are equal  on the line connecting them
    # (projections are named as *_p)
    # because of this:
    # a1_p = a2_p => f0_p - f1 + m1g_p = f1 - f2_p + m2g_p => f0_p + f2_p - 2 * f1 = (m2 - m1)g_p
    # but there should be centripetal force so because f1 should increase
    # if centripetal force increased it would be: f0_p + f2_p - 2 * f1 = (m2 - m1)g_p - centr.force

    # in order to find forces in system we fill the matrix
    F = np.zeros((n - 1, n - 1))
    S = np.zeros(n - 1)
    # | F_1 F_2 F_3 F_4 F_5 F_6 ... F_n-2 F_n-1 |
    # |                                         | (sum of constant forces for 1st segment)
    # |                                         | (sum of constant forces for 2nd segment)
    # |                                         | (sum of constant forces for 3rd segment)
    # |                                         | ( .... )
    # |                                         | (sum of constant forces for n-2 segment)
    # |                                         | (sum of constant forces for n-1 segment)
    # |                                         | (sum of constant forces for  n  segment)

    for i in range(0, n - 1):
        s_i1 = self.segments[i]
        s_i2 = self.segments[i + 1]
        line = (s_i1.pos - s_i2.pos).direction()
        l = (s_i1.pos - s_i2.pos).length

        if i != 0:
            s_i0 = self.segments[i - 1]
            F[i][i - 1] = line.project_k((s_i0.pos - s_i1.pos).direction()) * s_i2.m  # f_i-1_p
            #S[i] += - line.project(line.perpendicular(s_i0.speed - s_i1.speed)).lengthsq() / l * s_i2.m

        F[i][i] = -(s_i1.m + s_i2.m)  # 2 * f
        #S[i] += (s_i1.speed - s_i2.speed).lengthsq() / l * (s_i1.m + s_i2.m)
        S[i] += line.project_k(s_i2.forced_a - s_i1.forced_a) * line.length * s_i1.m * s_i2.m

        if i != n - 2:
            s_i3 = self.segments[i + 2]
            F[i][i + 1] = line.project_k((s_i2.pos - s_i3.pos).direction()) * s_i1.m  # f_i+1_p
            #S[i] += - line.project(line.perpendicular(s_i2.speed - s_i3.speed)).lengthsq() / l * s_i1.m

    # for i in range(n - 1):
    #     s = self.segments[i]
    #     line = (s.pos - self.segments[i + 1].pos).direction()
    #     l = (s.pos - self.segments[i + 1].pos).length
    #     if s.forced_a.lengthsq() != 0:
    #         if i != 0:
    #             F[i][i - 1] = 1
    #             S[i] += - line.project(line.perpendicular(self.segments[i - 1].speed - s.speed)).lengthsq() / l
    #         if i != n - 1:
    #             F[i][i + 1] = -1
    #             S[i] += line.project(
    #                 line.perpendicular(self.segments[i + 1].speed - self.segments[i + 2].speed)).lengthsq() / l
    #         S[i] = (line.project(s.forced_a - g)).length * (s.m + self.segments[i + 1].m)

    # print(F)

    Forces = np.linalg.solve(F, S)
    return Forces


def physics_newton(self):
    g = Vector3D(0, cfg.g, 0)
    x = Vector3D(1, 0, 0)
    y = Vector3D(0, 1, 0)

    n = len(self.segments)

    Forces = calc_newton(self)

    for i in range(n):
        s = self.segments[i]

        # adding forces to segments
        if i != 0:
            line = self.segments[i - 1].pos - s.pos
            s.F += line.direction() * Forces[i-1]

        if i != n - 1:
            line = s.pos - self.segments[i + 1].pos
            s.F -= line.direction() * Forces[i]

        s.F += s.forced_a * s.m
        s.F += s.m * g  # adding gravity force
        s.F -= s.speed * cfg.ak  # adding air resistance force
