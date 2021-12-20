def nearst_dot_index(dots_x, dots_y, x, y):
    if len(dots_x) < 1:
        return None, None

    current_distance = ((dots_x[0] - x) ** 2 + (dots_y[0] - y) ** 2) ** 0.5

    j = 0
    for i in range(len(dots_x)):
        distance = ((dots_x[i] - x) ** 2 + (dots_y[i] - y) ** 2) ** 0.5
        if distance < current_distance:
            current_distance = distance
            j = i

    print(j)

    return j


def nearst_dot_value(dots_x, dots_y, x, y):
    i = nearst_dot_index(dots_x, dots_y, x, y)
    print('nearst_dot_value', i)
    return dots_x[i], dots_y[i]
