class SurfaceFigure2d:
    def __init__(self):
        self.pre_x, self.pre_y, self.start_x, self.start_y = None, None, None, None

        self.priority: int = 1
        self.x_dots = list()
        self.y_dots = list()

    def set_priority(self, value: int):
        self.priority = int(value)

    def insert_dot(self, index: int, x: float, y: float):
        if 0 < index <= len(self.x_dots):
            self.x_dots.insert(index, x)
            self.y_dots.insert(index, y)

    def pop_dot(self, index: int):
        if 0 < index <= len(self.x_dots):
            self.x_dots.pop(index)
            self.y_dots.pop(index)

    def set_pre_dot(self, x: float, y: float):
        self.pre_x, self.pre_y = x, y
        self.add_dot(x, y)

    def set_start_dot(self, x: float, y: float):
        self.start_x, self.start_y = x, y
        self.set_pre_dot(x, y)

    def add_dot(self, x: float, y: float):
        self.x_dots.append(x)
        self.y_dots.append(y)

    def max_x(self) -> int:
        return int(max(self.x_dots) + 0.999)

    def max_y(self) -> int:
        return int(max(self.y_dots) + 0.999)

    def clear(self):
        self.x_dots = list()
        self.y_dots = list()
