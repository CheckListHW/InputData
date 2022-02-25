import math
import random

import matplotlib.pyplot as plt

from Model.line_segment_and_point import Point, LineSegment
from Tools.geometry.angle_line import reverse_dot
from Tools.geometry.calc_offset import calc_offset
from Tools.geometry.point_in_polygon import check_point_in_polygon
from Tools.plot_prepare import plot_prepare
from pupa_lupa.data import x, y

base_scale = 10

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot()
    plot_prepare(ax, base_scale)

    r: () = lambda: random.randint(0, 10)

    a, b = [8, 7], [4, 2]

    x1, y1 = reverse_dot(a, b)
    plt.plot(x1, y1)
    x, y = [0.18984209816006103, 0.18984209816006103, 9.816186063250708, 9.849, 0.171, 0.18984209816006103,
            0.18984209816006103], \
           [9.756219903691814, 9.756219903691814, 9.792335473515248, 5.0, 5.0, 9.756219903691814, 9.756219903691814]
    x1, y1 = 6, 9
    print(int(x1) + 0.5)
    point = check_point_in_polygon(x, y, math.ceil(x1) + 0.5, math.ceil(y1) + 0.5)
    plt.scatter(math.ceil(x1) + 0.5, math.ceil(y1) + 0.5)
    print(point)

    plt.plot(x, y)
    plt.show()
