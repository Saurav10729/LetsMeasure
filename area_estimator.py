import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import math

parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


def extract_edge_values(approx):
    points = np.array(approx).reshape(-1, 1, 2)
    length_of_sides = [0]
    for pt in zip(points, np.roll(points, -1, 0)):
        x = pt[0][0]
        y = pt[1][0]
        d = math.sqrt((x[1] - y[1]) * (x[1] - y[1]) + (x[0] - y[0]) * (x[0] - y[0]))
        length_of_sides.append(d)
        # print('length between point:', x, 'and', y, 'is', d)
    return length_of_sides


def perimeter_approx_poly(approx):
    points = np.array(approx).reshape(-1, 1, 2)
    perimeter = 0
    for pt in zip(points, np.roll(points, -1, 0)):
        x = pt[0][0]
        y = pt[1][0]
        d = math.sqrt((x[1] - y[1]) * (x[1] - y[1]) + (x[0] - y[0]) * (x[0] - y[0]))
        perimeter += d
    return perimeter


def image_preprocessing(opencv_image):
    image_blur = cv2.GaussianBlur(opencv_image, (7, 7), 1)
    image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    image_canny = cv2.Canny(image_gray, threshold1=23, threshold2=25)

    return image_canny


def area_polygon(opencv_image, image_canny):
    area_list = list()
    length_in_cm = list()
    perimeter_list = list()
    kernel = np.ones((5, 5))
    dilated_image = cv2.dilate(image_canny, kernel, iterations=1)
    no_of_objects = 0
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)
        aruco_area = cv2.contourArea(corners[0])
        pixel_cm_ratio = cv2.arcLength(corners[0], True) / 18.8
        area_conversion_ratio = aruco_area / 2209
        print("area conversion ratio:", area_conversion_ratio)
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # area_in_cm2 = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            area_in_mm2 = area / area_conversion_ratio
            area_in_cm2 = area_in_mm2 / 100
            area_in_cm2 = round(area_in_cm2, 2)

            if area > 20000:  # to remove noise contours

                no_of_objects += 1
                approx = cv2.approxPolyDP(cnt, .04 * cv2.arcLength(cnt, True), True)
                length = extract_edge_values(approx)
                for i in length:
                    length_in_cm.append(round(i / pixel_cm_ratio, 2))

                length_in_cm.pop(0)
                print(length_in_cm)
                if len(approx) == 3:
                    shape = "triangle"
                elif len(approx) == 4:
                    diff = abs(cv2.contourArea(cnt) - aruco_area)
                    print("difference in area:", diff / area_conversion_ratio)
                    r = cv2.minAreaRect(cnt)
                    _, (w, h), angle = r
                    ar = w / h
                    # if aspect ratio is close to 1 and area is close to area of aruco then, its aruco
                    if 0.95 < ar < 1.05 and 0 < diff / area_conversion_ratio < 60:
                        shape = ""  # aruco
                    # if aspect ratio close to 1, its square
                    elif 0.95 < ar < 1.05:
                        shape = "square"
                    elif 0.95 < length_in_cm[0] / length_in_cm[2] < 1.05 and \
                            0.95 < length_in_cm[1] / length_in_cm[3] < 1.05:
                        shape = "Rectangle"
                    # if none of the condition satisfy its irregular quadrilateral
                    else:
                        shape = "Quadrilateral"
                    # if no. of sides equals 5 its, pentagon
                elif len(approx) == 5:
                    shape = "pentagon"
                elif 5 < len(approx) < 8:
                    shape = str(len(approx)) + " point polygon"
                else:
                    shape = "not polygon"

                cv2.drawContours(opencv_image, cnt, -1, (0, 255, 0), 25)

                perimeter_val = perimeter_approx_poly(approx)
                perimeter_in_cm = round(perimeter_val / pixel_cm_ratio, 2)
                x, y, w, h = cv2.boundingRect(approx)
                area_list.append(area_in_cm2)
                perimeter_list.append(perimeter_in_cm)

                cv2.circle(opencv_image, (int(x + w // 2), int(y + h // 2)), 5, (0, 0, 255), -1)
                cv2.putText(opencv_image, shape, (int(x + w // 3), int(y + h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 255), 5, 2)
                cv2.putText(opencv_image, "No.of Points detected:" + str(len(approx)),
                            ((x + w // 3), (y + h // 2 + 60)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                cv2.putText(opencv_image, "Area: {} sqr.cm".format(area_in_cm2, 1),
                            ((x + w // 3), (y + h // 2 + 120)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                cv2.putText(opencv_image, "Perimeter: {}cm".format(perimeter_in_cm, 1),
                            (x + w // 3, y + h // 2 + 180), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
        # (x + w + 20, y + 30)(x+w+20,y+45)
        cv2.imshow("image", opencv_image)
        if no_of_objects > 1:
            return opencv_image, no_of_objects, area_list, perimeter_list
        else:
            return opencv_image, 0, None, None
    else:
        return opencv_image, -1, None, None


def area_circle(opencv_image, image_canny):
    image_copy = opencv_image.copy()
    circle_x_y = list()
    no_of_circle = 0
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(image_copy, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)

        pixel_cm_ratio = aruco_perimeter / 18.8
        print("pixel_cm_ratio: ", pixel_cm_ratio)

        radii = np.arange(400, 1000, 10)

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
                    circumference = 2 * (355 / 113) * radius
                    circle_data = [i[0], i[1], round(radius, 2), area, circumference]

                    for j in circle_x_y:
                        x_range = range(j[0] - 50, j[0] + 50, 1)
                        y_range = range(j[1] - 50, j[1] + 50, 1)
                        if (circle_data[0] in x_range) and (circle_data[1] in y_range):
                            flag = "false"
                        else:
                            flag = 'true'

                    if flag == 'true':
                        no_of_circle += 1
                        circle_x_y.append(circle_data)
                        cv2.circle(image_copy, (i[0], i[1]), i[2], (0, 255, 0), 25)
                        cv2.circle(image_copy, (i[0], i[1]), 2, (0, 0, 255), 3)
                        cv2.putText(image_copy, "Radius: " + str(round(radius, 2)) + ' cm', (i[0] - 70, i[1]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                        cv2.putText(image_copy, "Area: " + str(round(area, 2)) + 'sqr.cm', (i[0] - 70, i[1] + 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                        cv2.putText(image_copy, "Circumference: " + str(round(circumference, 2)) + 'cm',
                                    (i[0] - 70, i[1] + 120),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)

                    print(circle_x_y)

        if len(circle_x_y) > 0:
            for i in circle_x_y:
                print(i)  # printing circles after popping [0,0,0,0] item from circle_x_y
            return image_copy, no_of_circle, circle_x_y
        else:
            return image_copy, 0, None

    else:
        return image_copy, -1, None


def area_irregular(opencv_image, image_canny):
    area_list = list()
    perimeter_list = list()
    kernel = np.ones((5, 5))
    dilated_image = cv2.dilate(image_canny, kernel, iterations=1)
    no_of_objects = 0
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)
        aruco_area = cv2.contourArea(corners[0])
        pixel_cm_ratio = cv2.arcLength(corners[0], True) / 18.8
        area_conversion_ratio = aruco_area / 2209
        print("area conversion ratio:", area_conversion_ratio)
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # area_in_cm2 = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            area_in_mm2 = area / area_conversion_ratio
            area_in_cm2 = area_in_mm2 / 100
            area_in_cm2 = round(area_in_cm2, 2)

            if area > 20000:  # to remove noise contours
                no_of_objects += 1
                cv2.drawContours(opencv_image, cnt, -1, (0, 255, 0), 25)
                approx = cv2.approxPolyDP(cnt, .04 * cv2.arcLength(cnt, True), True)
                perimeter_val = perimeter_approx_poly(approx)
                perimeter_in_cm = round(perimeter_val / pixel_cm_ratio, 2)
                x, y, w, h = cv2.boundingRect(approx)
                area_list.append(area_in_cm2)
                perimeter_list.append(perimeter_in_cm)
                cv2.circle(opencv_image, (int(x + w // 2), int(y + h // 2)), 5, (0, 0, 255), -1)
                cv2.putText(opencv_image, "No.of Points detected:" + str(len(approx)),
                            ((x + w // 3), (y + h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                cv2.putText(opencv_image, "Area: {} sqr.cm".format(area_in_cm2, 1),
                            ((x + w // 3), (y + h // 2 + 60)), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                cv2.putText(opencv_image, "Perimeter: {}cm".format(perimeter_in_cm, 1),
                            (x + w // 3, y + h // 2 + 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
        # (x + w + 20, y + 30)(x+w+20,y+45)
        cv2.imshow("image", opencv_image)
        if no_of_objects > 1:
            return opencv_image, no_of_objects, area_list, perimeter_list
        else:
            return opencv_image, 0, None, None
    else:
        return opencv_image, -1, None, None
