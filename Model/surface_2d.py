import json

from Tools.filedialog import save_as_json


class SurfaceFigure2d:
    __slots__ = ['pre_x', 'pre_y', 'start_x', 'start_y', 'priority', 'x', 'y', 'index']

    def __init__(self, lay: dict = None):
        self.pre_x, self.pre_y, self.start_x, self.start_y = None, None, None, None
        self.priority, self.index = 1, 0
        self.x, self.y = list[float](), list[float]()

        if lay:
            self.load_surface_from_dict(lay)

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

    def get_surface_as_dict(self) -> dict:
        return {'priority': self.priority, 'x': self.x, 'y': self.y}

    def save_as_json(self):
        save_as_json(self.get_surface_as_dict())

    def load_surface_from_json(self, filename: str):
        with open(filename) as f:
            surface = json.load(f)
            self.x = surface.get('x')
            self.y = surface.get('y')
            self.priority = surface.get('priority')

    def load_surface_from_dict(self, dictionary: dict):
        self.x = dictionary.get('x')
        self.y = dictionary.get('y')
        self.priority = dictionary.get('priority') if dictionary.get('priority') else 1


class Surface2dPlus(SurfaceFigure2d):

    def __init__(self, size=15):
        s = 15

        x = [s * .4, s * .4, s * .1, s * .1, s * .4, s * .4, s * .6, s * .6, s * .9, s * .9, s * .9, s * .6, s * .6]
        y = [s * .1, s * .4, s * .4, s * .6, s * .6, s * .9, s * .9, s * .6, s * .6, s * .4, s * .4, s * .4, s * .1]
        lay = {'x': x, 'y': y}
        super(Surface2dPlus, self).__init__(lay=lay)
