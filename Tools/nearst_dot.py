def nearst_dot_index(dots_x, dots_y, x, y):
    if len(dots_x) < 1:
        return None

    current_distance = ((dots_x[0] - x) ** 2 + (dots_y[0] - y) ** 2) ** 0.5

    j = 0
    for i in range(len(dots_x)):
        distance = ((dots_x[i] - x) ** 2 + (dots_y[i] - y) ** 2) ** 0.5
        if distance < current_distance:
            current_distance = distance
            j = i
    return j


def nearst_dot_value(dots_x, dots_y, x, y):
    i = nearst_dot_index(dots_x, dots_y, x, y)
    return dots_x[i], dots_y[i]


def nearst_line_index(dots_x, dots_y, x, y):
    if len(dots_x) < 1:
        return None, None

    centers_lines_x, centers_lines_y = list(), list()

    for i in range(1, len(dots_x)):
        centers_lines_x.append((dots_x[i-1] + dots_x[i])/2)
        centers_lines_y.append((dots_y[i-1] + dots_y[i])/2)

    index = nearst_dot_index(centers_lines_x, centers_lines_y, x, y)

    return index, index+1
