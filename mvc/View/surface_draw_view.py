import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QComboBox

from mvc.Controller.edit_plot_modes import ModeStatus
from mvc.Controller.qt_matplotlib_connector import EditorSurfaceController
from mvc.Model.shape import Shape
from mvc.View.surface_choose_view import ViewingLayersWindow
from data_resource.strings import Tips


class SurfaceEditWindow(QMainWindow):
    def __init__(self, single_surface=False, shape: Shape = None):
        super(SurfaceEditWindow, self).__init__()
        uic.loadUi(os.environ['project'] + '/ui/surface_edit.ui', self)

        self.surface_editor = EditorSurfaceController(self.draw_polygon_frame, shape=shape)
        self.view_layers_window = ViewingLayersWindow(self.surface_editor)

        self.button_connect(single_surface)

    def button_connect(self, single_surface=True):
        if single_surface:
            self.viewLayersButton.hide()

        self.split_frame.hide()
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addSplitButton.clicked.connect(lambda: self.change_mode(ModeStatus.AddSplit))
        self.splitNumberComboBox.activated.connect(self.change_current_split)

        self.simplifyButton.clicked.connect(lambda: self.surface_editor.simplify_line())
        self.halve.clicked.connect(lambda: self.surface_editor.halve_dot())

        self.save.clicked.connect(lambda: self.surface_editor.save())
        self.open.clicked.connect(self.load_from_file)

        self.updateButton.clicked.connect(lambda: self.change_mode(ModeStatus.Empty))

        self.viewLayersButton.clicked.connect(self.view_layers_window.show)

        self.add_tips()

    def add_tips(self):
        self.simplifyButton.setToolTip(Tips.SIMPLIFYBUTTON)

    def change_current_split(self):
        x: QComboBox = self.splitNumberComboBox
        self.surface_editor.plot.surface.current_split = int(x.currentText()) - 1

    def load_from_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, '', os.getcwd(), 'Json Files (*.json)')
        if filename:
            self.surface_editor.set_shape(path=filename)

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.surface_editor.set_mode(mode)
        self.surface_editor.update_plot()
