from os import environ
from typing import Callable, List

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QFrame

from Controllers.qt_matplotlib_connector import EditorSurfaceControllerTight, EditorSurfaceController
from Model.surface import Surface
from View.single_surface_view import SingleLayWidget


class ViewingLayersWindow(QMainWindow):
    i = 0

    def __init__(self, surface_editor: EditorSurfaceController):
        super(ViewingLayersWindow, self).__init__()
        uic.loadUi(environ['project'] + '/ui/surface_choose.ui', self)
        # добавляется для того чтобы сборщик мусора не удалял объекты
        self.aaa = []
        self.surface_editor = surface_editor

        self.get_surfaces, self.frames, self.size = None, list(), 200
        self.handlers_connect()

    def handlers_connect(self):
        self.accept.clicked.connect(self.change_size)
        self.addSubLayersButton.clicked.connect(self.calc_intermediate_layers)
        self.removeSubLayersButton.clicked.connect(self.delete_secondary_surface)

    def calc_intermediate_layers(self):
        self.surface_editor.shape.calc_intermediate_layers()
        self.show()

    def delete_secondary_surface(self):
        self.surface_editor.shape.delete_secondary_surface()
        self.show()

    def add_frame_to_layout(self, index: int) -> QFrame:
        z = self.surface_editor.shape.layers[index].z
        frame = SingleLayWidget(index, z, edit_lay_handler=self.edit_layer)

        self.layout_plots.addWidget(frame, index, 0)

        frame.setMinimumSize(self.size, self.size)
        frame.setMaximumSize(self.size, self.size)
        self.frames.append(frame)
        self.aaa.append(frame)
        return frame.viewFrame

    def edit_layer(self, index: int, edit_method: str = 'add', **kwargs):
        self.surface_editor.edit_lay(index, edit_method, **kwargs)
        self.show()

    def change_layer(self, index):
        if self.surface_editor.change_lay(index):
            self.show()

    # тут все очень важное меняй с умом!!!
    def show(self) -> None:
        for i in reversed(range(self.layout_plots.count())):
            self.layout_plots.itemAt(i).widget().setParent(None)

        for frame in self.frames:
            for children in frame.children():
                children.setParent(None)

        self.frames = list()

        surfaces: List[Surface] = self.surface_editor.shape.sorted_layers()

        for i in range(len(surfaces)):
            frame = self.add_frame_to_layout(i)
            EditorSurfaceControllerTight(frame, tight=True, surf=surfaces[i],
                                         preview_click_handler=lambda j=i: self.change_layer(j))

        self.resize(self.size + 20, self.height())

        super(ViewingLayersWindow, self).show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.sizeSpin.setValue(self.width() // 50 * 50)

    def change_size(self):
        self.size = int(self.sizeSpin.value())
        self.sizeSpin.setValue(self.size)
        self.show()
