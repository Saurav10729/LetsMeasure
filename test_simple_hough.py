import cv2
import numpy as np

# Read image.
img = cv2.imread('Testimages/aruco with cup7.jpg', cv2.IMREAD_COLOR)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 600, 600)

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))
# Apply Hough transform on the blurred image.
# height, width = img.shape[:2]
# minRadius=int(height*0.06)
# maxRadius=int(width*0.09)
#
# detected_circles = cv2.HoughCircles(gray_blurred,
#                                     cv2.HOUGH_GRADIENT, 1, 20, param1=50,
#                                     param2=30, minRadius=minRadius, maxRadius=maxRadius)

height, width = img.shape[:2]
minRadius=int(height*0.1)
maxRadius=int(width*0.5)
detected_circles = cv2.HoughCircles(gray_blurred,
                           method=cv2.HOUGH_GRADIENT,
                           dp=1,
                           minDist=50,
                           param1=70,
                           param2=40,
                           minRadius=100,
                           maxRadius=2000)


# Draw circles that are detected.
if detected_circles is not None:
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
    print(len(detected_circles))
    print(detected_circles)

    # first_circle =detected_circles[0]
    # a,b,r = first_circle[0],first_circle[1],first_circle[2]
    # cv2.circle(img, (a, b), r, (0, 255, 0), 2)
    # cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
    # cv2.imshow("image", img)
    # cv2.waitKey(0)
    count = 0
    for pt in detected_circles[0, :]:
        count+=1
        a, b, r = pt[0], pt[1], pt[2]
        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.imshow("image", img)
        cv2.waitKey(0)
    print(count)
else:
    print('no circles found')