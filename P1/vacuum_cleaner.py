from GUI import GUI
from HAL import HAL
import rospy, random, math, time
import numpy as np
# Enter sequential code!
pi = math.pi
v = 1
w = v*pi
time_start = time.time()
start = time_start

def bumped(w):
    bumper = HAL.getBumperData().bumper
    crash = bool(HAL.getBumperData().state)
    if crash:
        if bumper == 0:
            print("izquierda")
            angle = random.uniform(4.08, 4.71)/pi
            if w < 0:
                w *= -1
        elif bumper == 2:
            print("derecha")
            angle = random.uniform(1.57, 2.2)/pi
            if w > 0:
                w *= -1
        else:
            print("frente")
            angle = random.uniform(2.83, 3.46)/pi
        HAL.setV(-2)
        HAL.setW(0)
        rospy.sleep(1)
        HAL.setV(0)
        HAL.setW(angle)
        rospy.sleep(1)
    return crash, w

while True:
    end = time.time()
    if (end - start) > 300:
        print("FINISH")
        HAL.setV(0)
        HAL.setW(0)
    else:
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
