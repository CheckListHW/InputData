import random

from Model.observer import Subject
from Model.surface_2d import SurfaceFigure2d
from Tools.dict_from_json import dict_from_json


# alpha - прозрачнгость от 0 до 1
class Figure3d(Subject):
    def __init__(self, path: str = None, name: str = 'layer 1') -> None:
        super().__init__()
        self.visible = True
        self.name: str = name
        self.alpha = 0.9
        self.color: str = '{0},{1},{2}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.priority: int = 100
        self.height = 15

        top_lay = SurfaceFigure2d(z=0)
        print('top_lay.z={0}'.format(top_lay.z))

        top_lay.square_layer()
        bottom_lay = SurfaceFigure2d(z=self.height)
        bottom_lay.square_layer()

        self.layers = list[SurfaceFigure2d]()
        self.add_layer(top_lay)
        self.add_layer(bottom_lay)

        if path:
            self.load_from_json(path)

    def get_top_lay(self):
        for lay in self.get_layers():
            print('z={0}'.format(lay.z))
        top_lay = list(filter(lambda x: x.z == 0, self.get_layers()))
        if len(top_lay) > 0:
            return top_lay[0]

    def swap_layer(self, index_a, index_b) -> bool:
        range_layers = range(len(self.layers))
        if index_a in range_layers and index_b in range_layers:
            self.layers[index_a], self.layers[index_b] = self.layers[index_b], self.layers[index_a]
            return True
        return False

    def change_height_on_layer(self, layer_index: int, new_z: int) -> int:
        if layer_index in range(1, len(self.layers) - 1):
            self.get_layers_by_z()[layer_index].z = new_z
            return new_z

    def random_layer_for_test(self):
        count = random.randint(3, 5)
        startz = 0
        for i in range(count):
            startz += int(self.height / count)
            surf = SurfaceFigure2d(z=startz)
            surf.random_layer_for_test()
            self.layers.append(surf)

    def get_color(self) -> (int, int, int):
        colors = self.color.replace(' ', '').split(',')
        try:
            return int(colors[0]), int(colors[1]), int(colors[2])
        except:
            return 0, 0, 0

    def load_from_json(self, path: str):
        layers = dict_from_json(path)
        for lay in layers:
            sf2d = SurfaceFigure2d(lay=layers[lay])
            self.add_layer(sf2d)

    def add_layer(self, layer: SurfaceFigure2d = None) -> SurfaceFigure2d:
        return self.insert_layer(len(self.layers), layer)

    def insert_layer(self, index: int, layer: SurfaceFigure2d = None) -> SurfaceFigure2d:
        if not layer:
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
        if len(self.get_layers()) <= 2:
            return

        if index <= 0:
            self.layers.pop(0)
        elif 0 < index < len(self.layers):
            self.layers.pop(index)
        else:
            self.layers.pop()

        self.notify()

    def size_x(self) -> int:
        if self.layers:
            return max(self.layers, key=lambda i: i.max_x()).max_x()
        else:
            return 0

    def size_y(self) -> int:
        if self.layers:
            return max(self.layers, key=lambda i: i.max_y()).max_y()
        else:
            return 0

    def size_fig(self) -> [int]:
        return [self.size_x(), self.size_y(), self.height + 1]

    def get_layers(self) -> [SurfaceFigure2d]:
        return self.layers

    def get_layers_by_z(self) -> [SurfaceFigure2d]:
        for lay in self.get_layers():
            print(lay.z)
        return sorted(self.get_layers(), key=lambda i: i.z)

    def get_layer(self, index: int) -> SurfaceFigure2d:
        if index in range(len(self.layers)):
            return self.get_layers()[index]
        else:
            return self.get_layers()[0]

    def set_priority(self, value: int):
        if value in range(101):
            self.priority = value

    def set_color(self, value: str):
        colors = value.replace(' ', '').split(',')
        for color in colors:
            if not int(color) in range(256):
                return
        self.color = value

    def set_alpha(self, value: float):
        if 0 < value < 1:
            self.alpha = value

    def get_figure_as_dict(self) -> dict:
        dict = {
            'name': self.name,
            'color': self.color,
            'priority': self.priority,
            'height': self.height,
            'layers': {},
        }

        layers = self.get_layers()
        for i in range(len(layers)):
            dict['layers'][str(i)] = layers[i].get_surface_as_dict()
        return dict

    def set_name(self, text: str) -> None:
        self.name = text
        self.notify()

    def set_height(self, value: int):
        if value in range(501):
            self.height = value

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
