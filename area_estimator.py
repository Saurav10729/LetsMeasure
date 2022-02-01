import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import math

parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


def image_preprocessing(opencv_image):
    image_blur = cv2.GaussianBlur(opencv_image, (7, 7), 1)
    image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    image_canny = cv2.Canny(image_gray, threshold1=23, threshold2=25)

    return image_canny


def area_polygon(opencv_image, image_canny):
    area_list = []
    kernel = np.ones((5, 5))
    dilated_image = cv2.dilate(image_canny, kernel, iterations=1)
    no_of_objects = 0
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)

        aruco_area = cv2.contourArea(corners[0])

        area_conversion_ratio = 2304 / aruco_area
        print("area conversion ratio:", area_conversion_ratio)
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # area_in_cm2 = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            area_in_mm2 = area_conversion_ratio * area
            area_in_cm2 = area_in_mm2 / 100
            area_in_cm2 = round(area_in_cm2, 2)

            if area > 20000:  # to remove noise contours
                no_of_objects += 1
                cv2.drawContours(opencv_image, cnt, -1, (0, 255, 0), 25)
                perimeter = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, .04 * perimeter, True)
                print(len(approx))
                x, y, w, h = cv2.boundingRect(approx)
                # cv2.rectangle(opencv_image,(x,y),(x+w,y+h), (0, 255, 0), 5)
                area_list.append(area_in_cm2)
                cv2.circle(opencv_image, (int(x + w // 2), int(y + h // 2)), 5, (0, 0, 255), -1)
                cv2.putText(opencv_image, "No.of Points detected:" + str(len(approx)),
                            (int(x + w // 3), int(y + h // 2)), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 3)
                cv2.putText(opencv_image, "Area {} sqr.cm".format(area_in_cm2, 1),
                            (int(x + w // 3), int(y + h // 2 + 60)), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 3)
        # (x + w + 20, y + 30)(x+w+20,y+45)
        cv2.imshow("image", opencv_image)
        if no_of_objects > 1:
            return opencv_image, no_of_objects, area_list
        else:
            return opencv_image, 0, None
    else:
        return opencv_image, -1, None


def area_circle(opencv_image, image_canny):
    image_copy = opencv_image.copy()
    circle_x_y = [[0, 0, 0, 0]]

    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(image_copy, int_corners, True, (0, 255, 0), 5)
        aruco_area = cv2.contourArea(corners[0])
        aruco_perimeter = cv2.arcLength(corners[0], True)

        pixel_cm_ratio = aruco_perimeter / 19.2
        area_conversion_ratio = 2304 / aruco_area
        print("pixel_cm_ratio: ", pixel_cm_ratio)
        print("area conversion ratio: ", area_conversion_ratio)

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
            flag = 'true'
            for i in circles[0, :]:
                radius = i[2] / pixel_cm_ratio

                if radius > 0.5:
                    area = (355 / 113) * radius * radius
                    circle_data = [i[0], i[1], round(radius, 2), area]

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
                        cv2.putText(image_copy, "Area: " + str(round(area, 2)) + ' cm', (i[0] - 70, i[1] + 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)

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


def area_irregular():
    print("area of irregular object function")
