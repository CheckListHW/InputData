import sys
from traceback import format_exception

from PyQt5.QtWidgets import QApplication

from View.edit_2d_surface import EditWindow
from View.figure_layer_edit import LayerEditWindow
from View.select_surface import ViewingLayersWindow


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("error!:", tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = console_excepthook
    window = EditWindow()
    window.show()
    sys.exit(app.exec_())
