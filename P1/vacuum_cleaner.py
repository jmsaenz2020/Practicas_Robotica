from GUI import GUI
from HAL import HAL
import rospy, random, math, time
import numpy as np
# Enter sequential code!
pi = math.pi
v = 1
w = 2*pi*1
time_start = time.time()
start = time_start

def bumped(w):
    bumper = HAL.getBumperData().bumper
    crash = bool(HAL.getBumperData().state)
    if crash:
        if bumper == 0:
            print("crashed")
            angle = random.uniform(0, 1.6)
            HAL.setV(-5)
            HAL.setW(0)
            rospy.sleep(0.5)
            HAL.setV(0)
            HAL.setW(angle*pi)
            rospy.sleep(0.5)
        elif bumper == 2:
            w *= -1
            angle = random.uniform(-1.6, 0)
            HAL.setV(-5)
            HAL.setW(0)
            rospy.sleep(0.5)
            HAL.setV(0)
            HAL.setW(angle*pi)
            rospy.sleep(0.5)
        else:
            angle = random.uniform(1.6, 2.4)
            HAL.setV(-5)
            HAL.setW(0)
            rospy.sleep(0.5)
            HAL.setV(0)
            HAL.setW(angle*pi)
            rospy.sleep(0.5)
    return crash, w

while True:
    end = time.time()
    if (end - start) > 300:
        HAL.setV(0)
        HAL.setW(0)
    else:
        HAL.setV(v)
        HAL.setW(w)
        bump, w = bumped(w)
        if not bump:
            if (w >= 0.05):
                time_current = time.time()
                if (time_current - time_start) > (2*pi/w):
                    time_start = time.time()
                    v += 1.4
                    w -= 0.6
                print("V:", v)
                print("W:", w)
        else:
            v = 1
            w = 2*pi*1
