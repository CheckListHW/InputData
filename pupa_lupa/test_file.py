import random

import matplotlib.pyplot as plt

from Model.line_segment_and_point import Point, LineSegment
from Tools.geometry.angle_line import reverse_dot
from Tools.geometry.calc_offset import calc_offset
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

    x_offset, y_offset = calc_offset(100, LineSegment(Point(8, 7), Point(4, 2)))
    plt.plot(x, y)
    for i in range(10):
        x = [x1 + x_offset for x1 in x]
        y = [y1 + y_offset for y1 in y]
        plt.plot(x, y)

    plt.show()
