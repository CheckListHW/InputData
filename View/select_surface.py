from typing import Callable

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QFrame

from Controllers.qt_matplotlib_connector import MatplotlibConnectorTight
from Model.surface_2d import SurfaceFigure2d
from View.single_lay_view import SingleLayWidget


class ViewingLayersWindow(QMainWindow):
    def __init__(self, **kwargs):
        super(ViewingLayersWindow, self).__init__()
        uic.loadUi('ui/viewing_layers.ui', self)
        # добавляется для того чтобы сборщик мусора не удалял объекты
        self.aaa = []

        self.kwargs, self.get_surfaces, self.frames, self.size = kwargs, None, list(), 200
        self.accept.clicked.connect(self.change_size)

    def set_surfaces(self, surface: Callable):
        self.get_surfaces = surface

    def add_frame_to_layout(self, index: int) -> QFrame:
        frame = SingleLayWidget(index, edit_lay_handler=self.edit_layer)
        self.layout_plots.addWidget(frame, index, 0)

        frame.setMinimumSize(self.size, self.size)
        frame.setMaximumSize(self.size, self.size)
        self.frames.append(frame)
        self.aaa.append(frame)
        return frame.viewFrame

    def edit_layer(self, index: int, edit_method: str = 'add', **kwargs):
        self.kwargs.get('edit_lay_handler')(index, edit_method, **kwargs)
        self.update_main_frame()

    def change_layer(self, index):
        if self.kwargs.get('change_lay_handler')(index):
            self.update_main_frame()

    def show(self) -> None:
        if not hasattr(self, 'get_surfaces'):
            return

        surfaces: list[dict] = self.get_surfaces().get('layers')

        for i in range(len(surfaces)):
            frame = self.add_frame_to_layout(i)
            MatplotlibConnectorTight(frame, tight=True, surf=SurfaceFigure2d(lay=surfaces[str(i)]),
                                     watch_click_handler=lambda j=i: self.change_layer(j))

        self.resize(self.size + 20, self.height())
        super(ViewingLayersWindow, self).show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.sizeSpin.setValue(self.width() // 50 * 50)

    def change_size(self):
        self.size = int(self.sizeSpin.value())
        self.sizeSpin.setValue(self.size)
        self.update_main_frame()

    # тут все очень важное меняй с умом!!!
    def update_main_frame(self):
        for i in reversed(range(self.layout_plots.count())):
            self.layout_plots.itemAt(i).widget().setParent(None)

        for frame in self.frames:
            for children in frame.children():
                children.setParent(None)

        self.frames = list()
        self.show()
