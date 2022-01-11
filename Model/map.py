from Model.figure_3d import Figure3d


class Map:
    def __init__(self):
        self.__figure3d = list[Figure3d]()

    def add_figure(self):
        figure = Figure3d()
        self.__figure3d.append(figure)

    def add_layer(self):
        self.add_figure()

    def delete_layer(self, index: int = None, name: str = None, figure: Figure3d = None):
        if index:
            self.__figure3d.pop(index)
            return

        if name:
            for i in range(len(self.__figure3d)):
                if self.__figure3d[i].name == name:
                    self.__figure3d.pop(i)
                    return

        if figure:
            for i in range(len(self.__figure3d)):
                if self.__figure3d[i] == figure:
                    self.__figure3d.pop(i)
                    return

    def get_figures(self):
        self.__figure3d.sort(key=lambda i: i.priority(), reverse=True)
        return self.__figure3d.copy()
