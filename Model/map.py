import sys
from typing import Optional

from Model.json_in_out import JsonInOut
from Model.observer import Subject
from Model.roof_profile import RoofProfile, RoofPoint
from Model.shape import Shape
from Model.size import Size
from Model.surface import Surface
from Tools.filedialog import dict_from_json


def pop_from_dict(dict_value: dict, name: str):
    dict_value[name] = False
    dict_value.pop(name)


class Map(Subject, JsonInOut):
    __slots__ = 'size', 'shapes', 'roof_profile',

    def __init__(self):
        super().__init__()
        self.size = Size()
        self.roof_profile = RoofProfile()
        self.shapes: [Shape] = list()

    def add_layer(self, figure: Shape = None) -> Shape:
        if not figure:
            figure = Shape(size=self.size)
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
        for shape in self.shapes:
            shapes_with_split = shapes_with_split + shape.splitting_shape()
        return sorted(filter(lambda i: i.visible is True, shapes_with_split), key=lambda i: i.priority).__reversed__()

    def get_shape_with_part(self) -> [Shape]:
        layers = []
        for layer in self.get_shapes():
            layers.append(layer)
            for part_name in layer.parts_property:
                layers.append(layer.parts_property[part_name])

        return layers

    def load_from_dict(self, load_dict: dict):
        self.shapes = []
        self.roof_profile = RoofProfile()
        for name_property in load_dict:
            if name_property == 'shapes':
                for lay in load_dict[name_property]:
                    self.add_layer(Shape(size=self.size, load_dict=lay))
            elif name_property == 'roof_profile':
                self.roof_profile.load_from_dict(load_dict[name_property])
            elif hasattr(self, name_property):
                if hasattr(getattr(self, name_property), 'load_from_dict'):
                    getattr(self, name_property).load_from_dict(load_dict[name_property])
                else:
                    self.__setattr__(name_property, load_dict[name_property])

    def get_as_dict(self) -> dict:
        map_dict = super(Map, self).get_as_dict()
        for d in map_dict:
            if d == 'shapes':
                for shape in map_dict[d]:
                    pop_from_dict(shape, 'size')
                    pop_from_dict(shape, 'split_shapes')
                    for name in shape.get('parts_property'):
                        pop_from_dict(shape['parts_property'][name], 'size')
                        pop_from_dict(shape['parts_property'][name], 'layers')
                        pop_from_dict(shape['parts_property'][name], 'splits')
                        pop_from_dict(shape['parts_property'][name], 'split_shapes')
                        pop_from_dict(shape['parts_property'][name], 'parts_property')
                    pop_layer_number = []
                    for lay, i in zip(shape['layers'], range(len(shape['layers']))):
                        if lay.get('primary') is True:
                            pop_from_dict(lay, 'size')
                            pop_from_dict(lay, 'pre_x')
                            pop_from_dict(lay, 'pre_y')
                            pop_from_dict(lay, 'start_x')
                            pop_from_dict(lay, 'start_y')
                            pop_from_dict(lay, 'splits')
                            pop_from_dict(lay, 'current_split')
                        elif lay.get('primary') is False:
                            pop_layer_number.append(i)
                    for i in pop_layer_number.__reversed__():
                        shape['layers'].pop(i)

        return map_dict

    def load_from_json(self, path: str):
        map_dict = dict_from_json(path)
        print(map_dict)
        self.load_from_dict(map_dict)

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
        if len(self.shapes) > 0:
            return max(self.shapes, key=lambda i: i.height).height
        else:
            return 0

    @property
    def height_with_offset(self) -> int:
        max_offset = int(max(self.roof_profile.points + [RoofPoint(x=0, z=0, y=0)], key=lambda i: i.z).z + 1)
        return max(self.shapes, key=lambda i: i.height_with_offset).height_with_offset + max_offset
