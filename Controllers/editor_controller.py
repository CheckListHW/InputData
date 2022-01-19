from PyQt5.QtWidgets import QFrame

from Controllers.qt_matplotlib_connector import MatplotlibConnectorEdit
from Model.figure_3d import Figure3d
from Tools.filedialog import save_as_json


class EditorController2d:
    def __init__(self, parent: QFrame):
        self.figure3d = Figure3d()
        self.select_layer = 0
        self.connector = MatplotlibConnectorEdit(parent, surf=self.figure3d.layers[0])

    def load_layers(self, path: str):
        self.figure3d = Figure3d(path)

    def edit_lay(self, index: int, edit_method: str = 'add', **kwargs):
        lay = None
        if edit_method == 'add':
            if 0 < index < len(self.figure3d.layers):
                if abs(self.figure3d.layers[index-1].z - self.figure3d.layers[index].z) > 2:
                    lay = self.figure3d.insert_layer(index)

        elif edit_method == 'del':
            index = abs(index)
            if 0 < index < len(self.figure3d.layers)-1:
                self.figure3d.pop_layer(index)
                lay = self.figure3d.layers[index]

        elif edit_method == 'move_up':
            if self.figure3d.swap_layer(index, index - 1):
                lay = self.figure3d.layers[index - 1]

        elif edit_method == 'move_down':
            if self.figure3d.swap_layer(index, index + 1):
                lay = self.figure3d.layers[index + 1]

        elif edit_method == 'change_height' and kwargs.get('height'):
            self.figure3d.set_layer_z(index, kwargs.get('height'))

        if lay is None:
            lay = self.figure3d.layers[0]

        self.connector.change_lay(lay)

    def change_lay(self, index: int):
        if 0 <= index < len(self.figure3d.layers):
            lay = self.figure3d.layers[index]
            self.connector.change_lay(lay)

    def save(self):
        fig_dict = self.figure3d.get_figure_as_dict()
        save_as_json(fig_dict)
