from typing import Callable

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QFrame

from Controllers.qt_matplotlib_connector import MatplotlibConnector, MatplotlibConnectorTight
from Model.surface_2d import SurfaceFigure2d, Surface2dPlus


class ViewingLayersWindow(QMainWindow):
    def __init__(self, **kwargs):
        super(ViewingLayersWindow, self).__init__()
        uic.loadUi('ui/viewing_layers.ui', self)

        self.kwargs, self.get_surfaces, self.frames, self.size = kwargs, None, list(), 200
        self.accept.clicked.connect(self.change_size)

    def set_surfaces(self, surface: Callable):
        self.get_surfaces = surface

    def add_frame_to_layout(self, index: int) -> QFrame:
        frame = QFrame(self.scrollAreaWidgetContents)
        self.frames.append(frame)
        self.layout_plots.addWidget(frame, index, 0)

        frame.setMinimumSize(self.size, self.size)
        frame.setMaximumSize(self.size, self.size)
        return frame

    def add_layer(self, index):
        self.kwargs.get('click_handler')(index)
        self.update_main_frame()

    def show(self) -> None:
        start_frame = self.add_frame_to_layout(0)
        MatplotlibConnectorTight(start_frame, tight=True, surf=Surface2dPlus(),
                                 watch_click_handler=lambda: self.add_layer(-1))

        surfaces: list[dict] = self.get_surfaces()

        for i in range(len(surfaces)):
            frame = self.add_frame_to_layout(i + 1)
            MatplotlibConnectorTight(frame, tight=True, surf=SurfaceFigure2d(surfaces[str(i)]),
                                     watch_click_handler=lambda j=i: self.kwargs.get('click_handler')(j))

        end_frame = self.add_frame_to_layout(10000)
        MatplotlibConnectorTight(end_frame, tight=True, surf=Surface2dPlus(),
                                 watch_click_handler=lambda: self.add_layer(10000))

        self.resize(self.size + 10, self.height())
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
