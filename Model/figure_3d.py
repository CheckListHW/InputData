from Model.surface2d import SurfaceFigure2d


class Figure3d:
    def __init__(self, height=1):
        if height < 1:
            return
        self.layers = [SurfaceFigure2d() for _ in range(height)]
        self.up = self.layers[0]
        self.bottom = self.layers[-1]

    def add_layers(self, count: int):
        self.layers += [SurfaceFigure2d() for _ in range(count)]

    def size_x(self) -> int:
        return max(self.layers, key=lambda i: i.max_x()).max_x()

    def size_y(self) -> int:
        return max(self.layers, key=lambda i: i.max_y()).max_y()

    def size_fig(self) -> [int]:
        return [self.size_x(), self.size_y(), len(self.layers)]

    def get_layers_by_priority(self):
        return self.layers.sort(key=lambda i: i.priority())
