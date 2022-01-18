from PyQt5.QtWidgets import QFrame

from Controllers.qt_matplotlib_connector import MatplotlibConnectorEdit
from Model.figure_3d import Figure3d
from Model.surface_2d import SurfaceFigure2d
from Tools.filedialog import save_as_json


class EditorController2d:
    def __init__(self, parent: QFrame):
        self.figure3d = Figure3d()
        self.select_layer = 0
        surf = self.figure3d.get_top_lay()
        print(surf.x, surf.y)
        self.connector = MatplotlibConnectorEdit(parent, surf=surf)

    def load_layers(self, path: str):
        self.figure3d = Figure3d(path)

    def edit_lay(self, index: int, edit_method: str = 'add', **kwargs):
        print(edit_method, index)
        lay = None
        if edit_method == 'add' and index >= 0:
            lay = self.figure3d.insert_layer(index)

        elif edit_method == 'del' or index <= 0:
            index = abs(index)
            self.figure3d.pop_layer(index)
            lay = self.figure3d.get_layer(index)

        elif edit_method == 'move_up':
            if self.figure3d.swap_layer(index, index - 1):
                lay = self.figure3d.layers[index-1]

        elif edit_method == 'move_down':
            if self.figure3d.swap_layer(index, index + 1):
                lay = self.figure3d.layers[index + 1]

        elif edit_method == 'change_height' and kwargs.get('height'):
            return self.figure3d.change_height_on_layer(index, kwargs.get('height'))

        if lay is None:
            lay = self.figure3d.get_layers()[0]

        self.connector.change_lay(lay)

    def change_lay(self, number: int):
        if 0 <= number < len(self.figure3d.layers):
            lay = self.figure3d.get_layer(number)
            self.connector.change_lay(lay)

    def save(self):
        fig_dict = self.figure3d.get_figure_as_dict()
        save_as_json(fig_dict)
