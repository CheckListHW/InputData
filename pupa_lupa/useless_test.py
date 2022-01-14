# intersection function
from math import sqrt


def isect_line_plane_v3(p0, p1, h):
    p_co, p_no = [h, h, h], [h, h, h]
    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > 1e-6:
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = u[0] * fac, u[1] * fac, u[2] * fac
        return p0[0] + u[0], p0[1] + u[1], p0[2] + u[2]
    else:
        return None


def sub_v3v3(v0, v1):
    return v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2],


def dot_v3v3(v0, v1):
    return (v0[0] * v1[0]) + (v0[1] * v1[1]) + (v0[2] * v1[2])

if __name__ == "__main__":
    x1, y1, z1 = 0, 0, 0
    x2, y2, z2 = 5, 5, 5
    hight = 3

    x3 = abs(x1-x2)
    y3 = abs(y1-y2)
    z3 = abs(z1-z2)

    AB = sqrt(x3**2+y3**2+y3**2)
    print(AB)

    xx = min(x1, x2)+(hight/z3)*AB
    yy = min(y1, y2)+(hight/z3)*AB

    print(xx, yy)