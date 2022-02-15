from __future__ import annotations

from typing import Callable, Optional, Final

from numpy import array as np_array

from Model.size import Size
from data_resource.digit_value import Limits


class SurfacePropertyMemento:
    __slots__ = ['target', 'history', 'current_version']

    def __init__(self, obj: SurfaceProperty):
        self.target = obj
        self.history: [SurfaceProperty] = list()
        self.add()
        self.current_version = -1

    def get_prev(self):
        self.current_version = self.current_version - 1 if self.current_version > 0 else 0
        try:
            surf = self.history[self.current_version]
        except IndexError:
            self.current_version = 0
            surf = self.history[self.current_version]

        self.target.set_from_copy(surf)

    def add(self):
        sum_size = 0
        for s in self.history:
            sum_size += s.__sizeof__()

        if len(self.history) > 100:
            self.history.pop(0)
        self.current_version = len(self.history) - 1
        self.history.append(self.target.get_copy())

    def get_next(self):
        self.current_version += 1
        try:
            surf = self.history[self.current_version]
        except IndexError:
            self.current_version = len(self.history) - 1
            surf = self.history[self.current_version]
        self.target.set_from_copy(surf)


class SurfaceProperty:  # z - высота слоя
    __slots__ = 'pre_x', 'pre_y', 'start_x', 'start_y', '__x', '__y', '__z', 'primary', 'size', 'split_line'
    base_scale: Final = 10

    def __init__(self, size: Size = Size(), z: int = -1):
        self.pre_x, self.pre_y, self.start_x, self.start_y, self.__z = None, None, None, None, z
        self.__x: [float] = list()
        self.__y: [float] = list()
        self.split_line = (None, None)

        self.size = size
        self.primary = True

    @property
    def x(self) -> [float]:
        return self.__x

    @x.setter
    def x(self, value: [float]):
        self.__x = value

    @property
    def y(self) -> [float]:
        return self.__y

    @y.setter
    def y(self, value: [float]):
        self.__y = value

    @property
    def z(self) -> int:
        return self.__z

    @z.setter
    def z(self, value: int):
        if value in range(Limits.MINHEIGHT, Limits.MAXHEIGHT+1):
            self.__z = value
        elif value > Limits.MAXHEIGHT:
            self.__z = Limits.MAXHEIGHT

    @property
    def curve(self) -> ([float], [float]):
        if self.x and self.y:
            if self.x[0] != self.x[-1] or self.y[0] != self.y[-1]:
                return self.x + [self.x[0]], self.y + [self.y[0]]
        return self.x, self.y

    @curve.setter
    def curve(self, value: ([float], [float])):
        self.x, self.y = value

    @property
    def scalable_curve(self) -> ([float], [float]):
        x, y = self.curve
        if self.size:
            x, y = np_array(x), np_array(y)
            x = x * (self.size.x / self.base_scale)
            y = y * (self.size.y / self.base_scale)
            x, y = x.tolist(), y.tolist()
        return x, y

    def get_copy(self) -> SurfaceProperty:
        this_copy = SurfaceProperty()
        self.__copying(self, this_copy)
        return this_copy

    @staticmethod
    def __copying(from_property: SurfaceProperty, to_property: SurfaceProperty):
        for slot in SurfaceProperty.__slots__:
            attribute_name = slot.replace('__', '')
            if hasattr(from_property.__getattribute__(attribute_name), "copy"):
                to_property.__setattr__(attribute_name, from_property.__getattribute__(attribute_name).copy())
            else:
                to_property.__setattr__(attribute_name, from_property.__getattribute__(attribute_name))

    def set_from_copy(self, copy: SurfaceProperty):
        self.__copying(copy, self)


class Surface(SurfaceProperty):
    __slots__ = ['__prev_layer', '__next_layer', 'memento']

    def __init__(self, size: Size = Size(), z: int = -1, lay: dict = None):
        super(Surface, self).__init__(size, z)
        self.__next_layer: () = lambda x: None
        self.__prev_layer: () = lambda x: None
        self.memento = SurfacePropertyMemento(self)

        if lay:
            self.load_surface_from_dict(lay)

    @property
    def prev_layer(self) -> Optional[Surface]:
        return self.__prev_layer(self.z)

    @prev_layer.setter
    def prev_layer(self, method: Callable):
        self.__prev_layer = method

    @property
    def next_layer(self) -> Optional[Surface]:
        return self.__next_layer(self.z)

    @next_layer.setter
    def next_layer(self, method):
        self.__next_layer = method

    def dot_value_change(self, index, x, y) -> None:
        if self.x and self.y:
            if 0 <= index <= len(self.x):
                self.x[index], self.y[index] = x, y
                self.memento.add()

    def insert_dot(self, index: int, x1: float, y1: float):
        if type(index) is int:
            self.x.insert(index, x1)
            self.y.insert(index, y1)
            self.memento.add()
        else:
            print('type error: index is ', type(index), ' = ', index)

    def pop_dot(self, index: int):
        if index in range(0, len(self.x) + 1):
            self.x.pop(index)
            self.y.pop(index)
            self.memento.add()

    def set_pre_dot(self, x1: float, y1: float):
        self.pre_x, self.pre_y = x1, y1
        self.add_dot(x1, y1)

    def set_start_dot(self, x1: float, y1: float):
        self.start_x, self.start_y = x1, y1
        self.set_pre_dot(x1, y1)

    def add_dot(self, x1: float, y1: float):
        self.insert_dot(len(self.x), x1, y1)

    def clear(self):
        self.memento.add()
        self.x, self.y = list(), list()

    def get_surface_as_dict(self) -> dict:
        x, y = self.curve
        return {'x': x, 'y': y, 'z': self.z, 'primary': self.primary}

    def load_surface_from_dict(self, dictionary: dict):
        for field_name in dictionary:
            if field_name == 'x':
                self.x = dictionary.get('x')
            elif field_name == 'y':
                self.y = dictionary.get('y')
            elif field_name == 'z':
                self.z = dictionary.get('z')
            elif field_name == 'primary':
                self.primary = dictionary.get('primary')
        self.memento.add()
