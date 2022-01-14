from typing import Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SingleLayWidget(QWidget):
    def __init__(self, index: int, edit_lay_handler: Callable = None):
        super(SingleLayWidget, self).__init__()
        uic.loadUi('C:/Users/KosachevIV/PycharmProjects/InputData/ui/view_single_lay.ui', self)
        self.add_lay: () = edit_lay_handler
        self.index = index
        self.addPreButton.clicked.connect(self.add_pre_lay)
        self.addPostButton.clicked.connect(self.add_post_lay)
        self.delButton.clicked.connect(self.del_lay)
        self.indexLabel.setText(str(index))

    def add_pre_lay(self):
        print(self.index, 'pre')
        self.add_lay(self.index)

    def add_post_lay(self):
        print(self.index+1, 'post')
        self.add_lay(self.index+1)

    def del_lay(self):
        print(-self.index, 'del')
        self.add_lay(-self.index)

