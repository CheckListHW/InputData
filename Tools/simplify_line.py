from typing import Optional

from Tools.intersection_point_horizontal_plane import intersection_point_horizontal_plane


def simplify_line(x: [float], y: [float], dot_count: Optional[int] = None) -> ([int], [int]):
    if not dot_count:
        dot_count = int(min(len(x), len(y)))

    if len(x) < dot_count or len(y) < dot_count or dot_count < 2:
        return x, y

    x1, y1, total_len = x[0], y[0], 0
    distance_to_dot = list()
    for x2, y2 in zip(x, y):
        total_len += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        distance_to_dot.append(total_len)
        x1, y1 = x2, y2

    total_len_main, total_len_simplify, step = 0, 0, total_len / (dot_count - 1)
    simplify_x, simplify_y, x1, y1 = [], [], x[0], y[0]

    for i in range(1, len(x)):
        x1, x2, y1, y2 = x[i - 1], x[i], y[i - 1], y[i]
        distance_between_dots = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 + 0.000001
        while round(distance_to_dot[i], 4) + 0.0001 >= round(total_len_simplify, 4):
            percent = 1 - (distance_to_dot[i] - total_len_simplify) / distance_between_dots
            total_len_simplify += step
            x3, y3, _ = intersection_point_horizontal_plane([x1, y1, 0], [x2, y2, 1000], int(percent * 1000))
            simplify_y.append(y3)
            simplify_x.append(x3)

    while len(simplify_x) > dot_count:
        simplify_x.pop(-2)
        simplify_y.pop(-2)

    return simplify_x, simplify_y
