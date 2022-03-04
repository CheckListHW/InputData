from functools import reduce

import matplotlib.pyplot as plt
import numpy as np

from Model.point import Point
from Tools.geometry.angle_line import intersection_segment_dot


class a:
    def __init__(self, val):
        self.val = [val]


if __name__ == '__main__':
    a = [24.668028141137512,
         24.43569422150883]
    b = [24.668028141137512,
         0.32855136436597054]

    c = [18.0, 0.0]
    d = [25.0, 15.0]

    plt.plot([a[0], b[0]], [a[1], b[1]])
    plt.plot([c[0], d[0]], [c[1], d[1]])

    x1, y1 = intersection_segment_dot(
        Point(a[0], a[1]), Point(b[0], b[1]), Point(c[0], c[1]), Point(d[0], d[1]))
    plt.scatter(x1, y1)

    print(x1, y1)

    plt.show()
