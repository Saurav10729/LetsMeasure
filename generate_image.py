import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import math

from object_detector import HomogeneousBgDetector

parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
detector = HomogeneousBgDetector()


def generate_image_rectangle(opencv_image):
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)

    if corners:

        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)

        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 19.2

        contours = detector.detect_objects(opencv_image)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 20000:
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect

                object_width = w / pixel_cm_ratio
                object_height = h / pixel_cm_ratio

                cv2.circle(opencv_image, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.drawContours(opencv_image, cnt, -1, (0, 255, 0), 25)

                cv2.putText(opencv_image, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 30)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)

                cv2.putText(opencv_image, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 30)),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)

    return opencv_image


def generate_image_circle(opencv_image):
    image_copy = opencv_image.copy()
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(image_copy, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 19.2

        blur_image = cv2.GaussianBlur(opencv_image, (7, 7), 1)
        gray_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
        image_canny = cv2.Canny(gray_image, 23, 25)
        circle_x_y = [[0, 0, 0]]

        radii = np.arange(0, 1000, 10)

        for idx in range(len(radii) - 1):

            minRadius = radii[idx] + 1
            maxRadius = radii[idx + 1]
            print(minRadius, " , ", maxRadius)
            circles = cv2.HoughCircles(image_canny, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30,
                                       minRadius=minRadius,
                                       maxRadius=maxRadius)
            if circles is None:
                continue
            circles = np.uint16(np.around(circles))
            count = 1
            flag = 'true'
            for i in circles[0, :]:
                radius = i[2] / pixel_cm_ratio
                diameter = radius * 2
                if radius > 0.5:
                    circle_data = [i[0], i[1], round(radius, 2)]

                    for j in circle_x_y:
                        x_range = range(j[0] - 50, j[0] + 50, 1)
                        y_range = range(j[1] - 50, j[1] + 50, 1)
                        if (circle_data[0] in x_range) and (circle_data[1] in y_range):
                            flag = "false"
                        else:
                            flag = 'true'

                    if flag == 'true':
                        circle_x_y.append(circle_data)
                        cv2.circle(image_copy, (i[0], i[1]), i[2], (0, 255, 0), 25)
                        cv2.circle(image_copy, (i[0], i[1]), 2, (0, 0, 255), 3)
                        cv2.putText(image_copy, "Radius: " + str(round(radius, 2)) + ' cm', (i[0] - 70, i[1]),
                                    cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 3)
                        cv2.putText(image_copy, "Diameter: " + str(round(diameter, 2)) + ' cm', (i[0] - 70, i[1] + 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)

                    count = count + 1
                    print(circle_x_y)

        if len(circle_x_y) > 1:
            no_of_circle = len(circle_x_y) - 1
            circle_x_y.pop(0)
            for i in circle_x_y:
                print(i)  # printing circles after popping [0,0,0,0] item from circle_x_y
            return image_copy, no_of_circle, circle_x_y
        else:
            return image_copy, 0, None

    else:
        return image_copy, -1, None
