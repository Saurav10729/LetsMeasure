import cv2
import numpy as np


class HomogeneousBgDetector:
    def __init__(self):
        pass

    def detect_objects(self, frame):
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
        image_blur = cv2.GaussianBlur(frame, (7, 7), 1)
        image_gray = cv2.cvtColor(image_blur, cv2.COLOR_BGR2GRAY)
        image_canny = cv2.Canny(image_gray, threshold1=23, threshold2=25)
        kernel = np.ones((5, 5))
        dilated_image = cv2.dilate(image_canny, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10000:
                objects_contours.append(cnt)

        return objects_contours
