
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
        circle_x_y = [[0,0,0]]
        radii = np.arange(0, 310, 10)
        for idx in range(len(radii)-1):
            # print(" 1st loop")
            minRadius = radii[idx] + 1
            maxRadius = radii[idx + 1]
            circles = cv2.HoughCircles(blurimage, cv2.HOUGH_GRADIENT, 1, 5, param1=25, param2=75, minRadius=minRadius, maxRadius=maxRadius)
            if circles is None:
                continue
            circles = np.uint16(np.around(circles))
            # print(circles)
            count =1
            flag = 'true'
            for i in circles[0, :]:
                # print("innerloop")
                radius = i[2] / pixel_cm_ratio
                diameter = radius * 2

                circle_data =[i[0],i[1],round(radius,2)]
                offset1 = 20
                offset2 = offset1 + 30

                for j in circle_x_y:
                    x_range = range(j[0] - 20, j[0] + 20,1)
                    y_range = range(j[1] - 20, j[1] + 20,1)
                    if (circle_data[0] in x_range) and (circle_data[1] in y_range):
                        flag = "false"
                    else:
                        flag = 'true'

                if flag == 'true':
                    circle_x_y.append(circle_data)
                    cv2.circle(image_copy, (i[0], i[1]), i[2], (0, 255, 0), 1)
                    cv2.circle(image_copy, (i[0], i[1]), 2, (0, 0, 255), 3)
                    cv2.putText(image_copy, "Radius: " + str(round(radius, 2)) + ' cm', (i[0] - 70, i[1] + offset1),
                                cv2.FONT_HERSHEY_SIMPLEX, .8, (241, 231, 64), 2)
                    cv2.putText(image_copy, "Diameter: " + str(round(diameter, 2)) + ' cm', (i[0] - 70, i[1] + offset2),
                                cv2.FONT_HERSHEY_SIMPLEX, .8, (241, 231, 64), 2)

                count = count +1
                print(circle_x_y)

        no_of_circle = len(circle_x_y) -1
        circle_x_y.pop(0)
        for i in circle_x_y:
            print(i)
        return (image_copy,no_of_circle,circle_x_y)

    return (image_copy, -1,None)

    #     all_circles = cv2.HoughCircles(blurimage, cv2.HOUGH_GRADIENT, 0.9, 120)
    #     print(type(all_circles))
    #     if all_circles is not None:
    #         all_circles_rounded = np.uint16(np.around(all_circles))
    #         print(type(all_circles_rounded))
    #         print(all_circles_rounded)
    #         print(all_circles_rounded.shape)
    #         print('Circles found:' + str(all_circles_rounded.shape[1]))
    #
    #         count = 1
    #         for i in all_circles_rounded[0, :]:
    #             radius = i[2]/pixel_cm_ratio
    #             circumference = 2*(22/7)*radius
    #             area = (22/7)*radius*radius
    #             cv2.circle(image_copy, (i[0], i[1]), i[2], (50, 200, 200), 5)
    #             cv2.circle(image_copy, (i[0], i[1]), 2, (255, 0, 0), 5)
    #
    #             #display on the image
    #             # Circle
    #             # Radius: __ cm
    #             # Circumference: ___ cm
    #             # Area: __ sqr.cm
    #
    #             cv2.putText(image_copy, "Circle" + str(count), (i[0] - 70, i[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
    #             cv2.putText(image_copy, "Radius: " + str(round(radius,2))+' cm', (i[0] - 70, i[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
    #             cv2.putText(image_copy, "Circumference: " + str(round(circumference,2))+' cm', (i[0] - 70, i[1] + 70), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
    #             cv2.putText(image_copy, "Area: " + str(round(area,2))+' sqr.cm', (i[0] - 70, i[1] + 90), cv2.FONT_HERSHEY_SIMPLEX, .5,(241,231,64), 2)
    #
    #             count += 1
    #         return (image_copy, len(all_circles_rounded))
    #
    #     else:
    #         return(image_copy,0)
    # return(image_copy,-1)

