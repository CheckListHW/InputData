from Tools.recursive_extraction_of_list import recursive_extraction


class AxisConstraints:
    __slots__ = ['_start', '_end']

    def __init__(self, start, end):
        self._start = start
        self._end = end

    def change_constraints(self, start=None, end=None):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: int):
        try:
            value = abs(int(value))
            self._start = value if type(value) == int else self._start
        except:
            pass

    @property
    def end(self) -> int:
        return self._end

    @end.setter
    def end(self, value: int):
        try:
            value = abs(int(value))
            self._end = value if type(value) == int else self._end
        except:
            pass

    def get_as_dict(self) -> dict:
        my_dict = {}
        this_class = AxisConstraints
        for slot in this_class.__slots__:
            my_dict[slot] = recursive_extraction(getattr(self, slot))
        return my_dict

    def load_from_dict(self, load_dict: dict):
        for name_property in load_dict:
            if hasattr(self, name_property):
                self.__setattr__(name_property, load_dict[name_property])


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

    def get_as_dict(self) -> dict:
        my_dict = {}
        for slot in self.__slots__:
            if hasattr(self, slot):
                sub_slot = self.__getattribute__(slot)
                my_dict[slot] = sub_slot.get_as_dict() if hasattr(sub_slot, 'get_as_dict') else sub_slot
        return my_dict

    def load_from_dict(self, load_dict: dict):
        for name_property in load_dict:
            if name_property == 'x_constraints':
                self.x_constraints = AxisConstraints(None, None)
                self.x_constraints.load_from_dict(load_dict[name_property])
            elif name_property == 'y_constraints':
                self.y_constraints = AxisConstraints(None, None)
                self.y_constraints.load_from_dict(load_dict[name_property])
            elif name_property == 'z_constraints':
                self.z_constraints = AxisConstraints(None, None)
                self.z_constraints.load_from_dict(load_dict[name_property])
            else:
                if hasattr(self, name_property):
                    self.__setattr__(name_property, load_dict[name_property])

        pass
