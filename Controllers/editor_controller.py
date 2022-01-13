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

    def change_lay(self, number: int):
        if number < 0:
            lay = SurfaceFigure2d()
            self.figure3d.insert_layer(0, lay)
        elif 0 <= number < len(self.figure3d.layers):
            lay = self.figure3d.get_layer(number)
        else:
            lay = SurfaceFigure2d()
            self.figure3d.add_layer(lay)
        self.connector.change_lay(lay)

    def save(self):
        fig_dict = self.figure3d.get_figure_as_dict()
        save_as_json(fig_dict)


