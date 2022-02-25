import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from Controllers.edit_plot_modes import ModeStatus
from Controllers.qt_matplotlib_connector import EditorRoofProfileController
from Model.shape import Shape
from View.surface_choose_view import ViewingLayersWindow


class RoofProfileEditWindow(QMainWindow):
    def __init__(self, shape: Shape):
        super(RoofProfileEditWindow, self).__init__()
        uic.loadUi(os.environ['project'] + '/ui/roof_profile_edit.ui', self)

        self.surface_editor = EditorRoofProfileController(self.draw_polygon_frame)
        self.view_layers_window = ViewingLayersWindow(self.surface_editor)

        self.button_connect()

    def button_connect(self):
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.chooseDot.clicked.connect(lambda: self.change_mode(ModeStatus.ChooseDot))

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.surface_editor.set_mode(mode)
        self.surface_editor.update_plot()
