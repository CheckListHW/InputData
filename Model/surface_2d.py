# z - высота слоя
class SurfaceFigure2d:
    __slots__ = ['pre_x', 'pre_y', 'start_x', 'start_y', 'x', 'y', 'z']

    def __init__(self, z: int = -1, lay: dict = None):
        self.pre_x, self.pre_y, self.start_x, self.start_y, self.z = None, None, None, None, z
        self.x, self.y = list(), list()

        if lay:
            self.load_surface_from_dict(lay)

    def max_x(self) -> int:
        return int(max(self.x + [0]) + 0.999)

    def max_y(self) -> int:
        return int(max(self.y + [0]) + 0.999)

    def insert_dot(self, index: int, x1: float, y1: float):
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

    def clear(self):
        self.x, self.y = list(), list()

    def get_surface_as_dict(self) -> dict:
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def load_surface_from_dict(self, dictionary: dict):
        print(dictionary)
        for field_name in dictionary:
            print(field_name)
            if field_name == 'x':
                self.x = dictionary.get('x')
            elif field_name == 'y':
                self.y = dictionary.get('y')
            elif field_name == 'z':
                self.z = dictionary.get('z')

    def square_layer_test(self, border: int):
        max_y, max_x = 15, 15
        self.add_dot(1+border, 1+border)
        self.add_dot(1+border, max_y - 1-border)
        self.add_dot(max_x - 1-border, max_y - 1-border)
        self.add_dot(max_x - 1-border, 1+border)
