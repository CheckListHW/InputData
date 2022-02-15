import math
import random
from typing import List, Optional, Counter

from Model.observer import Subject
from Model.size import Size
from Model.surface import Surface
from Tools.filedialog import dict_from_json

# alpha - прозрачнгость от 0 до 1
from Tools.intersection_point_horizontal_plane import intersection_point_horizontal_plane
from Tools.simplify_line import simplify_line
from Tools.counter import Counter


class ShapeProperty(Subject):
    __slots__ = 'size', 'visible', '__alpha', '__priority', '__color', '__name', '__layers'

    def __init__(self, size: Size):
        super(ShapeProperty, self).__init__()
        self.size = size
        self.visible, self.__alpha, self.__priority = True, 0.9, 100
        self.__color: (int, int, int) = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.__name: str = 'layer 1'
        self.__layers: List[Surface] = list()

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        if 0 <= value <= 1:
            self.__alpha = value

    @property
    def color(self) -> (int, int, int):
        return self.__color

    @color.setter
    def color(self, value: (int, int, int)):
        r, g, b = value
        if int(r) in range(256) and int(g) in range(256) and int(b) in range(256):
            self.__color = (r, g, b)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def height(self):
        return max(self.layers, key=lambda i: i.z).z

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value: int):
        value = int(value)
        if value in range(101):
            self.__priority = value

    @property
    def layers(self) -> [Surface]:
        return self.__layers

    @layers.setter
    def layers(self, value: [Surface]):
        self.__layers = value


class Shape(ShapeProperty):
    __slots__ = 'size'

    def __init__(self, size: Size, path: str = None) -> None:
        super().__init__(size)
        self.size = size
        self.add_layer(Surface(size=self.size, z=0))
        if path:
            self.load_from_json(path)

    def get_next_layer(self, z: int) -> Optional[Surface]:
        layers_less = [lay for lay in self.layers if lay.z < z]
        if layers_less:
            return sorted(layers_less, key=lambda i: i.z)[-1]

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
            if [lay for lay in self.layers if lay.z >= self.height]:
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

    def get_figure_as_dict(self) -> dict:
        dictionary = {
            'name': self.name,
            'color': self.color,
            'priority': self.priority,
            'height': self.height,
            'alpha': self.alpha,
            'layers': {},
        }

        for i in range(len(self.layers)):
            dictionary['layers'][str(i)] = self.layers[i].get_surface_as_dict()

        return dictionary

    def set_layer_z(self, index, value):
        try:
            self.layers[index].z = value
        except IndexError:
            print('set_layer_z', IndexError)
        print(self.layers[index].z)

    def set_property(self, settings: dict):
        for name_property in settings:
            if name_property == 'name':
                self.name = settings[name_property]
            elif name_property == 'priority':
                self.priority = settings[name_property]
            elif name_property == 'color':
                self.color = settings[name_property]
            elif name_property == 'alpha':
                self.alpha = settings['alpha']

        self.notify()

    def load_from_json(self, path: str):
        self.load_from_dict(dict_from_json(path))

    def load_from_dict(self, dictionary: dict):
        self.layers = list()
        for lay in dictionary.get('layers').values():
            self.layers.append(Surface(size=self.size, lay=lay))
        self.set_property(dictionary)
