# z - высота слоя
from __future__ import annotations

from typing import Callable, Optional


class SurfaceProperty:
    __slots__ = ['pre_x', 'pre_y', 'start_x', 'start_y', '__x', '__y', '__z', 'primary', '__size_x', '__size_y']

    def __init__(self, z: int = -1):
        self.pre_x, self.pre_y, self.start_x, self.start_y, self.__z = None, None, None, None, z
        self.__x: [float] = list()
        self.__y: [float] = list()
        self.__size_x = 15
        self.__size_y = 15
        self.primary = True

    @property
    def x(self) -> [int]:
        return self.__x

    @x.setter
    def x(self, value: [int]):
        self.__x = value

    @property
    def y(self) -> [int]:
        return self.__y

    @y.setter
    def y(self, value: [int]):
        self.__y = value

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value):
        if value >= 0:
            self.__z = value

    @property
    def curve(self) -> ([int], [int]):
        if self.x and self.y:
            if self.x[0] != self.x[-1] or self.y[0] != self.y[-1]:
                return self.x + [self.x[0]], self.y + [self.y[0]]
        return self.x, self.y

    @curve.setter
    def curve(self, value: ([int], [int])):
        self.x, self.y = value

    @property
    def size_x(self) -> int:
        return self.__size_x

    @size_x.setter
    def size_x(self, value: int):
        self.__size_x = int(value)

    @property
    def size_y(self) -> int:
        return self.__size_y

    @size_y.setter
    def size_y(self, value: int):
        self.__size_y = int(value)

    def size(self) -> int:
        return min([len(self.x), len(self.y)])


class Surface(SurfaceProperty):
    __slots__ = ['__prev_layer', '__next_layer']

    def __init__(self, z: int = -1, lay: dict = None):
        super(Surface, self).__init__(z)
        self.__next_layer: () = lambda x: None
        self.__prev_layer: () = lambda x: None

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

    def insert_dot(self, index: int, x1: float, y1: float):
        self.x.insert(index, x1)
        self.y.insert(index, y1)

    def pop_dot(self, index: int):
        if index in range(0, len(self.x) + 1):
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

    def clear(self):
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
