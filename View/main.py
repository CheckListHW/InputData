import sys
from traceback import format_exception

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from Controllers.plot_mode import ModeStatus


from Controllers.qt_connect_matplotlib import MatplotlibConnector


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.connector = MatplotlibConnector(self.draw_polygon_frame)
        self.update.clicked.connect(self.connector.update_plot)
        self.halve.clicked.connect(self.connector.halve_dot)

        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.connector.set_mode(mode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.excepthook = console_excepthook
    window.show()
    sys.exit(app.exec_())
