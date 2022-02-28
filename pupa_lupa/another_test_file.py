import random

from matplotlib import pyplot as plt

from Model.line_segment_and_point import Point, LineSegment, PolygonalChain
from Tools.geometry.split_square import split_square

if __name__ == '__main__':
    base_value = 10
    r: () = lambda: random.randint(-5, 15)

    # [0.0, 10.0][5.061195826645265, 4.681982343499198]

    line = LineSegment(Point(0.0, 5.061195826645265), Point(10.0, 4.681982343499198))

    # print(line.a.x, line.a.y, line.b.x, line.b.y)

    plt.plot(line.get_x(), line.get_y())

    square = PolygonalChain()

    for x1, y1 in zip([0, base_value, base_value, 0, 0], [0, 0, base_value, base_value, 0]):
        square.add_dot(x1, y1)

    chain1, chain2 = split_square(square, line)

    plt.plot(chain1.get_x(), chain1.get_y())
    plt.plot(chain2.get_x(), chain2.get_y())
    plt.show()
