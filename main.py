import sys
from traceback import format_exception

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from ChangeName.Editor3d.plot_mode import ModeStatus


from Controllers.qt_connect_matplotlib import MatplotlibConnector


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.connector = MatplotlibConnector(self.draw_polygon_frame)
        show_3d = self.connector.plot.show_3d_figure
        self.update.clicked.connect(show_3d)

        self.deleteDot.clicked.connect(lambda: self.change_mode(ModeStatus.DeleteDot))
        self.addDot.clicked.connect(lambda: self.change_mode(ModeStatus.AddDot))
        self.moveDot.clicked.connect(lambda: self.change_mode(ModeStatus.MoveDot))
        self.drawCurve.clicked.connect(lambda: self.change_mode(ModeStatus.DrawCurve))

    def change_mode(self, mode: ModeStatus):
        self.modeName.setText(str(mode).replace('ModeStatus.', ''))
        self.connector.set_mode(mode)

    def console_excepthook(self, exc_type, exc_value, exc_tb):
        tb = "".join(format_exception(exc_type, exc_value, exc_tb))
        self.debug_list.addItem(tb)
        print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.excepthook = window.console_excepthook
    window.show()
    sys.exit(app.exec_())
