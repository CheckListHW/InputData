from os import getcwd
from typing import Final, Optional

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog

from Model.shape import Shape
from Model.map import Map
from Tools.filedialog import save_dict_as_json


class FileEdit:
    file_used = ''

    # Messages
    create_file_default: Final = 'Введите название файла:'
    create_file_error: Final = 'Не удалось создать файл,  \nфайл с таким именем уже существует'

    def __init__(self, parent: QMainWindow):
        self.parent = parent

    def open_file(self):
        self.file_used, _ = QFileDialog.getOpenFileName(self.parent, '', getcwd(), 'Json Files (*.json)')
        return self.file_used

    def create_file(self, message=None) -> Optional[str]:
        if not message:
            message = self.create_file_default

        filename, ok = QInputDialog.getText(self.parent, 'Input Dialog', str(message))
        if ok and filename and filename != '':
            path = QFileDialog.getExistingDirectory(self.parent, getcwd())
            self.file_used = save_dict_as_json({}, path, filename)
            return self.file_used

        return None


class ShapeFile(FileEdit):
    def save_file(self, data_figure: Shape):
        data = data_figure.get_figure_as_dict()

        if not self.file_used:
            self.create_file()
        save_dict_as_json(data=data, filename=self.file_used)


class MapFile(FileEdit):
    def save_file(self, data_map: Map):
        data, i = {}, 0
        for lay in data_map.get_shapes():
            lay.get_figure_as_dict()
            i += 1
            data[i] = lay.get_figure_as_dict()
        if not self.file_used:
            self.create_file()
        save_dict_as_json(data=data, filename=self.file_used)
