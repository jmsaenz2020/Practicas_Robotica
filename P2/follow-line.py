from GUI import GUI
from HAL import HAL
import math, cv2
import numpy as np

v = 1
w = 0
k_p = 0.001
k_i = 0.1
k_d = 0.1

def filter_image(image):
    img_hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    mask = cv2.add(mask0, mask1)
    output = cv2.bitwise_and(image, image, mask = mask)
    # Buscar contornos
    contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contour, key=cv2.contourArea)
    M = cv2.moments(max_contour) # Obtener centroide de imagen
    center_x = int(M["m10"] / M["m00"])
    center_y = int(M["m01"] / M["m00"])
    center = (center_x, center_y)
    radius = 5
    color = (255, 0, 0)
    thickness = -1
    image = cv2.circle(image, center, radius, color, thickness)
    GUI.showImage(image)
    return center
    
    
def get_speed(v, w, reference):
    center = (329, 399)
    get_x, get_y = reference
    diff_x = center[0] - get_x # 329 y 399 son coordenadas del centroide en t = 0
    diff_y = center[1] - get_y
    print(diff_x, diff_y)
    w = k_p*diff_x
    if (abs(diff_x) > 130) and (abs(diff_x) < 150):
        v -= k_p*abs(diff_x)
        if v < 2:
            v = 2
    elif (abs(diff_x) > 150):
        v -= k_p*abs(diff_x)
        if v < 1:
            v = 1
    elif abs(diff_x) < 4:
        v += 0.07
        if v > 6:
            v = 6
    elif (abs(diff_x) > 60) and (abs(diff_x) < 130):
        v = 1
    else:
        v += 0.01
        if v > 5:
            v = 5
    return v, w

HAL.setV(0)
HAL.setW(0)
while True:
    try:
        camera = HAL.getImage()
        center = filter_image(camera)
        v, w = get_speed(v, w, center)
        HAL.setV(v)
        HAL.setW(w)
    except Exception as e:
        print("CRASHED")

