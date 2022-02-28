from __future__ import annotations

from Model.json_in_out import JsonInOut


class Point(JsonInOut):
    __slots__ = 'x', 'y', 'z'

    def __init__(self, x: float = None, y: float = None, z: float = None, load_dict: dict = None):
        self.set(x, y, z)

        if load_dict:
            self.load_from_dict(load_dict)

    def set(self, x: float, y: float, z: float = None):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
