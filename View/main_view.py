import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QGridLayout

from View.mini_figure_view import FigureWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main.ui', self)
        for i in range(10):
            widget = FigureWidget(name='Figure '+str(i))
            self.figures.addWidget(widget, 0, i)

        self.button_connect()

    def button_connect(self):
        pass
