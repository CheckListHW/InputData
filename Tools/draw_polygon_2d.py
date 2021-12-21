def draw_polygon(x, y, ax, size=1, color='brown'):
    int_x, int_y = int(x), int(y)
    ax.fill([int_x, int_x + size, int_x + size, int_x, int_x],
            [int_y, int_y, int_y + size, int_y + size, int_y], color=color)
