import random

from Model.figure_3d import Figure3d
from Model.observer import Subject


class Map(Subject):
    def __init__(self):
        super().__init__()
        self.figure3d = list[Figure3d]()

    def add_layer(self, figure: Figure3d = None) -> Figure3d:
        if not figure:
            figure = Figure3d(name='layer {0}'.format(len(self.figure3d)))
        figure._observers = self._observers
        self.figure3d.append(figure)
        self.notify()
        return figure

    def random_layer_for_test(self):
        for i in range(random.randint(1, 1)):
            fig = Figure3d(name='layer {0}'.format(len(self.figure3d)))
            fig.random_layer_for_test()
            self.figure3d.append(fig)

    def delete_layer(self, index: int = None, name: str = None, figure: Figure3d = None):
        if index:
            self.figure3d.pop(index)

        if name:
            for i in range(len(self.figure3d)):
                if self.figure3d[i].name == name:
                    self.figure3d.pop(i)
                    break

        if figure:
            for i in range(len(self.figure3d)):
                if self.figure3d[i] == figure:
                    self.figure3d.pop(i)
                    break

        self.notify()

    def get_figures(self) -> list[Figure3d]:
        self.figure3d.sort(key=lambda i: i.priority, reverse=True)
        return self.figure3d

    def get_visible_figures(self):
        return list(filter(lambda i: i.visible is True, self.get_figures()))
