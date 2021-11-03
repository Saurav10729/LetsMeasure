import cv2
import cv2
import numpy as np

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

            cv2.putText(opencv_image, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

            cv2.putText(opencv_image, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

    return opencv_image

def generate_image_circle(opencv_image):
    opencv_copy = opencv_image.copy()
    gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image,(5,5),0)
    lower =84
    upper =255
    edges = cv2.Canny(blurred_image,lower,upper)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, 1)
    rep = cv2.drawContours(opencv_image, contours, -1, (0, 255, 0), 3)

    # cnt = contours
    # for i in range(0, len(cnt)):
    #     ellipse = cv2.fitEllipse(cnt[i])
    #
    #     (center, axes, orientation) = ellipse
    #     majoraxis_length = max(axes)
    #     minoraxis_length = min(axes)
    #
    #     eccentricity = (np.sqrt(1 - (minoraxis_length / majoraxis_length) ** 2))
    #     print("Eccentricity:: ",eccentricity)
    #
    #     cv2.ellipse(opencv_copy, ellipse, (0, 0, 255), 2)
    #
    # cv2.imshow('Detected ellipse', opencv_copy)
    return(opencv_image)
    # return(opencv_image, opencv_copy)


