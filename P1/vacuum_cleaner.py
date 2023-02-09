from GUI import GUI
from HAL import HAL
import rospy, random, math
import numpy as np
# Enter sequential code!
v = 3

def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i)
        laser += [(dist, angle)]
    return laser

def laser_vector(laser):
    laser_vectorized = []
    for d,a in laser:
        # (4.2.1) laser into GUI reference system
        x = d * math.cos(a) * -1
        y = d * math.sin(a) * -1
        v = (x,y)
        laser_vectorized += [v]

    laser_mean = np.mean(laser_vectorized, axis=0)
    return laser_mean

def data():
    side = None
    crash = HAL.getBumperData().state
    wherecrash = HAL.getBumperData().bumper
    pos0 = HAL.getPose3d().yaw
    laser = parse_laser_data(HAL.getLaserData())
    dist = laser_vector(laser)
    print("Velocidad:", v)
    print("Orientación:", round(pos0, 3))
    print("Choque:", bool(crash))
    print("Distancia:", dist)
    if bool(crash):
        if wherecrash == 0:
            side = "derecho"
        elif wherecrash == 2:
            side = "izquierdo"
        else:
            side = "centro"
    print("Lado", side)
    
    return crash, wherecrash, pos0

def manage_crash(crash, wherecrash, v, pos0):
    if bool(crash):
        while bool(crash):
            pi = math.pi
            if wherecrash == 0:
                v = 0.5
                HAL.setW(pi/2)
                if pos0 == math.pi:
                    crash = False
            elif wherecrash == 2:
                v = -0.5
                HAL.setW(-pi/2)
            else:
                v = -1
                HAL.setW(pi)
    HAL.setV(v)
    HAL.setW(0)
    rospy.sleep(0.5)
    return v


while True:
    crash, wherecrash, pos0 = data()
    v = manage_crash(crash, wherecrash, v, pos0)
    print("Velocidad:", v)
