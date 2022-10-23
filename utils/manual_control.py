import pygame
import numpy as np
import utils.config as cfg
from maths.vector3D import Vector3D

def inc_speed(self):
    self.a_forced = cfg.q_a * Vector3D(np.sin(self.angle), np.cos(self.angle), 0)

def dec_speed(self):
    self.a_forced = 0

def inc_angle(self):
    self.angle_accel = cfg.q_angle_accel

def dec_angle(self):
    self.angle_accel = 0