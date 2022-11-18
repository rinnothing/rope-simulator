"""Time constants"""
fps = 60  # how many fps window display
upfr = 360  # how many times per second physics updates
upup = 36 #on what updte in order approch is made
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
q_a = 12 #max top acceleration
q_angle_accel = 1 #max angle acceleration
q_v = 100 #max top velocity
q_angle_vel = 3.14 #max angle velocity 

"""Approach constants"""
appr_a_res=1 #what acceleration difference between checks should be
appr_w_res=1/32
speed_w = 2 #weight of speed aspect
dist_w = 2 #weight of height aspect
tgth_w = 200 #weight of taraget heading aspect

"""Autopilot constants"""
req_sp = 10 #what speed required
req_dist = 1 #what distance between lower end of rope and ground required
tgt_x = 30 #what x autopilot oriented to
tgt_y = 40