def check_point_in_polygon(curves_x, curves_y, x, y):
    entry, j = False, len(curves_x) - 1

    for i in range(0, len(curves_x)):
        if ((curves_y[i] < y <= curves_y[j] or curves_y[j] < y <= curves_y[i]) and
                (curves_x[i] + (y - curves_y[i]) / (curves_y[j] - curves_y[i]) * (curves_x[j] - curves_x[i]) < x)):
            entry = not entry
        j = i

    return entry
