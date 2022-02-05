import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import math

from object_detector import HomogeneousBgDetector

parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
detector = HomogeneousBgDetector()


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


def give_edge_numbering(approx, opencv_image, length_in_cm):
    points = np.array(approx).reshape(-1, 1, 2)
    numbering = 0
    for pt in zip(points, np.roll(points, -1, 0)):
        x = pt[0][0]  # say point 1  so x[0] = x1 coord of point 1 x[1] = y1 coord of point1
        y = pt[1][0]

        midX, midY = int((x[0] + y[0]) / 2), int((x[1] + y[1]) / 2)
        print(x[0], ",", x[1])
        print(y[0], ",", y[1])
        print("mid point: ", midX, ", ", midY)
        cv2.putText(opencv_image, str(length_in_cm[numbering]) + "cm", (midX, midY), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (255, 255, 0), 5, 2)
        cv2.circle(opencv_image, (x[0], x[1]), 15, (0, 0, 255), -1)
        cv2.circle(opencv_image, (y[0], y[1]), 15, (0, 0, 255), -1)
        numbering += 1

    return opencv_image


def generate_image_rectangle(opencv_image):
    no_of_objects = 0
    dimension_list = list()
    length_in_cm = list()
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)

    if corners:
        # int_corners = np.int0(corners)
        # # cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 18.8
        aruco_area = cv2.contourArea(corners[0])
        print("area of aruco:", aruco_area)
        area_conversion_ratio = aruco_area / 2209

        contours = detector.detect_objects(opencv_image)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            print("area of contour", area)
            if area > 20000:
                no_of_objects += 1
                # trying to determine shape of polygon and extract and measure edge

                shape_of_object = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
                print(shape_of_object)
                length = extract_edge_values(shape_of_object)
                for i in length:
                    length_in_cm.append(round(i / pixel_cm_ratio, 2))

                length_in_cm.pop(0)
                print(length_in_cm)

                if len(shape_of_object) == 3:
                    shape = "triangle"
                elif len(shape_of_object) == 4:
                    diff = abs(cv2.contourArea(cnt) - aruco_area)
                    print("difference in area:", diff / area_conversion_ratio)
                    r = cv2.minAreaRect(cnt)
                    _, (w, h), angle = r
                    ar = w / h
                    # if aspect ratio is close to 1 and area is close to area of aruco then, its aruco
                    if 0.95 < ar < 1.05 and 0 < diff / area_conversion_ratio < 60:
                        shape = ""  # aruco
                        dimension_list.append([no_of_objects, shape, length_in_cm])
                    # if aspect ratio close to 1, its square
                    elif 0.95 < ar < 1.05:
                        shape = "square"
                        dimension_list.append([no_of_objects, shape, length_in_cm])
                    # if opposite sides are equal then its rectangle
                    elif 0.95 < length_in_cm[0] / length_in_cm[2] < 1.05 and \
                            0.95 < length_in_cm[1] / length_in_cm[3] < 1.05:
                        shape = "Rectangle"
                        dimension_list.append([no_of_objects, shape, length_in_cm])
                    # if none of the condition satisfy its irregular quadrilateral
                    else:
                        shape = "Quadrilateral"
                        dimension_list.append([no_of_objects, shape, length_in_cm])
                # if no. of sides equals 5 its, pentagon
                elif len(shape_of_object) == 5:
                    shape = "pentagon"
                    dimension_list.append([no_of_objects, shape, length_in_cm])
                elif 5 < len(shape_of_object) < 8:
                    shape = str(len(shape_of_object)) + " point polygon"
                    dimension_list.append([no_of_objects, shape, length_in_cm])
                else:
                    shape = "not polygon"
                # print(dimension_list)
                print(shape)
                print("----------------")

                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(opencv_image, (cX, cY), 7, (0, 0, 255), -1)
                cv2.putText(opencv_image, shape, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5, 2)
                cv2.drawContours(opencv_image, cnt, -1, (0, 255, 0), 10)
                opencv_image = give_edge_numbering(approx=shape_of_object, opencv_image=opencv_image,
                                                   length_in_cm=length_in_cm)
                length_in_cm.clear()
        if no_of_objects > 1:
            return opencv_image, no_of_objects, dimension_list
        else:
            return opencv_image, 0, None
    else:
        return opencv_image, -1, None


def generate_image_circle(opencv_image):
    image_copy = opencv_image.copy()
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    length_in_cm = list()
    circle_x_y = list()
    no_of_objects = 0

    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(image_copy, int_corners, True, (0, 255, 0), 5)
        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / 18.8
        print(int_corners[0])
        length = extract_edge_values(int_corners[0])
        for i in length:
            length_in_cm.append(round(i / pixel_cm_ratio, 1))
        length_in_cm.pop(0)
        print(length_in_cm)
        give_edge_numbering(int_corners[0], image_copy, length_in_cm)

        blur_image = cv2.GaussianBlur(opencv_image, (7, 7), 1)
        gray_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
        image_canny = cv2.Canny(gray_image, 23, 25)

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
                        no_of_objects += 1
                        circle_x_y.append(circle_data)
                        cv2.circle(image_copy, (i[0], i[1]), i[2], (0, 255, 0), 25)
                        cv2.circle(image_copy, (i[0], i[1]), 15, (0, 0, 255), -1)
                        cv2.putText(image_copy, "Radius: " + str(round(radius, 2)) + ' cm', (i[0] - 70, i[1]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)
                        cv2.putText(image_copy, "Diameter: " + str(round(diameter, 2)) + ' cm', (i[0] - 70, i[1] + 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 5)

                    count = count + 1
                    print(circle_x_y)

        if len(circle_x_y) > 0:
            for i in circle_x_y:
                print(i)  # printing circles after popping [0,0,0,0] item from circle_x_y
            return image_copy, no_of_objects, circle_x_y
        else:
            return image_copy, 0, None

    else:
        return image_copy, -1, None
