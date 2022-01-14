from Model.observer import Subject
from Model.surface_2d import SurfaceFigure2d
from Tools.dict_from_json import dict_from_json

# z - высота слоя
class Figure3d(Subject):
    def __init__(self, path: str = None) -> None:
        super().__init__()
        self.name: str = 'layer 1'
        self.color: str = '0,0,0'
        self.priority: int = 100
        self.z = 0
        self.layers = list[SurfaceFigure2d]()

        if path:
            self.load_from_json(path)

    def load_from_json(self, path: str):
        layers = dict_from_json(path)
        for lay in layers:
            sf2d = SurfaceFigure2d(lay=layers[lay])
            self.add_layer(sf2d)

    def add_layer(self, layer: SurfaceFigure2d):
        self.layers.append(layer)
        self.notify()

    def insert_layer(self, index: int, layer: SurfaceFigure2d):
        self.layers.insert(index, layer)
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
        return [self.size_x(), self.size_y(), len(self.layers)]

    def get_layers_by_priority(self) -> [SurfaceFigure2d]:
        return self.layers.sort(key=lambda i: i.priority())

    def get_layer(self, number: int) -> SurfaceFigure2d:
        if 0 <= number < len(self.layers):
            return self.layers[number]

    def set_priority(self, value: int):
        if value in range(101):
            self.priority = value

    def get_figure_as_dict(self) -> dict:
        dict = {
            'name': self.name,
            'color': self.color,
            'z': self.z,
            'priority': self.priority
        }
        for i in range(len(self.layers)):
            dict[str(i)] = self.layers[i].get_surface_as_dict()
        return dict

    def set_name(self, text: str) -> None:
        self.name = text
        self.notify()

    def set_property(self, settings: dict):
        for name_property in settings:
            if name_property == 'name':
                self.set_name(settings[name_property])
            elif name_property == 'priority':
                self.set_priority(settings[name_property])

        self.notify()

