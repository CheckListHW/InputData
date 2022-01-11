from Model.surface_2d import SurfaceFigure2d
from Tools.dict_from_json import dict_from_json


class Figure3d:
    def __init__(self, path: str = None) -> None:
        self.priority = 100
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

    def insert_layer(self, index: int, layer: SurfaceFigure2d):
        self.layers.insert(index, layer)

    def size_x(self) -> int:
        return max(self.layers, key=lambda i: i.max_x()).max_x()

    def size_y(self) -> int:
        return max(self.layers, key=lambda i: i.max_y()).max_y()

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
        a = {}
        for i in range(len(self.layers)):
            a[str(i)] = self.layers[i].get_surface_as_dict()
        return a
