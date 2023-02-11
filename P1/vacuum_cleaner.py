from GUI import GUI
from HAL import HAL
import rospy, random, math, time
import numpy as np
# Enter sequential code!
pi = math.pi
v = 0.15
w = 2*pi*0.85
angle = random.uniform(1.6, 2.4)
time_start = time.time()

def bumped():
    bumper = HAL.getBumperData().bumper
    crash = bool(HAL.getBumperData().state)
    if crash:
        print("crashed")
        HAL.setV(-5)
        HAL.setW(0)
        rospy.sleep(0.5)
        HAL.setV(0)
        HAL.setW(angle*pi)
        rospy.sleep(0.5)
    return crash


while True:
    HAL.setV(v)
    HAL.setW(w)
    bump = bumped()
    if not bump:
        if (w >= 0.05):
            time_current = time.time()
            if (time_current - time_start) > (2*pi/w):
                time_start = time.time()
                v += 0.35
                w -= 0.35
            print("V:", v)
            print("W:", w)
    else:
        v = 0.45
        w = 2*pi*0.55
