from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class FigureWidget(QWidget):
    def __init__(self, name: str):
        super(FigureWidget, self).__init__()
        uic.loadUi('ui/figure_widget.ui', self)
        self.figureNameLabel.setText(name)
