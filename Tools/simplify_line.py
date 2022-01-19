from Tools.intersection_point_horizontal_plane import intersection_point_horizontal_plane


def simplify_line(x: [float], y: [float], dot_count: int) -> ([int], [int]):
    if len(x) <= dot_count or len(y) <= dot_count or dot_count < 3:
        return x, y
    total_len = 0
    for i in range(len(x) - 1):
        x1, x2, y1, y2 = x[i], x[i + 1], y[i], y[i + 1]
        total_len += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    current_len, step, simplify_x, simplify_y = 0, total_len / dot_count, [x[0]], [y[0]]

    # for i in range(len(x) - 1):
    i = 0
    while len(simplify_y) < dot_count:
        while i >= len(x)/2:
            x = x + x
            y = y + y

        while x[i] == x[i + 1] or y[i] == y[i + 1]:
            i += 1

        x1, x2, y1, y2 = x[i], x[i + 1], y[i], y[i + 1]
        distance_between_dots = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if current_len + distance_between_dots > step:
            percent = (step - current_len) / distance_between_dots

            x3, y3, _ = intersection_point_horizontal_plane([x1, y1, 0], [x2, y2, 1000], int(percent * 1000))
            simplify_x.append(x3)
            simplify_y.append(y3)
            current_len = current_len + distance_between_dots - step
        else:
            current_len += distance_between_dots
        i += 1

    return simplify_x, simplify_y
