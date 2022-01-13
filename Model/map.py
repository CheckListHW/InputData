from Model.figure_3d import Figure3d
from Model.observer import Subject


class Map(Subject):
    def __init__(self):
        super().__init__()
        self.figure3d = list[Figure3d]()

    def add_layer(self, figure: Figure3d = None) -> Figure3d:
        if not figure:
            figure = Figure3d()
        figure._observers = self._observers
        self.figure3d.append(figure)
        self.notify()
        return figure

    def delete_layer(self, index: int = None, name: str = None, figure: Figure3d = None):
        if index:
            self.figure3d.pop(index)
            return

        if name:
            for i in range(len(self.figure3d)):
                if self.figure3d[i].name == name:
                    self.figure3d.pop(i)
                    return

        if figure:
            for i in range(len(self.figure3d)):
                if self.figure3d[i] == figure:
                    self.figure3d.pop(i)
                    return

        self.notify()

    def get_figures(self) -> list[Figure3d]:
        self.figure3d.sort(key=lambda i: i.priority, reverse=True)
        return self.figure3d
