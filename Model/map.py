import random

from Model.shape import Shape
from Model.observer import Subject
from Tools.filedialog import dict_from_json


class Map(Subject):
    def __init__(self):
        super().__init__()
        self.__size_x = 15
        self.__size_y = 15
        self.__size_z = 15
        self.shapes: [Shape] = list()

    def set_size(self, x: int, y: int, z: int):
        if

    def add_layer(self, figure: Shape = None) -> Shape:
        if not figure:
            figure = Shape(name='layer {0}'.format(len(self.shapes)))
        figure._observers = self._observers
        figure.set_size(self.__size_x, self.__size_y, self.__size_z)
        self.shapes.append(figure)
        self.notify()
        return figure

    def delete_layer(self, index: int = None, figure: Shape = None):
        if index:
            self.shapes.pop(index)
        if figure:
            self.shapes.remove(figure)
        self.notify()

    def get_shapes(self) -> [Shape]:
        return self.shapes

    def get_visible_shapes(self) -> [Shape]:
        return sorted(filter(lambda i: i.visible is True, self.get_shapes()), key=lambda i: i.priority).__reversed__()

    def load_from_dict(self, dictionary: dict):
        load_shapes: [Shape] = list()
        for lay in dictionary:
            fig = Shape()
            fig.load_from_dict(dictionary[lay])
            load_shapes.append(fig)

        self.shapes = load_shapes
        self.notify()

    def load_from_json(self, path: str):
        self.load_from_dict(dict_from_json(path))

    def size(self, axis: str) -> int:
        if axis == 'x':
            return self.__size_x
        elif axis == 'y':
            return self.__size_y
        elif axis == 'z':
            return self.__size_z
        else:
            return max(self.__size_z, self.__size_x, self.__size_y)

