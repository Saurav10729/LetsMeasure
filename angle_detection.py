import math


def gradient(pt1, pt2):
    try:
        x = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    except ZeroDivisionError:
        return 10000

def getAngle(pointsList):
    b,a,c = pointsList[-3:]
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    angle_magnitude = ang if ang>0 else -ang
    return angle_magnitude

# def get_angle(pointsList):
#     pt1, pt2, pt3 = pointsList[-3:]
#     m1 = gradient(pt1, pt2)
#     m2 = gradient(pt1, pt3)
#     if m1 == 10000 or m2 == 10000 :
#         angD = 90
#     else:
#         angR = math.atan((m2 - m1) / (1 + (m2 * m1)))
#         angD = abs(round(math.degrees(angR)))
#     return angD
