import math
import random
from typing import List

from Model.observer import Subject
from Model.surface_2d import SurfaceFigure2d
from Tools.dict_from_json import dict_from_json


# alpha - прозрачнгость от 0 до 1
from Tools.intersection_point_horizontal_plane import intersection_point_horizontal_plane
from Tools.simplify_line import simplify_line


class Figure3d(Subject):
    def __init__(self, path: str = None, name: str = 'layer 1') -> None:
        super().__init__()
        self.visible = True
        self.name: str = name
        self.alpha = 0.9
        self.__color: str = '{0},{1},{2}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.priority: int = 100
        self.height = 15

        self.layers: List[SurfaceFigure2d] = list()
        self.add_layer(SurfaceFigure2d(z=0)).square_layer_test(1)
        self.add_layer(SurfaceFigure2d(z=self.height)).square_layer_test(4)

        if path:
            self.load_from_json(path)

    def calc_intermediate_layers(self):
        for i in reversed(range(len(self.layers))):
            if len(self.layers[i].x) < 1:
                self.pop_layer(i)

        dot_count = float('inf')

        for lay in self.layers:
            print(len(lay.x), dot_count)
            if len(lay.x) < dot_count:
                dot_count = len(lay.x)

        print('dot_count', dot_count)
        for lay in self.layers:
            print('before simplify_line', len(lay.x))

        for lay in self.layers:
            lay.x, lay.y = simplify_line(lay.x, lay.y, dot_count)

        for lay in self.layers:
            print('post simplify_line', len(lay.x))

        new_layers = [self.layers[0]]
        for i in range(len(self.layers)-1):
            top_z = self.layers[i].z
            bottom_z = self.layers[i+1].z

            top_lay = self.layers[i]
            bottom_lay = self.layers[i+1]

            for loc_z in range(top_z+1, bottom_z):
                intermediate_lay = SurfaceFigure2d(z=loc_z)

                for dot_n in range(len(top_lay.x)):
                    print(len(top_lay.x), len(bottom_lay.x))
                    a = [top_lay.x[dot_n], top_lay.y[dot_n], top_z]
                    b = [bottom_lay.x[dot_n], bottom_lay.y[dot_n], bottom_z]
                    x, y, _ = intersection_point_horizontal_plane(a, b, loc_z)
                    intermediate_lay.add_dot(x, y)

                new_layers.append(intermediate_lay)

            new_layers.append(self.layers[i+1])

        self.layers = new_layers


    def swap_layer(self, index_a: int, index_b: int):
        range_layers = range(len(self.layers))
        if index_a in range_layers and index_b in range_layers:
            self.layers[index_a], self.layers[index_b] = self.layers[index_b], self.layers[index_a]
            self.layers[index_a].z, self.layers[index_b].z = self.layers[index_b].z, self.layers[index_a].z

    def add_layer(self, layer: SurfaceFigure2d = None) -> SurfaceFigure2d:
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index: int, layer: SurfaceFigure2d = None) -> SurfaceFigure2d:
        if not layer:
            if index - 1 >= 0 and index < len(self.layers):
                z = int((self.layers[index - 1].z + self.layers[index].z) / 2)
                layer = SurfaceFigure2d(z=z)
            else:
                layer = SurfaceFigure2d()
        if index <= 0:
            self.layers.insert(0, layer)
        elif 0 < index < len(self.layers):
            self.layers.insert(index, layer)
        else:
            self.layers.append(layer)
        self.notify()
        return layer

    def pop_layer(self, index: int):
        if len(self.layers) <= 2:
            return
        self.layers.pop(index)
        self.notify()

    def size_x(self) -> int:
        return max(self.layers, key=lambda i: i.max_x()).max_x()

    def size_y(self) -> int:
        return max(self.layers, key=lambda i: i.max_y()).max_y()

    def get_figure_as_dict(self) -> dict:
        dictionary = {
            'name': self.name,
            'color': self.__color,
            'priority': self.priority,
            'height': self.height,
            'layers': {},
        }

        for i in range(len(self.layers)):
            dictionary['layers'][str(i)] = self.layers[i].get_surface_as_dict()
        return dictionary

    def get_color(self) -> (int, int, int):
        colors = self.__color.replace(' ', '').split(',')
        try:
            return int(colors[0]), int(colors[1]), int(colors[2])
        except:
            return 0, 0, 0

    def set_color(self, value: str):
        colors = value.replace(' ', '').split(',')
        for color in colors:
            if not int(color) in range(256):
                return
        self.__color = value

    def set_layer_z(self, index, value):
        range_valid = range(len(self.layers))
        if index - 1 in range_valid and index + 1 in range_valid:
            if value in range(self.layers[index - 1].z, self.layers[index + 1].z):
                self.layers[index].z = value
            elif value > self.layers[index + 1].z:
                self.layers[index].z = self.layers[index + 1].z-1
            elif value < self.layers[index - 1].z:
                self.layers[index].z = self.layers[index - 1].z+1

    def set_priority(self, value: int):
        if value in range(101):
            self.priority = value

    def set_alpha(self, value: float):
        if 0 < value < 1:
            self.alpha = value

    def set_name(self, text: str) -> None:
        self.name = text
        self.notify()

    def set_height(self, value: int):
        if value in range(501):
            self.height = value
            self.layers[-1].z = value

    def set_property(self, settings: dict):
        for name_property in settings:
            if name_property == 'name':
                self.set_name(settings[name_property])
            elif name_property == 'priority':
                self.set_priority(settings[name_property])
            elif name_property == 'color':
                self.set_color(settings[name_property])
            elif name_property == 'priority':
                self.set_alpha(settings['alpha'])
            elif name_property == 'height':
                self.set_height(settings['height'])

        self.notify()

    def load_from_json(self, path: str):
        figure = dict_from_json(path)
        self.layers = list()
        for lay in figure.get('layers'):
            sf2d = SurfaceFigure2d(lay=figure.get('layers')[str(lay)])
            self.add_layer(sf2d)

    # def get_sorted_layers_by_z(self) -> [SurfaceFigure2d]:
    #     return sorted(self.layers, key=lambda i: i.z)
