class SurfaceFigure2d:
    def __init__(self):
        self.pre_x, self.pre_y, self.start_x, self.start_y = None, None, None, None
        self.x_dots = list()
        self.y_dots = list()

    def set_pre_dot(self, x: int, y: int):
        self.pre_x, self.pre_y = x, y
        self.add_dot(x, y)

    def set_start_dot(self, x: int, y: int):
        self.start_x, self.start_y = x, y
        self.set_pre_dot(x, y)

    def add_dot(self, x: int, y: int):
        self.x_dots.append(x)
        self.y_dots.append(y)

    def size_x(self):
        return int(max(self.x_dots)+1)

    def size_y(self):
        return int(max(self.y_dots)+1)


class Figure3d:
    def __init__(self, height=1):
        if height < 1:
            return
        self.layers = [SurfaceFigure2d() for _ in range(height)]
        self.up = self.layers[0]
        self.bottom = self.layers[-1]

    def size_x(self):
        return max(self.layers, key=lambda i: i.size_x()).size_x()

    def size_y(self):
        return max(self.layers, key=lambda i: i.size_y()).size_y()

    def size_fig(self):
        print([self.size_x(), self.size_y(), len(self.layers)])
        return [self.size_x(), self.size_y(), len(self.layers)]
