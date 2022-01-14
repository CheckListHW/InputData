import os
from typing import Final, Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QCheckBox, QSpacerItem

from Controllers.Editor.draw3d import Plot3d, DrawVoxels
from Controllers.qt_matplotlib_connector import MatplotlibConnector3dViewing
from Model.figure_3d import Figure3d
from Model.map import Map
from Model.observer import Observer, Subject
from Tools.filedialog import save_as_json
from View.edit_2d_surface import EditWindow


class LayerEditObserver(Observer):
    __handlers = list[Callable]()

    def add_handler(self, handler: Callable) -> None:
        self.__handlers.append(handler)

    def add_handlers(self, handlers: [Callable]) -> None:
        for handler in handlers:
            self.add_handler(handler)

    def update(self, subject: Subject) -> None:
        for handler in self.__handlers:
            handler()


class LayerEditWindow(QMainWindow):
    visible = False

    def __init__(self):
        self.map, self.file = Map(), MapFile(self)

        super(LayerEditWindow, self).__init__()
        uic.loadUi('ui/figure_layer_edit.ui', self)

        self.handlers_connect()
        self.layer_observer_build()

        connector = MatplotlibConnector3dViewing(self.viewFrame)
        plot = Plot3d(connector.figure, connector.ax)
        self.map.add_layer(Figure3d(path='C:/Users/KosachevIV/PycharmProjects/InputData/lay_name254.json'))
        self.map.add_layer(Figure3d(path='C:/Users/KosachevIV/PycharmProjects/InputData/lay_name607.json'))
        self.voxels = DrawVoxels(self.map.get_figures(), plot)

    def update3dView(self):
        self.voxels.update()

    def layer_observer_build(self) -> None:
        observer = LayerEditObserver()
        observer.add_handler(self.update_layers_info)
        self.map.attach(observer)

    def update_layers_info(self) -> None:
        current_index = self.layersComboBox.currentIndex() if self.layersComboBox.currentIndex() >= 0 else 0

        self.layersComboBox.clear()
        for layer in self.map.get_figures():
            self.layersComboBox.addItem(layer.name, layer)

        self.layersComboBox.setCurrentIndex(current_index)

        self.update_show_layers()

        try:
            layer = self.layersComboBox.currentData()
            self.descriptionLabel.setText('Description ({0})'.format(layer.name))
            self.editLabel.setText('Edit ({0})'.format(layer.name))
            self.layerNameLabel.setText(layer.name)
            self.nameLineEdit.setText(layer.name)
        except:
            return

    def update_show_layers(self):
        layers = self.map.get_figures()

        for i in reversed(range(self.showLayersScrollArea.count())):
            if not type(self.showLayersScrollArea.itemAt(i)) is QSpacerItem:
                self.showLayersScrollArea.itemAt(i).widget().setParent(None)

        for i in range(len(layers)):
            widget = QCheckBox(layers[i].name)
            widget.setChecked(self.visible)
            self.showLayersScrollArea.addWidget(widget, i, 0)

    def change_all_layers_show(self, check):
        if check == 0:
            self.visible = False
        else:
            self.visible = True

        self.update_layers_info()

    def handlers_connect(self) -> None:
        self.create_file_action.triggered.connect(self.file.create_file)
        self.open_file_action.triggered.connect(self.file.open_file)
        self.save_file_action.triggered.connect(lambda: self.file.save_file(self.map))
        self.addLayerButton.clicked.connect(self.map.add_layer)
        self.deleteLayerButton.clicked.connect(self.map.delete_layer)
        self.acceptSettingsButton.clicked.connect(self.accept_settings)
        self.editLayerButton.clicked.connect(self.edit_layer)
        self.updateViewButton.clicked.connect(self.update3dView)
        self.allLayersCheckBox.stateChanged.connect(self.change_all_layers_show)

        self.layersComboBox.activated.connect(self.update_layers_info)

    def edit_layer(self):
        # self.edit_window если оставлять локальной переменной удаляется из памяти!
        self.edit_window = EditWindow()
        print()
        self.edit_window.set_figure(figure=self.map.get_figures()[0])
        self.edit_window.show()

    def accept_settings(self):
        self.layersComboBox.currentData().set_property({'name': self.nameLineEdit.text(),
                                                        'priority': self.priority_spinbox.text()})
        self.update_layers_info()


class MapFile:
    file_used = ''

    # Messages
    create_file_default: Final = 'Введите название файла:'
    create_file_error: Final = 'Не удалось создать файл,  \nфайл с таким именем уже существует'

    def __init__(self, parent: QMainWindow):
        self.parent = parent

    def create_file(self, message=None):
        if not message:
            message = self.create_file_default

        filename, ok = QInputDialog.getText(self.parent, 'Input Dialog', str(message))
        if ok:
            path = QFileDialog.getExistingDirectory(self.parent, os.getcwd())
            save_path = save_as_json({}, path, filename)
            if save_path:
                self.file_used = save_path
            else:
                self.create_file(self.create_file_error)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.parent, '', os.getcwd(), 'Json Files (*.json)')
        self.file_used = file_path

    def save_file(self, map: Map):
        for lay in map.get_figures():
            lay.get_figure_as_dict()
            save_as_json(dict=lay.get_figure_as_dict(), filename=lay.name)
        pass
