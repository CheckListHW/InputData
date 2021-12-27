import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from Controllers.edit_plot_modes import ModeStatus
from Controllers.editor_controller import EditorController
from Tools.dict_from_json import dict_from_json
from View.select_surface_window import ViewingLayersWindow


class EditWindow(QMainWindow):
    def __init__(self):
        super(EditWindow, self).__init__()
        uic.loadUi('ui/edit_surface.ui', self)

        self.editor2d = EditorController(self.draw_polygon_frame)
        self.view_layers_window = ViewingLayersWindow(click_handler=self.editor2d.change_lay)

        self.button_connect()

    def button_connect(self):
        self.update.clicked.connect(self.editor2d.connector.update_plot)
        self.halve.clicked.connect(self.editor2d.connector.halve_dot)
        self.save.clicked.connect(self.save_figure)
        self.open.clicked.connect(self.open_file)
        self.view_layers.clicked.connect(self.show_layers)

        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))

    def show_layers(self):
        self.view_layers_window.set_surfaces(self.editor2d.figure3d.get_figure_as_dict())
        self.view_layers_window.show()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, '', os.getcwd(), 'Json Files (*.json)')
        self.editor2d.load_layers(dict_from_json(filename))

    def save_figure(self):
        self.editor2d.save()

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.editor2d.connector.set_mode(mode)
