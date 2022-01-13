import sys
from traceback import format_exception

from PyQt5.QtWidgets import QApplication

from View.edit_2d_surface import EditWindow
from View.figure_layer_edit import LayerEditWindow


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("error!:", tb)


if __name__ == '__main__':
    sys.excepthook = console_excepthook
    app = QApplication(sys.argv)
    window = LayerEditWindow()
    window.show()
    sys.exit(app.exec_())
