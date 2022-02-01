#importing the module cv2
import cv2
#reading the image whose shape is to be detected using imread() function
imageread = cv2.imread('Testimages/phone_with_aruco.jpg')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 600, 800)

#converting the input image to grayscale image using cvtColor() function
imagegray = cv2.cvtColor(imageread, cv2.COLOR_BGR2GRAY)
#using threshold() function to convert the grayscale image to binary image
canny = cv2.Canny(imagegray,23,25)
#finding the contours in the given image using findContours() function
imagecontours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#for each of the contours detected, the shape of the contours is approximated using approxPolyDP() function and the contours are drawn in the image using drawContours() function
contours = imagecontours[0] if len(imagecontours) == 2 else imagecontours[1]
big_contour = max(contours, key=cv2.contourArea)

epsilon = 0.01 * cv2.arcLength(big_contour, True)
approximations = cv2.approxPolyDP(big_contour, epsilon, True)
cv2.drawContours(imageread, [approximations], 0, (255,255,0), 3)
i, j = approximations[0][0]
if len(approximations) == 3:
    cv2.putText(imageread, "Triangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
    print("triangle")
elif len(approximations) == 4:
    cv2.putText(imageread, "Rectangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
    print("rectangle")

elif len(approximations) == 5:
    cv2.putText(imageread, "Pentagon", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
    print("pentagon")

elif 6 < len(approximations) < 15:
    cv2.putText(imageread, "Ellipse", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
    print("ellipse")

else:
    cv2.putText(imageread, "Circle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
    print("circle")

#
# for count in imagecontours:
#     epsilon = 0.01 * cv2.arcLength(count, True)
#     approximations = cv2.approxPolyDP(count, epsilon, True)
#     cv2.drawContours(imageread, [approximations], 0, (0), 3)
#
#     i, j = approximations[0][0]
#     if len(approximations) == 3:
#         cv2.putText(imageread, "Triangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
#     elif len(approximations) == 4:
#         cv2.putText(imageread, "Rectangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
#     elif len(approximations) == 5:
#         cv2.putText(imageread, "Pentagon", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
#     elif 6 < len(approximations) < 15:
#         cv2.putText(imageread, "Ellipse", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
#     else:
#         cv2.putText(imageread, "Circle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
#
cv2.imshow("image", imageread)
cv2.waitKey(0)