import math


def getAngle(pointsList):
    b, a, c = pointsList[-3:]
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle_magnitude = ang if ang > 0 else -ang
    return angle_magnitude
