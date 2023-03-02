from GUI import GUI
from HAL import HAL
import math
import cv2
import numpy as np

V = 1
Vmax = 5
W = 0
K_P = 9
K_D = 11
K_I = 7
e = math.e
prev_error = 0
sum_error = 0
i = 0

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
    if M["m00"] != 0:
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        center = (center_x, center_y)
    else:
        center = (329, 399)

    radius = 5
    color = (255, 0, 0)
    thickness = -1
    image = cv2.circle(image, center, radius, color, thickness)
    GUI.showImage(image)
    return center


def get_speed(V, W, reference, prev_error, sum_error, i):
    center = (329, 399) # 329 y 399 son coordenadas del centroide en t = 0
    get_x, get_y = reference
    diff_x = center[0] - get_x
    diff_y = center[1] - get_y
    error = diff_x/480
    i += 1
    sum_error -= error
    W = K_P*error + K_D*(error - prev_error) + K_I * sum_error/i
    V = Vmax/(abs(W) + 1)
    if V >= Vmax:
        V = Vmax
    return V , W, error

HAL.setV(0)
HAL.setW(0)
while True:
    try:
        camera = HAL.getImage()
        center = filter_image(camera)
        V, W, prev_error = get_speed(V, W, center, prev_error, sum_error, i)
        HAL.setV(V)
        HAL.setW(W)
        print(round(V*20, 0), "km/h")
        print(round(W, 2), "rad/s")
    except Exception as e:
        print(e)
        HAL.setV(0)
        HAL.setW(0)

