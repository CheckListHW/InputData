def draw_polygon(x, y, ax):
    int_x, int_y = int(x), int(y)
    ax.fill([int_x, int_x + 1, int_x + 1, int_x, int_x],
            [int_y, int_y, int_y + 1, int_y + 1, int_y], color='brown')