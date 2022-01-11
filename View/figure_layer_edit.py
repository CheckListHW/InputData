import os
from typing import Final

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QInputDialog

from Model.map import Map
from Tools.filedialog import save_as_json

# Messages

create_file_default: Final = 'Введите название файла:'
create_file_error: Final = 'Не удалось создать файл,  \nфайл с таким именем уже существует'


class LayerEditWindow(QMainWindow):
    file_used = ''

    def __init__(self):
        self.map = Map()
        super(LayerEditWindow, self).__init__()
        uic.loadUi('ui/figure_layer_edit.ui', self)

        self.button_connect()

    def button_connect(self):
        self.create_file_action.triggered.connect(self.create_file)
        self.open_file_action.triggered.connect(self.open_file)
        self.save_file_action.triggered.connect(self.save_file)
        self.addLayerButton.clicked.connect(self.add_layer)
        self.deleteLayerButton.clicked.connect(self.delete_layer)

    def create_file(self, message=None):
        if not message:
            message = create_file_default

        filename, ok = QInputDialog.getText(self, 'Input Dialog', str(message))
        if ok:
            path = QFileDialog.getExistingDirectory(self, os.getcwd())
            save_path = save_as_json({}, path, filename)
            if save_path:
                self.file_used = save_path
            else:
                self.create_file(create_file_error)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '', os.getcwd(), 'Json Files (*.json)')
        self.file_used = file_path

    def save_file(self):
        pass

    def add_layer(self):
        self.map.add_layer()
        pass

    def delete_layer(self):
        self.map.delete_layer()
        pass
