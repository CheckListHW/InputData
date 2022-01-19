from typing import List


class Dot:
    __slots__ = ['x', 'y', 'index', 'distance']

    def __init__(self, index, distance, x, y):
        self.index = index
        self.distance = distance
        self.x = x
        self.y = y


def halve_dot_count(x: [float], y: [float]) -> ([float], [float]):
    new_x, new_y = x.copy(), y.copy()
    while len(new_x) > len(x)/2:
        new_x, new_y = dot_count_minus_one(new_x, new_y, pop_dot_count=int(len(x)*0.05)+1)

    return new_x, new_y


def dot_count_minus_one(x: [float], y: [float], pop_dot_count: int = 1) -> ([float], [float]):
    if min(len(x), len(y)) < 10:
        return x, y

    dots: List[Dot] = list()

    for i in range(1, min(len(x), len(y)) - 1):
        distance_ab = ((x[i - 1] - x[i]) ** 2 + (y[i - 1] - y[i]) ** 2) ** 0.5
        distance_bc = ((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2) ** 0.5
        dots.append(Dot(i, distance_ab + distance_bc, x[i], y[i]))

    dots.sort(key=lambda j: j.distance)
    for _ in range(pop_dot_count):
        dots.pop(0)
    dots.sort(key=lambda j: j.index)

    xx: List[float] = list()
    yy: List[float] = list()

    xx.append(x[0])
    yy.append(y[0])

    for d in dots:
        xx.append(d.x)
        yy.append(d.y)

    xx.append(x[-1])
    yy.append(y[-1])

    print('halve', len(xx), len(yy))

    return xx, yy
