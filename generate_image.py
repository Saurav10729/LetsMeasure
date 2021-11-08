
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

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
        pixel_cm_ratio = aruco_perimeter / 20

        contours = detector.detect_objects(opencv_image)

        for cnt in contours:

            rect = cv2.minAreaRect(cnt)
            (x, y), (w, h), angle = rect

            object_width = w / pixel_cm_ratio
            object_height = h / pixel_cm_ratio

            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.circle(opencv_image, (int(x), int(y)), 5, (0, 0, 255), -1)

            cv2.polylines(opencv_image, [box], True, (255, 0, 0), 2)

            cv2.putText(opencv_image, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

            cv2.putText(opencv_image, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    return opencv_image

def generate_image_circle(opencv_image):
    image_copy = opencv_image.copy()
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)

        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 20

        grayimage = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        blurimage = cv2.GaussianBlur(grayimage, (21, 21), cv2.BORDER_DEFAULT)

        all_circles = cv2.HoughCircles(blurimage, cv2.HOUGH_GRADIENT, 0.9, 120)

        if all_circles is not None:
            all_circles_rounded = np.uint16(np.around(all_circles))

            print(all_circles_rounded)
            print(all_circles_rounded.shape)
            print('Circles found:' + str(all_circles_rounded.shape[1]))

            count = 1
            for i in all_circles_rounded[0, :]:
                radius = i[2]/pixel_cm_ratio
                circumference = 2*(22/7)*radius
                area = (22/7)*radius*radius
                cv2.circle(image_copy, (i[0], i[1]), i[2], (50, 200, 200), 5)
                cv2.circle(image_copy, (i[0], i[1]), 2, (255, 0, 0), 5)

                #display on the image
                # Circle
                # Radius: __ cm
                # Circumference: ___ cm
                # Area: __ sqr.cm

                cv2.putText(image_copy, "Circle" + str(count), (i[0] - 70, i[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
                cv2.putText(image_copy, "Radius: " + str(round(radius,2))+' cm', (i[0] - 70, i[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
                cv2.putText(image_copy, "Circumference: " + str(round(circumference,2))+' cm', (i[0] - 70, i[1] + 70), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
                cv2.putText(image_copy, "Area: " + str(round(area,2))+' sqr.cm', (i[0] - 70, i[1] + 90), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)

                count += 1
            return (image_copy, len(all_circles_rounded))

        else:
            return(image_copy,0)
    return(image_copy,-1)

