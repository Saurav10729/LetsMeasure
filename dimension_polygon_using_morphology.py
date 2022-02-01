import math
import cv2
import numpy as np

# load image
img = cv2.imread('Testimages/phone_with_aruco.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply canny edge detection
edges = cv2.Canny(gray, 90, 130)

kernel = np.ones((5, 5))
dilated_image = cv2.dilate(edges, kernel, iterations=1)

# apply morphology close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morph = cv2.morphologyEx(dilated_image, cv2.MORPH_CLOSE, kernel)


# get contours and keep largest
contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

big_contour = max(contours, key=cv2.contourArea)
area_big_contour = cv2.contourArea(big_contour) *0.040
if area_big_contour in range(22,25):
    contours
# draw contour
contour = img.copy()
cv2.drawContours(contour, [big_contour], 0, (0, 255, 255), 5)

# get number of vertices (sides)
peri = cv2.arcLength(big_contour, True)
approx = cv2.approxPolyDP(big_contour, 0.03 * peri, True)
print('number of sides:', len(approx))

# save results
cv2.imwrite("quadrilateral_edges.jpg", edges)
cv2.imwrite("quadrilateral_dilated.jpg", dilated_image)
cv2.imwrite("quadrilateral_morphology.jpg", morph)
cv2.imwrite("quadrilateral_contour.jpg", contour)

# show result
cv2.imshow("edges", edges)
cv2.imshow("morph", morph)
cv2.imshow("contour", contour)
cv2.waitKey(0)
cv2.destroyAllWindows()

points = np.array(approx).reshape(-1, 1, 2)
for pt in zip(points, np.roll(points, -1, 0)):
    x = pt[0][0]
    y = pt[1][0]
    d = math.sqrt((x[1] - y[1]) * (x[1] - y[1]) + (x[0] - y[0]) * (x[0] - y[0]))
    print('length between point:', x, 'and', y, 'is', d)
