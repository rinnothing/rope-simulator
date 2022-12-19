import numpy as np
from maths.vector3D import Vector3D
import utils.config as cfg
from physics.rope import calc_newton
from objects.edge import Edge

def approach(self, edges):
    if self.counter %  cfg.upup != 0:
        self.counter += 1
        return 
    
    self.counter += 1

    quadr_orient = Vector3D(np.sin(self.angle), np.cos(self.angle), 0)
    acc_window = (0, min(cfg.q_a, (cfg.q_v - (quadr_orient.project(self.speed).length))/(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)))
    w_window = (-min(cfg.q_angle_accel, (cfg.q_angle_vel - self.angle_speed)/(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)), min(cfg.q_angle_accel, (cfg.q_angle_vel - self.angle_speed)/(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)))
    
    ch_table = []

    for w in np.arange(w_window[0], w_window[1], cfg.appr_w_res):
        for acc in np.arange(acc_window[0], acc_window[1], cfg.appr_a_res):
            pred_pos, pred_vel = predict_cords(self.att_rope, Vector3D(np.sin(self.angle + (self.angle_speed + w/2*(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)) * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)), 
            np.cos(self.angle + (self.angle_speed + w/2*(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)) * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)), 0)*acc)

            if not(save_check(self, pred_pos, pred_vel, edges)):
                continue

            #ch_table.append([acc, w, cfg.speed_w*speed_proximity(self, pred_vel) + cfg.dist_w*distance_proximity(self, pred_pos, edges) + cfg.tgth_w*heading_proximity(self)])
            ch_table.append([acc, w, cfg.tgth_w*heading_proximity(self, pred_pos)])

    best_sp = ()
    max_sum = 0
    for i in ch_table:
        if i[2] > max_sum:
            max_sum = i[2]
            best_sp = (i[0], i[1])
    print(best_sp)

    self.a_forced = best_sp[0] * Vector3D(np.sin(self.angle + (self.angle_speed + best_sp[1]/2*(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)) * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)),
     np.cos(self.angle + (self.angle_speed + best_sp[1]/2*(cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)) * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)), 0)
    self.angle_accel = best_sp[1]




def predict_cords(self, forced_a):
    g = Vector3D(0, cfg.g, 0)
    x = Vector3D(1, 0, 0)
    y = Vector3D(0, 1, 0)

    n = len(self.segments)
    self.segments[0].forced_a = forced_a

    pred_pos = [0]*n
    pred_vel = [0]*n

    Forces = calc_newton(self)

    for i in range(n):
        s = self.segments[i]

        F = Vector3D(0, 0, 0)

        speed = s.speed
        pos = s.pos

        # adding forces to segments
        if i != 0:
            line = self.segments[i - 1].pos - s.pos
            F += line.direction() * Forces[3 * i - 1]

        if i != n - 1:
            line = s.pos - self.segments[i + 1].pos
            F -= line.direction() * Forces[3 * i + 2]

        F += x * Forces[3 * i]
        F += y * Forces[3 * i + 1]
        F -= s.m * g  # adding gravity force
        F -= s.speed * cfg.ak  # adding air resistance force

        speed += F/s.m * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)
        pred_vel[i] = speed

        pos += speed * (cfg.sk / cfg.fps / int(cfg.upfr / cfg.fps) * cfg.upup)
        pred_pos[i] = pos

    return pred_pos, pred_vel

def save_check(self, pred_pos, pred_vel, edges):
    if edges is None:
        return True

    last = self.att_rope.segments[len(self.att_rope.segments)-1]
    ln = len(self.att_rope.segments)-1

    for edge in edges:
        s_tow = edge.distance(pred_pos[ln])
        vec_tow = edge.p_vec()
        sp_tow = vec_tow.project(pred_vel[ln])

        quadr_a = vec_tow.project(Vector3D(np.sin(self.angle), np.cos(self.angle), 0) * cfg.q_a)
        quadr_v = vec_tow.project(self.speed)
        quadr_h = vec_tow.project(self.pos - pred_pos[ln])
        quadr_ttl = vec_tow.project(Vector3D(np.sin(self.angle), np.cos(self.angle), 0) * self.att_rope.ttl_length)

        if not((s_tow/sp_tow.length) > ( (quadr_v.length + (quadr_v.lengthsq() + 4 * (quadr_ttl.length-quadr_h.length)*quadr_a.length)**(1/2)) / (2 * quadr_a.length))):
            return False

    return True

def speed_proximity(self, pred_vel):
    ln = len(self.att_rope.segments)-1
    x = Vector3D(1, 0, 0)

    return (x.project(pred_vel[ln]).length-cfg.req_sp)**2 / cfg.req_sp**2

def distance_proximity(self, pred_pos, edges):
    if edges is None:
        return 0

    ln = len(self.att_rope.segments)-1

    dist = 100000
    for edge in edges:
        dist = min(dist, edge.distance(pred_pos[ln]))

    return (dist - cfg.req_dist)**2 / cfg.req_dist**2

def heading_proximity(self, pred_pos):
    x = Vector3D(1, 0, 0)
    y = Vector3D(0, 1, 0)
    ln = 0
    #ln = len(self.att_rope.segments)-1

    #return 1/(pred_pos[ln].x - cfg.tgt_x)**2
    return 1/((pred_pos[ln].x - cfg.tgt_x)**2 + (pred_pos[ln].y - cfg.tgt_y)**2)**(1/2)
    #return 1/((pred_pos[ln].x - cfg.tgt_x)**2 + (pred_pos[ln].y - cfg.tgt_y)**2)
    #return ((x.project_k(self.speed) * x.length) / (cfg.tgt_x - x.project_k(self.pos) * x.length))**2 