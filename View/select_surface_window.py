from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QFrame, QGridLayout

from Controllers.qt_connect_matplotlib import MatplotlibConnector
from Model.surface_2d import SurfaceFigure2d, Surface2dPlus


class ViewingLayersWindow(QMainWindow):
    def __init__(self, **kwargs):
        super(ViewingLayersWindow, self).__init__()
        self.kwargs, self.surfaces, self.frames, self.size = kwargs, None, list(), 150
        uic.loadUi('ui/viewing_layers.ui', self)
        self.accept.clicked.connect(self.change_size)

    def set_surfaces(self, surface: dict):
        self.surfaces = surface

    def create_frame(self) -> QFrame:
        frame = QFrame(self.scrollAreaWidgetContents)
        frame.setMinimumSize(self.size, self.size)
        frame.setMaximumSize(self.size, self.size)
        return frame

    def add_layer(self, index):
        print('asd')
        self.kwargs.get('click_handler')(index)
        self.change_size()

    def show(self) -> None:
        if not hasattr(self, 'add_frame'):
            self.add_frame = self.create_frame()
            self.gridLayout.addWidget(self.add_frame, 1, 0)
            MatplotlibConnector(self.add_frame, tight=True, surf=Surface2dPlus(),
                                watch_click_handler=lambda: self.add_layer(0))

        for surface in self.surfaces:
            frame = self.create_frame()
            self.frames.append(frame)
            self.gridLayout.addWidget(frame, int(surface), 0)
            MatplotlibConnector(frame, tight=True, surf=SurfaceFigure2d(self.surfaces[surface]),
                                watch_click_handler=lambda i=int(surface): self.kwargs.get('click_handler')(i))

        # end_frame = self.create_frame()
        # self.gridLayout.addWidget(end_frame, len(self.frames), 0)
        # MatplotlibConnector(end_frame, tight=True, surf=Surface2dPlus(),
        #                     watch_click_handler=lambda i=len(self.frames)+1: self.add_layer(i))
        self.resize(self.size + 10, self.height())
        super(ViewingLayersWindow, self).show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.size = self.width()
        self.sizeSpin.setValue(self.width() // 50 * 50)

    def change_size(self):
        self.size = int(self.sizeSpin.value())
        self.sizeSpin.setValue(self.size)

        for frame in self.frames:
            self.gridLayout.removeWidget(frame)
        self.frames = list()
        self.show()
