from Model.size import Size
from Model.shape import Shape
from Model.observer import Subject
from Tools.filedialog import dict_from_json


class Map(Subject):
    __slots__ = 'size', 'shapes'

    def __init__(self):
        super().__init__()
        self.size = Size()
        self.shapes: [Shape] = list()

    def add_layer(self, figure: Shape = None) -> Shape:
        if not figure:
            figure = Shape(size=self.size)
        if not figure.size:
            figure.size = self.size
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
        return sorted(filter(lambda i: i.visible is True, self.get_shapes()), key=lambda i: i.priority).__reversed__()

    def load_from_dict(self, dictionary: dict):
        self.shapes = list()
        for lay in dictionary:
            fig = Shape(size=self.size)
            fig.load_from_dict(dictionary[lay])
            self.add_layer(fig)

        self.notify()

    def load_from_json(self, path: str):
        self.load_from_dict(dict_from_json(path))

    @property
    def height(self) -> int:
        return max(self.shapes, key=lambda i: i.height).height
