import cv2
import numpy as np


class HomogeneousBgDetector:
    def __init__(self):
        pass

    def detect_objects(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 19, 5)
        # mask = cv2.Canny(gray,25,25)
        kernel = np.ones((5, 5))
        image_dilation = cv2.dilate(mask, kernel, iterations=1)
        contours, _ = cv2.findContours(image_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        objects_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10000:
                objects_contours.append(cnt)

        return objects_contours
