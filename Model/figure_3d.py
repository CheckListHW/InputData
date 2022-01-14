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

        self.top_lay = SurfaceFigure2d(z=self.height)
        self.top_lay.random_layer_for_test()
        self.bottom_lay = SurfaceFigure2d(z=0)
        self.bottom_lay.random_layer_for_test()

        self.layers = list[SurfaceFigure2d]()

        if path:
            self.load_from_json(path)

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

    def add_layer(self, layer: SurfaceFigure2d = None):
        if layer:
            self.layers.append(layer)
        else:
            self.layers.append(SurfaceFigure2d())
        self.notify()

    def insert_layer(self, index: int, layer: SurfaceFigure2d):
        self.layers.insert(index, layer)
        self.notify()

    def pop_layer(self, index: int):
        if len(self.layers) > 1:
            self.layers.pop(index)
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
        return [self.size_x(), self.size_y(), self.height+1]

    def get_layers(self) -> [SurfaceFigure2d]:
        return [self.top_lay] + self.layers + [self.bottom_lay]

    def get_layers_by_priority(self) -> [SurfaceFigure2d]:
        return sorted(self.get_layers(), key=lambda i: i.z)

    def get_layer(self, index: int) -> SurfaceFigure2d:
        if index in range(len(self.layers)):
            return self.get_layers()[index]

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
            'top': self.top_lay.get_surface_as_dict(),
            'bottom': self.bottom_lay.get_surface_as_dict(),
            'layers': {},
        }

        for i in range(len(self.layers)):
            dict['layers'][str(i)] = self.layers[i].get_surface_as_dict()
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
