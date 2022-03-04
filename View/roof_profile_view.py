import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from Controllers.edit_plot_modes import ModeStatus
from Controllers.qt_matplotlib_connector import EditorRoofProfileController
from Model.map import Map
from View.surface_choose_view import ViewingLayersWindow


class RoofProfileEditWindow(QMainWindow):
    def __init__(self, map: Map):
        super(RoofProfileEditWindow, self).__init__()
        uic.loadUi(os.environ['project'] + '/ui/roof_profile_edit.ui', self)

        self.map = map
        self.surface_editor = EditorRoofProfileController(map=self.map, parent=self.draw_polygon_frame)
        self.view_layers_window = ViewingLayersWindow(self.surface_editor)

        self.button_connect()
        self.surface_editor.update_plot()

    def button_connect(self):
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.chooseDot.clicked.connect(lambda: self.change_mode(ModeStatus.ChooseDot))
        self.interpolateMethodComboBox.currentTextChanged.connect(self.method_change)
        self.threeDButton.clicked.connect(self.surface_editor.plot.show3d)
        self.heightSpinBox.editingFinished.connect(self.change_height)

    def method_change(self):
        self.map.roof_profile.interpolate_method = self.interpolateMethodComboBox.currentText()
        self.surface_editor.update_plot()

    def change_height(self):
        if self.surface_editor.plot.nearst_dot_index is not None:
            self.map.roof_profile.points[self.surface_editor.plot.nearst_dot_index].z \
                = self.heightSpinBox.value()
        self.surface_editor.update_plot()

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.surface_editor.set_mode(mode)
        self.surface_editor.update_plot()
