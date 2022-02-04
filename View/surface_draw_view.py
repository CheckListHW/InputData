import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from Controllers.edit_plot_modes import ModeStatus
from Controllers.qt_matplotlib_connector import EditorSurfaceController
from View.surface_choose_view import ViewingLayersWindow
from resource import string_resource as str_res


class SurfaceEditWindow(QMainWindow):
    def __init__(self, single_surface=False):
        super(SurfaceEditWindow, self).__init__()
        uic.loadUi(os.environ['project'] + '/ui/edit_surface.ui', self)

        self.surface_editor = EditorSurfaceController(self.draw_polygon_frame)
        self.view_layers_window = ViewingLayersWindow(self.surface_editor)

        self.button_connect(single_surface)

    def button_connect(self, single_surface=True):
        if single_surface:
            self.viewLayersButton.hide()

        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))
        self.updateButton.clicked.connect(lambda: self.surface_editor.update_plot())

        self.simplifyButton.clicked.connect(lambda: self.surface_editor.simplify_line())
        self.halve.clicked.connect(lambda: self.surface_editor.halve_dot())
        self.viewLayersButton.clicked.connect(self.show_layers)

        self.save.clicked.connect(lambda: self.surface_editor.save())
        self.open.clicked.connect(self.open_file)

        self.add_tips()

    def add_tips(self):
        self.simplifyButton.setToolTip(str_res.tool_tip_text_simplifyButton)

    def show_layers(self):
        self.view_layers_window.set_surfaces(self.surface_editor.shape.get_figure_as_dict)
        self.view_layers_window.show()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, '', os.getcwd(), 'Json Files (*.json)')
        if filename:
            self.surface_editor.set_shape(path=filename)

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.surface_editor.set_mode(mode)
