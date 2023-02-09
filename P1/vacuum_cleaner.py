from GUI import GUI
from HAL import HAL
import rospy, random, math
import numpy as np
# Enter sequential code!
v = 0.5
w = 0.5
pi = math.pi

def bumped():
    bumper = HAL.getBumperData().bumper
    crash = bool(HAL.getBumperData().state)
    if crash:
        print("crashed")
        HAL.setV(-1)
        HAL.setW(0)
        rospy.sleep(0.5)
    return crash


while True:
    HAL.setV(v)
    HAL.setW(w)
    bump = bumped()
    if not bump:
        v += 0.05
        w += 0.05
        print("V:", v)
        print("W:", w)
        rospy.sleep(1/3)
    else:
        v = 0.5
        w = 0.5
    print("V:", v)
    print("W:", w)
