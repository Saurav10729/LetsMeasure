import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import math


parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

def image_preprocessing(opencv_image):
    image_contour = opencv_image.copy()
    image_blur = cv2.GaussianBlur(opencv_image, (7, 7), 1)
    image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
    image_canny = cv2.Canny(image_gray, threshold1=23, threshold2=22)
    kernel = np.ones((5, 5))
    image_dilation = cv2.dilate(image_canny, kernel, iterations=1)
    return image_dilation

def area_polygon(opencv_image,dilated_image):
    image_contour = opencv_image.copy()
    area_list = []
    # image_blur = cv2.GaussianBlur(opencv_image,(7,7),1)
    # image_gray = cv2.cvtColor(image_blur,cv2.COLOR_BGR2GRAY)
    # image_canny = cv2.Canny(image_gray,threshold1=23, threshold2=22)
    # kernel = np.ones((5,5))
    # image_dilation = cv2.dilate(image_canny,kernel,iterations=1)
    # cv2.imshow("image with dialation",image_dilation)
    corners, _, _ = cv2.aruco.detectMarkers(opencv_image, aruco_dict, parameters=parameters)
    if corners:
        int_corners = np.int0(corners)
        cv2.polylines(opencv_image, int_corners, True, (0, 255, 0), 5)

        aruco_area = cv2.contourArea(corners[0])
        aruco_perimeter = cv2.arcLength(corners[0], True)

        pixel_cm_ratio = aruco_perimeter / 20
        area_conversion_ratio = 2500/aruco_area

        contours, _ = cv2.findContours(dilated_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        area_in_cm2 = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            area_in_mm2 = area_conversion_ratio * area
            area_in_cm2 = area_in_mm2/100
            area_in_cm2 = round(area_in_cm2,1)

            if area > 1000: #to remove noise contours
                cv2.drawContours(image_contour, cnt, -1, (255, 0, 255), 10)
                perimeter = cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt, .02*perimeter, True)
                print(len(approx))
                x , y , w , h = cv2.boundingRect(approx)
                cv2.rectangle(image_contour,(x,y),(x+w,y+h),(0,255,0),5)
                area_list.append(area_in_cm2)
                cv2.putText(opencv_image, "No.of Points detected:"+str(len(approx)),(x+w+20,y+30),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
                cv2.putText(opencv_image, "Area {} sqr.cm".format(area_in_cm2, 1),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)

        return opencv_image,area_list

def area_circle():
    print("area of circle function")

def area_irregular():
    print("area of irregular object function")




