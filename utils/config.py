"""Time constants"""
fps = 60  # how many fps window display
upfr = 1000  # how many times per second physics updates
sk = 8  # how many times time speed increased

"""Physical constants"""
g = 9.8  # gravity constant
k = 10000  # spring elasticity constant
ak = 0  # air resistance constant

"""Actual size of terrain"""
# sets a size of the "box" where simulation takes place, units are meters
terra_x = 50
terra_y = 50
aspectRatio = terra_x / terra_y

"""Window parameters"""
width = 800
height = width * aspectRatio

"""Useful constants"""
scale = width / terra_x

"""Quadrocopter constants"""
q_a = 9 #max top acceleration
q_angle_accel = 1/2 #max angle acceleration