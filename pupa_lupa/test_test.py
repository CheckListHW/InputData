import matplotlib.pyplot as plt

from Model.line_segment_and_point import LineSegment, Point

from Tools.geometry.angle_line import intersection_segment_dot
from Tools.geometry.split_square import rectangle

if __name__ == '__main__':
    a_1 = -0.008705447393006271
    a_2 = 3.087054473930063
    b_1 = 9.991294552606993
    b_2 = 4.087054473930063
    line = LineSegment(Point(a_1, a_2), Point(b_1, b_2))
    line1 = LineSegment(Point(-22, 10), Point(-22, 0))
    rect = rectangle(10, 10)
    b = rect.dots[0]
    xxx, yyy = [], []
    for a in rect.dots:
        xx, yy = intersection_segment_dot(line.a, line.b, a, b, vector=True)
        plt.scatter(xx, yy)

        print(xx, yy)

        if xx is not None and yy is not None:
            xxx.append(xx)
            yyy.append(yy)
        b = a
    plt.plot(xxx, yyy)
    plt.plot(rect.get_x(), rect.get_y())
    plt.show()
