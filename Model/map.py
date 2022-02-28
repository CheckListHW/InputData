from typing import List

from Model.line_segment_and_point import LineSegment
from Model.size import Size
from Model.shape import Shape
from Model.observer import Subject
from Model.surface import Surface
from Tools.filedialog import dict_from_json


class Map(Subject):
    __slots__ = 'size', 'shapes'

    def __init__(self):
        super().__init__()
        self.size = Size(message='map')
        self.shapes: [Shape] = list()

    def add_layer(self, figure: Shape = None) -> Shape:
        if not figure:
            figure = Shape(size=self.size)
        if not figure.size:
            figure.size = self.size
        if not figure._observers:
            figure._observers = self._observers

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
        shapes_with_split = []
        for shape in self.get_shapes():
            shapes_with_split = shapes_with_split + shape.spliting_shape()
        return sorted(filter(lambda i: i.visible is True, shapes_with_split), key=lambda i: i.priority).__reversed__()

    def load_from_dict(self, dictionary: dict):
        self.shapes = list()
        for lay in dictionary:
            fig = Shape(size=self.size)
            fig.load_from_dict(dictionary[lay])
            self.add_layer(fig)

        self.notify()

    def load_from_json(self, path: str):
        self.load_from_dict(dict_from_json(path))

    def update_size(self):
        x_start, x_finish = self.size.x_constraints.start, self.size.x_constraints.end
        y_start, y_finish = self.size.y_constraints.start, self.size.y_constraints.end
        z_finish = self.size.z_constraints.end

        for shape in self.shapes:
            for surf in shape.layers:
                s: Surface = surf
                min_x, min_y = s.get_min_x_and_y()
                max_x, max_y = s.get_max_x_and_y()
                if min_x is not None:
                    x_start = min_x if min_x < x_start else x_start
                if min_y is not None:
                    y_start = min_y if min_y < y_start else y_start
                if max_x is not None:
                    x_finish = max_x if max_x > x_finish else x_finish
                if max_y is not None:
                    y_finish = max_y if max_y > y_finish else y_finish

            z_finish = shape.height if shape.height > z_finish else z_finish

        self.size.x_constraints.start, self.size.x_constraints.end = x_start, x_finish
        self.size.y_constraints.start, self.size.y_constraints.end = y_start, y_finish
        self.size.z_constraints.end = z_finish

    @property
    def height(self) -> int:
        return max(self.shapes, key=lambda i: i.height).height
