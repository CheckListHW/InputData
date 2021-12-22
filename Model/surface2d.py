class SurfaceFigure2d:
    def __init__(self):
        self.pre_x, self.pre_y, self.start_x, self.start_y = None, None, None, None

        self.priority: int = 1
        self.x = list()
        self.y = list()

    def set_priority(self, value: int):
        self.priority = int(value)

    def insert_dot(self, index: int, x1: float, y1: float):
        if 0 < index <= len(self.x):
            self.x.insert(index, x1)
            self.y.insert(index, y1)

    def pop_dot(self, index: int):
        if 0 < index <= len(self.x):
            self.x.pop(index)
            self.y.pop(index)

    def set_pre_dot(self, x1: float, y1: float):
        self.pre_x, self.pre_y = x1, y1
        self.add_dot(x1, y1)

    def set_start_dot(self, x1: float, y1: float):
        self.start_x, self.start_y = x1, y1
        self.set_pre_dot(x1, y1)

    def add_dot(self, x1: float, y1: float):
        self.x.append(x1)
        self.y.append(y1)

    def max_x(self) -> int:
        return int(max(self.x) + 0.999)

    def max_y(self) -> int:
        return int(max(self.y) + 0.999)

    def clear(self):
        self.x = list()
        self.y = list()
