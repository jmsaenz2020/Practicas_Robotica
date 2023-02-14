from GUI import GUI
from HAL import HAL
import rospy, random, math, time
import numpy as np
# Enter sequential code!
pi = math.pi
v = 1
w = v*pi
time_start = time.time()

def bumped(w):
    bumper = HAL.getBumperData().bumper
    crash = bool(HAL.getBumperData().state)
    if crash:
        if bumper == 0:
            print("izquierda")
            angle = random.uniform(-0.35, -0.25)
            if w < 0:
                w *= -1
        elif bumper == 2:
            print("derecha")
            angle = random.uniform(0.25, 0.35)
            if w > 0:
                w *= -1
        else:
            print("frente")
            angle = random.uniform(0.45, 0.55)
        HAL.setV(-5)
        HAL.setW(0)
        rospy.sleep(1)
        HAL.setV(0)
        HAL.setW(angle)
        rospy.sleep(1)
    return crash, w

while True:
    HAL.setV(v)
    HAL.setW(w)
    bump, w = bumped(w)
    if not bump:
        print(v, w)
        if (abs(w) >= 0.05):
            time_current = time.time()
            if (time_current - time_start) > (2*pi/abs(w)):
                time_start = time.time()
                v += 0.5
    else:
        v = 1

