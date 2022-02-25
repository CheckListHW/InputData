from __future__ import annotations

import random
from copy import deepcopy
from typing import List, Optional

import matplotlib.pyplot as plt

from Model.line_segment_and_point import LineSegment, Point
from Model.split import Split
from Tools.geometry.calc_offset import calc_offset
from Tools.geometry.point_in_polygon import check_point_in_polygon
from Tools.geometry.split_square import rectangle, split_square
from data_resource.digit_value import Limits
from Model.observer import Subject
from Model.size import Size
from Model.surface import Surface
from Tools.geometry.angle_line import intersection_segment_dot
from Tools.filedialog import dict_from_json

# alpha - прозрачнгость от 0 до 1
from Tools.geometry.intersection_point_horizontal_plane import intersection_point_horizontal_plane
from Tools.recursive_extraction_of_list import recursive_extraction
from Tools.geometry.simplify_line import simplify_line


class ShapeProperty(Subject):
    __slots__ = 'size', 'visible', '_alpha', '_priority', '_color', 'name', 'layers', 'split_parts', 'splits'

    def __init__(self, size: Size):
        super(ShapeProperty, self).__init__()
        self.split_parts: [Shape] = None
        self.splits: [Split] = [Split(), Split()]
        self.visible, self._alpha, self._priority = True, 0.9, 100
        self._color: (int, int, int) = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.name: str = 'layer 1'
        self.layers: List[Surface] = list()
        self.size = size

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value: float):
        if 0 <= value <= 1:
            self._alpha = value

    @property
    def color(self) -> (int, int, int):
        return self._color

    @color.setter
    def color(self, value: (int, int, int)):
        r, g, b = value
        if int(r) in range(256) and int(g) in range(256) and int(b) in range(256):
            self._color = [r, g, b]

    @property
    def height(self):
        return max(self.layers, key=lambda i: i.z).z

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value: int):
        value = int(value)
        if value in range(101):
            self._priority = value

    def get_as_dict(self) -> dict:
        my_dict = {}
        this_class = ShapeProperty
        for slot in this_class.__slots__:
            my_dict[slot] = recursive_extraction(getattr(self, slot))
        return my_dict

    def load_from_dict(self, settings: dict):
        for name_property in settings:
            if name_property.__contains__('layers'):
                self.layers = []
                for lay in settings[name_property]:
                    self.layers.append(Surface(size=self.size, load_dict=lay))
            elif name_property == 'splits':
                self.splits = []
                for split in settings[name_property]:
                    self.splits.append(Split())
                    self.splits[-1].load_from_dict(split)
            else:
                if hasattr(self, name_property):
                    if hasattr(self.__getattribute__(name_property), 'load_from_dict'):
                        self.__getattribute__(name_property).load_from_dict(settings[name_property])
                    else:
                        self.__setattr__(name_property, settings[name_property])
        self.notify()


class Shape(ShapeProperty):
    def __init__(self, size: Size, path: str = None) -> None:
        super().__init__(size)
        self.add_layer(Surface(size=self.size, z=0))

        if path:
            self.load_from_json(path)

    def get_next_layer(self, z: int) -> Optional[Surface]:
        layers_less = [lay for lay in self.layers if lay.z < z]
        if layers_less:
            return sorted(layers_less, key=lambda i: i.z)[-1]

    def spliting_shape(self, ) -> [Shape]:
        local_splits: [Split] = []
        for split in [split for split in self.splits if not split.line.is_empty()]:
            a = Point(round(split.line.a.x * self.size.x), round(split.line.a.y * self.size.y))
            b = Point(round(split.line.b.x * self.size.x), round(split.line.b.y * self.size.y))
            l_split: Split = Split()
            l_split.load_from_dict(split.get_as_dict())
            l_split.line = LineSegment(a, b)
            local_splits.append(l_split)

        split_shapes: [Shape] = [self]

        for split in local_splits:
            x_offset, y_offset = calc_offset(split.angle, split.line)
            # print(x_offset, y_offset, split.line.get_x(), split.line.get_y())
            # plt.plot(split.line.get_x(), split.line.get_y())
            copy_split_shapes = split_shapes.copy()
            split_shapes = []
            for cur_shape in copy_split_shapes:
                a_shape, b_shape = Shape(cur_shape.size), Shape(cur_shape.size)
                cur_shape.split_parts = [a_shape, b_shape]

                for lay_main in cur_shape.layers:
                    a_shape.layers.append(lay_main.get_copy())
                    a_shape.layers[-1].size = self.size
                    b_shape.layers.append(lay_main.get_copy())
                    b_shape.layers[-1].size = self.size
                    lay_a, lay_b = a_shape.layers[-1], b_shape.layers[-1]
                    lay_a.clear()
                    lay_b.clear()

                    a_x, a_y, b_x, b_y = split.line.a.x, split.line.a.y, split.line.b.x, split.line.b.y
                    level = lay_main.z if split.from_start else max(self.layers, key=lambda i: i.z).z - lay_main.z
                    a_x, a_y = a_x + (x_offset * level), a_y + (y_offset * level)
                    b_x, b_y = b_x + (x_offset * level), b_y + (y_offset * level)
                    old_split_level = LineSegment(Point(a_x, a_y), Point(b_x, b_y))
                    a_polygon, b_polygon, split_level \
                        = split_square(rectangle(cur_shape.size.x, cur_shape.size.y), old_split_level)

                    x1, x2, y1, y2 = old_split_level.a.x, old_split_level.b.x, old_split_level.a.y, old_split_level.b.y
                    a_sum = sum([(a.x - x1) * (y2 - y1) - (a.y - y1) * (x2 - x1) for a in a_polygon.dots])
                    b_sum = sum([(b.x - x1) * (y2 - y1) - (b.y - y1) * (x2 - x1) for b in b_polygon.dots])
                    if a_sum < 0 or b_sum > 0:
                        a_polygon, b_polygon = b_polygon, a_polygon

                    # print(lay_a.z, split.line.a.x, split.line.a.y, split.line.b.x, split.line.b.y)
                    # print(lay_a.z, a_x, a_y, b_x, b_y)
                    # print(lay_a.z, 'x_offset, y_offset', x_offset, y_offset)
                    # print(lay_a.z, split_level.get_x(), split_level.get_y())
                    # print(lay_a.z, a_polygon.get_x(), a_polygon.get_y())
                    # print(lay_a.z, b_polygon.get_x(), b_polygon.get_y())
                    # print('------')

                    # plt.plot(a_polygon.get_x(), a_polygon.get_y(), color='red')
                    # plt.plot(b_polygon.get_x(), b_polygon.get_y(), color='blue')
                    # plt.plot(split_level.get_x(), split_level.get_y(), color='green')
                    # plt.plot([i + 15 for i in a_polygon.get_x()], a_polygon.get_y(), color='red')
                    # plt.plot([i + 30 for i in b_polygon.get_x()], b_polygon.get_y(), color='blue')
                    # plt.show()

                    lay_x, lay_y = lay_main.curve

                    if len(lay_x) > 0:
                        d = [lay_x[0], lay_y[0]]

                    for i, j in zip(lay_x, lay_y):
                        c, d = d, [i, j]
                        # plt.plot(split_level.get_x(), split_level.get_y())
                        # plt.plot([c[0], d[0]], [c[1], d[1]])
                        if split_level.a.x is not None:
                            x1, y1 = intersection_segment_dot(
                                split_level.a, split_level.b, Point(c[0], c[1]), Point(d[0], d[1]))
                            if x1 is not None and y1 is not None:
                                lay_a.x.append(x1)
                                lay_a.y.append(y1)
                                lay_b.x.append(x1)
                                lay_b.y.append(y1)
                        if check_point_in_polygon(a_polygon.get_x(), a_polygon.get_y(), i, j):
                            lay_a.x.append(i)
                            lay_a.y.append(j)
                        if check_point_in_polygon(b_polygon.get_x(), b_polygon.get_y(), i, j):
                            lay_b.x.append(i)
                            lay_b.y.append(j)

                    # plt.fill(lay_a.x, lay_a.y, color='red')
                    # plt.fill(lay_b.x, lay_b.y, color='blue')
                    # plt.fill([i + 15 for i in a_polygon.get_x()], a_polygon.get_y(), color='red')
                    # plt.fill([i + 30 for i in b_polygon.get_x()], b_polygon.get_y(), color='blue')
                    # plt.show()

                    if len(lay_a.x) > 0:
                        lay_a.x.append(lay_a.x[0])
                        lay_a.y.append(lay_a.y[0])
                    if len(lay_b.x) > 0:
                        lay_b.x.append(lay_b.x[0])
                        lay_b.y.append(lay_b.y[0])

                split_shapes = split_shapes + [a_shape, b_shape]

                for lay in a_shape.layers:
                    lay.z += split.a_offset_z
                for lay in b_shape.layers:
                    lay.z += split.b_offset_z
        return split_shapes

    def sorted_layers(self):
        self.layers = sorted(self.layers, key=lambda lay: lay.z)
        return self.layers

    def get_prev_layer(self, z: int) -> Optional[Surface]:
        layers_bigger = [lay for lay in self.layers if lay.z > z]
        if layers_bigger:
            return sorted(layers_bigger, key=lambda i: i.z)[0]

    def delete_secondary_surface(self):
        self.layers = [lay for lay in self.layers if lay.primary is True]
        self.notify()

    def calc_intermediate_layers(self):
        self.delete_secondary_surface()
        this_layers = [lay for lay in self.layers if len(lay.curve[0]) > 0]

        if not this_layers:
            return

        dot_count = len(min(this_layers, key=lambda layer: len(layer.x)).x)

        for lay in this_layers:
            x, y = lay.curve
            lay.curve = simplify_line(x, y, dot_count)
            if len(lay.x) != dot_count:
                return

        new_layers = [this_layers[0]]
        for i in range(len(this_layers) - 1):
            top_z = this_layers[i].z
            bottom_z = this_layers[i + 1].z

            top_lay_x, top_lay_y = this_layers[i].curve
            bottom_lay_x, bottom_lay_y = this_layers[i + 1].curve

            for loc_z in range(top_z + 1, bottom_z):
                intermediate_lay = Surface(z=loc_z, size=self.size)
                intermediate_lay.primary = False

                for dot_n in range(dot_count):
                    a = [top_lay_x[dot_n], top_lay_y[dot_n], top_z]
                    b = [bottom_lay_x[dot_n], bottom_lay_y[dot_n], bottom_z]
                    x, y, _ = intersection_point_horizontal_plane(a, b, loc_z)
                    intermediate_lay.add_dot(x, y)

                new_layers.append(intermediate_lay)

            new_layers.append(this_layers[i + 1])

        self.layers = new_layers

    def swap_layer(self, index_a: int, index_b: int):
        range_layers = range(len(self.layers))
        if index_a in range_layers and index_b in range_layers:
            self.layers[index_a], self.layers[index_b] = self.layers[index_b], self.layers[index_a]
            self.layers[index_a].z, self.layers[index_b].z = self.layers[index_b].z, self.layers[index_a].z

    def add_layer(self, layer: Surface = None) -> Surface:
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index: int, layer: Surface = None) -> Optional[Surface]:
        if not layer:
            layer = Surface(size=self.size)

        if index <= 0:
            if [lay for lay in self.layers if lay.z <= 0]:
                return None
            layer.z = self.layers[0].z - 1 if self.layers else 0
            self.layers.insert(0, layer)

        elif 0 < index < len(self.layers):
            if abs(self.layers[index - 1].z - self.layers[index].z) < 2:
                return None
            layer.z = int((self.layers[index - 1].z + self.layers[index].z) / 2)
            self.layers.insert(index, layer)

        elif index >= len(self.layers):
            if [lay for lay in self.layers if lay.z >= Limits.MAXHEIGHT]:
                return None
            layer.z = self.layers[-1].z + 1 if self.layers else 0
            self.layers.append(layer)

        layer.prev_layer = self.get_prev_layer
        layer.next_layer = self.get_next_layer
        self.notify()
        return layer

    def pop_layer(self, index: int):
        if len(self.layers) < 2:
            return
        index = index if index in range(0, self.height + 1) else 0 if index <= 0 else len(self.layers) - 1
        self.layers.pop(index)
        self.notify()

    def set_layer_z(self, index, value):
        self.layers[index].z = value

    def load_from_json(self, path: str):
        self.load_from_dict(dict_from_json(path))
