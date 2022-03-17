import os
import sys
from traceback import format_exception

from mvc.View.shapes_edit_view import ShapeEditWindow

os.environ['project'] = os.getcwd()

from PyQt5.QtWidgets import QApplication


def console_excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(format_exception(exc_type, exc_value, exc_tb))
    print("error!:", tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = console_excepthook
    window = ShapeEditWindow()
    window.show()
    sys.exit(app.exec_())
