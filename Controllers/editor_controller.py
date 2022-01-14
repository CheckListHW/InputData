from PyQt5.QtWidgets import QFrame

from Controllers.qt_matplotlib_connector import MatplotlibConnectorEdit
from Model.figure_3d import Figure3d
from Model.surface_2d import SurfaceFigure2d
from Tools.filedialog import save_as_json


class EditorController2d:
    def __init__(self, parent: QFrame):
        self.figure3d = Figure3d()
        self.select_layer = 0
        self.connector = MatplotlibConnectorEdit(parent)

    def load_layers(self, path: str):
        self.figure3d = Figure3d(path)

    def edit_lay(self, index):
        if -len(self.figure3d.layers) < index < 0:
            print('-----------del-----------')
            self.figure3d.pop_layer(-index)
            lay = self.figure3d.get_layer(-index)
        elif 0 <= index < len(self.figure3d.layers):
            print('-----------add-----------')
            lay = self.figure3d.get_layer(index)
            self.figure3d.insert_layer(index, lay)
        elif index >= len(self.figure3d.layers):
            print('-----------add-----------')
            self.figure3d.add_layer()
            lay = self.figure3d.layers[-1]
        else:
            lay = self.figure3d.layers[0]
        self.connector.change_lay(lay)

    def change_lay(self, number: int):
        if 0 <= number < len(self.figure3d.layers):
            lay = self.figure3d.get_layer(number)
            self.connector.change_lay(lay)

    def save(self):
        fig_dict = self.figure3d.get_figure_as_dict()
        save_as_json(fig_dict)


