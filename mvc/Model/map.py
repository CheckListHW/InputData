import math

import numpy as np

from utils.json_in_out import JsonInOut
from utils.observer import Subject
from mvc.Model.roof_profile import RoofProfile, RoofPoint
from mvc.Model.shape import Shape
from mvc.Model.size import Size
from utils.filedialog import dict_from_json
from utils.geometry.point_in_polygon import check_polygon_in_polygon
from utils.transform_data_to_export import dict_update, transform_data


def pop_from_dict(dict_value: dict, name: str):
    dict_value[name] = False
    dict_value.pop(name)


def pop_from_dict_many(dict_value: dict, names: [str]):
    for name in names:
        pop_from_dict(dict_value, name)


class Map(Subject, JsonInOut):
    __slots__ = 'size', 'shapes', 'roof_profile', 'data', 'draw_speed'

    def __init__(self):
        super().__init__()
        self.draw_speed = 'Fast'
        self.data = {}
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
        for shape in [i for i in self.shapes if i.visible]:
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
        pop_from_dict(map_dict, 'data')
        for d in map_dict:
            if d == 'shapes':
                for shape in map_dict[d]:
                    pop_from_dict_many(shape, ['size', 'split_shapes'])

                    for name in shape.get('parts_property'):
                        pop_names = ['size', 'layers', 'splits', 'split_shapes', 'parts_property']
                        pop_from_dict_many(shape['parts_property'][name], pop_names)
                    pop_layer_number = []

                    for lay, i in zip(shape['layers'], range(len(shape['layers']))):
                        if lay.get('primary') is True:
                            pop_names = ['size', 'pre_x', 'pre_y', 'start_x', 'start_y', 'splits', 'current_split']
                            pop_from_dict_many(lay, pop_names)
                        elif lay.get('primary') is False:
                            pop_layer_number.append(i)
                    for i in pop_layer_number.__reversed__():
                        shape['layers'].pop(i)
        return map_dict

    def load_from_json(self, path: str):
        map_dict = dict_from_json(path)
        self.load_from_dict(map_dict)

    def update_size(self):
        x = [a for b in [surf.x for shape in self.shapes for surf in shape.layers] for a in b] + \
            [self.size.x_constraints.start, self.size.x_constraints.end]
        y = [a for b in [surf.y for shape in self.shapes for surf in shape.layers] for a in b] + \
            [self.size.y_constraints.start, self.size.y_constraints.end]

        self.size.x_constraints.start, self.size.x_constraints.end = min(x), max(x)
        self.size.y_constraints.start, self.size.y_constraints.end = min(y), max(y)
        self.size.z_constraints.end = max([i.height for i in self.shapes] + [self.size.z_constraints.end])

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


class ExportMap:
    def __init__(self, map: Map):
        self.map = map
        self.repeat, self.map.data = {}, {}

    def __call__(self, *args, **kwargs) -> dict:
        for shape in self.map.shapes:
            shape.calc_intermediate_layers()
        return self.export()

    def export(self) -> dict:
        self.__init__(self.map)
        for shape in self.map.get_visible_shapes():
            data = self.calc_polygon_in_draw(shape)
            self.map.data[f'{shape.name}|{shape.sub_name}'] = dict_update(self.map.data.get(shape.name),
                                                                          transform_data(data))

        return self.map.data

    def calc_polygon_in_draw(self, fig: Shape) -> []:
        x_size, y_size, z_size = self.map.size.x, self.map.size.y, max(fig.height, self.map.height_with_offset) + 1
        roof_profile_offset = self.map.roof_profile.get_x_y_offset(base=max(x_size, y_size))
        data = np.zeros([x_size, y_size, z_size], dtype=bool)

        lay_size = fig.size.x * fig.size.y
        for lay in fig.layers:
            (x, y), lay_z = lay.scalable_curve, lay.z
            for x1 in range(fig.size.x):
                x1_c = math.ceil(x1)
                xx, rpo_x = [x1_c, x1_c + 1, x1_c, x1_c + 1], roof_profile_offset[x1]
                for y1 in range(fig.size.y):
                    y1_c = math.ceil(y1)
                    z1_offset, yy = int(lay_z + rpo_x[y1]), [y1_c, y1_c, y1_c + 1, y1_c + 1]
                    if check_polygon_in_polygon(x, y, xx, yy):
                        rep_name = lay_size * z1_offset + x1 * fig.size.y + y1
                        if self.repeat.get(rep_name) is None:
                            self.repeat[rep_name] = data[x1, y1, z1_offset] = True

        return data
