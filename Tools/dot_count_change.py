class Dot:
    __slots__ = ['x', 'y', 'index', 'distance']

    def __init__(self, index, distance, x, y):
        self.index = index
        self.distance = distance
        self.x = x
        self.y = y


def halve_dot_count(x: [float], y: [float]) -> ([float], [float]):
    if min(len(x), len(y)) < 10:
        return x, y

    dots: [Dot] = list[Dot]()

    for i in range(1, min(len(x), len(y)) - 1):
        distance_ab = ((x[i - 1] - x[i]) ** 2 + (y[i - 1] - y[i]) ** 2) ** 0.5
        distance_bc = ((x[i + 1] - x[i]) ** 2 + (y[i + 1] - y[i]) ** 2) ** 0.5
        dots.append(Dot(i, distance_ab + distance_bc, x[i], y[i]))

    dots.sort(key=lambda j: j.distance)
    dots = dots[int(len(dots)/2):-1]
    dots.sort(key=lambda j: j.index)

    xx = list[float]()
    yy = list[float]()

    xx.append(x[0])
    yy.append(y[0])

    for d in dots:
        xx.append(d.x)
        yy.append(d.y)

    xx.append(x[-1])
    yy.append(y[-1])

    print('halve', len(xx), len(yy))

    return xx, yy
