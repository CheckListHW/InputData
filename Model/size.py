class AxisConstraints:
    __slots__ = ['__start', '__end', '__scale']

    def __init__(self, start, end):
        self.__start = start
        self.__end = end

    def change_constraints(self, start=None, end=None):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value: int):
        try:
            value = abs(int(value))
            self.__start = value if type(value) == int else self.__start
        except:
            pass

    @property
    def end(self) -> int:
        return self.__end

    @end.setter
    def end(self, value: int):
        try:
            value = abs(int(value))
            self.__end = value if type(value) == int else self.__end
        except:
            pass


class Size:
    __slots__ = ['x_constraints', 'y_constraints', 'z_constraints']

    def __init__(self, x_start=0, x_end=10, y_start=0, y_end=10, z_start=0, z_end=10):
        self.x_constraints = AxisConstraints(x_start, x_end)
        self.y_constraints = AxisConstraints(y_start, y_end)
        self.z_constraints = AxisConstraints(z_start, z_end)

    def change_constraints(self, x_start=None, x_end=None, y_start=None, y_end=None, z_start=None, z_end=None):
        self.x_constraints.change_constraints(x_start, x_end)
        self.y_constraints.change_constraints(y_start, y_end)
        self.z_constraints.change_constraints(z_start, z_end)

    @property
    def x(self) -> int:
        return int(abs(self.x_constraints.start - self.x_constraints.end))

    @property
    def y(self):
        return int(abs(self.y_constraints.start - self.y_constraints.end))

    @property
    def z(self):
        return int(abs(self.z_constraints.start - self.z_constraints.end))

    def max(self):
        return max([0, self.y, self.x, self.z])
