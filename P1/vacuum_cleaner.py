from GUI import GUI
from HAL import HAL
import rospy, random, math, time
import numpy as np

pi = math.pi
v = 1
w = v*pi
time_start = time.time()

def bumped(w):
    bumper = HAL.getBumperData().bumper # donde detecta el choque
    crash = bool(HAL.getBumperData().state) # detecta choque
    if crash:
        if bumper == 0:
            print("izquierda")
            angle = random.uniform(-0.35, -0.25)
            if w < 0: # si se choca en sentido opuesto, cambia dirección
                w *= -1
        elif bumper == 2:
            print("derecha")
            angle = random.uniform(0.25, 0.35)
            if w > 0: # si se choca en sentido opuesto, cambia dirección
                w *= -1
        else:
            print("frente")
            angle = random.uniform(0.45, 0.55)
        # Retrocede, gira con el ángulo aleatorio y sigue al estado normal
        HAL.setV(-5)
        HAL.setW(0)
        rospy.sleep(1)
        HAL.setV(0)
        HAL.setW(angle)
        rospy.sleep(1)
    return crash, w

while True:
    # Gira en elipse
    HAL.setV(v)
    HAL.setW(w)
    bump, w = bumped(w)
    if not bump:
        # Si no se choca
        print(v, w)
        if (abs(w) >= 0.05):
            # tiempo de periodo
            time_current = time.time()
            # si supera al periodo, aumenta la velocidad
            if (time_current - time_start) > (2*pi/abs(w)):
                time_start = time.time()
                v += 0.5
    else:
      # si se choca, vuelve a la velocidad normal
        v = 1

