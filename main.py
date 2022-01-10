import sys
from traceback import format_exception

from PyQt5.QtWidgets import QApplication

from View.edit_2d_surface import EditWindow


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("error!:", tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EditWindow()
    sys.excepthook = console_excepthook
    window.show()
    sys.exit(app.exec_())
