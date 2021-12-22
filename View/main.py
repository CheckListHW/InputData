import sys
from time import sleep
from traceback import format_exception

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QWidget, QVBoxLayout, QLayout, QSpinBox, QGridLayout

from Controllers.edit_plot_modes import ModeStatus
from Controllers.qt_connect_matplotlib import MatplotlibConnector


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main.ui', self)

        self.view_layers_window = ViewingLayersWindow()

        self.connector = MatplotlibConnector(self.draw_polygon_frame)
        self.button_connect()

    def button_connect(self):
        self.update.clicked.connect(self.connector.update_plot)
        self.halve.clicked.connect(self.connector.halve_dot)

        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))
        self.view_layers.clicked.connect(self.view_layers_window.show)

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.connector.set_mode(mode)


class ViewingLayersWindow(QMainWindow):
    def __init__(self):
        super(ViewingLayersWindow, self).__init__()
        uic.loadUi('ui/viewing_layers.ui', self)
        self.accept.clicked.connect(self.change_size)
        self.size = 150

    def show(self) -> None:
        # q = QGridLayout()
        # q.removeWidget()

        self.frames = list()
        for i in range(1, 20):
            frame = QFrame(self.scrollAreaWidgetContents)
            frame.setMinimumSize(self.size, self.size)
            frame.setMaximumSize(self.size, self.size)
            connector = MatplotlibConnector(frame, tight=True)
            connector.set_mode(ModeStatus.Watch)
            connector.plot.grid_off = True
            connector.plot.update_plot()
            connector.plot.ax.plot([1, 15], [0, 15])
            self.gridLayout.addWidget(frame, i, 0)
            self.frames.append(frame)

        self.resize(self.size + 100, self.height())
        super(ViewingLayersWindow, self).show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.size = self.width()
        self.sizeSpin.setValue(self.size)

    def change_size(self):
        self.size = int(self.sizeSpin.value()) // 50 * 50
        self.sizeSpin.setValue(self.size)

        for frame in self.frames:
            self.gridLayout.removeWidget(frame)
        self.show()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.excepthook = console_excepthook
#     window.show()
#     sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViewingLayersWindow()
    sys.excepthook = console_excepthook
    window.show()
    sys.exit(app.exec_())