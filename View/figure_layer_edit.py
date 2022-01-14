import os
from typing import Final, Callable

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QCheckBox, QSpacerItem, QSpinBox

from Controllers.Editor.draw3d import Plot3d, DrawVoxels
from Controllers.qt_matplotlib_connector import MatplotlibConnector3dViewing
from Model.figure_3d import Figure3d
from Model.map import Map
from Model.observer import Observer, Subject
from Tools.filedialog import save_as_json
from View.edit_2d_surface import EditWindow


class LayerEditWindow(QMainWindow):
    def __init__(self):
        super(LayerEditWindow, self).__init__()
        uic.loadUi('ui/figure_layer_edit.ui', self)

        self.map, self.file = Map(), MapFile(self)

        self.handlers_connect()
        self.map.attach(LayerEditObserver([self.update_all]))

        self.connector = MatplotlibConnector3dViewing(self.viewFrame)

        self.map.random_layer_for_test()
        self.voxels = DrawVoxels(self.map, Plot3d(self.connector.figure, self.connector.ax))
        self.update_all()

    def handlers_connect(self) -> None:
        self.create_file_action.triggered.connect(self.file.create_file)
        self.open_file_action.triggered.connect(self.file.open_file)
        self.save_file_action.triggered.connect(lambda: self.file.save_file(self.map))

        del_def: () = lambda: self.map.delete_layer(figure=self.layersComboBox.currentData())
        self.deleteLayerButton.clicked.connect(del_def)
        self.addLayerButton.clicked.connect(self.map.add_layer)
        self.acceptSettingsButton.clicked.connect(self.accept_settings)
        self.editLayerButton.clicked.connect(self.edit_layer)
        self.updateViewButton.clicked.connect(self.update_view_map)
        self.acceptLayersChange.clicked.connect(self.accept_view)

        self.allLayersCheckBox.stateChanged.connect(self.change_all_layers_show)
        self.layersComboBox.activated.connect(self.update_layers_info)

    def update_all(self):
        self.update_layers_info()
        self.update_show_layers()
        self.update_view_map()

    def update_view_map(self):
        self.voxels.update()
        self.connector.draw()

    def update_layers_info(self) -> None:
        current_index = self.layersComboBox.currentIndex() if self.layersComboBox.currentIndex() >= 0 else 0

        self.layersComboBox.clear()
        for layer in self.map.get_figures():
            self.layersComboBox.addItem(layer.name, layer)

        self.layersComboBox.setCurrentIndex(current_index)

        layer = self.layersComboBox.currentData()
        if type(layer) is Figure3d:
            self.descriptionLabel.setText('Description ({0})'.format(layer.name))
            self.editLabel.setText('Edit ({0})'.format(layer.name))
            self.layerNameLabel.setText(layer.name)
            self.nameLineEdit.setText(layer.name)
            r, g, b = layer.get_color()
            self.colorRSpinBox.setValue(r)
            self.colorGSpinBox.setValue(g)
            self.colorBSpinBox.setValue(b)
            self.alphaSpinBox.setValue(layer.alpha)

    def update_show_layers(self):
        layers = self.map.get_figures()

        for i in reversed(range(self.showLayersScrollArea.count())):
            self.showLayersScrollArea.itemAt(i).widget().setParent(None)

        for i in range(len(layers)):
            widget = QCheckBox(layers[i].name)
            widget.setChecked(layers[i].visible)
            widget.setProperty('figure', layers[i])
            widget.stateChanged.connect(self.accept_view)
            self.showLayersScrollArea.addWidget(widget, i, 0)

    def change_all_layers_show(self, check):
        for lay in self.map.get_figures():
            lay.visible = True if check == 2 else False

        self.update_all()

    def accept_view(self):
        for i in range(self.showLayersScrollArea.count()):
            check_box = self.showLayersScrollArea.itemAt(i).widget()
            if type(check_box) is QCheckBox:
                if check_box.checkState():
                    check_box.property('figure').visible = True
                else:
                    check_box.property('figure').visible = False

        self.update_all()

    def edit_layer(self):
        # self.edit_window если оставлять локальной переменной удаляется из памяти!
        self.edit_window = EditWindow()
        self.edit_window.set_figure(figure=self.layersComboBox.currentData())
        self.edit_window.show()

    def accept_settings(self):
        color = '{0},{1},{2}'.format(self.colorRSpinBox.value(), self.colorGSpinBox.value(), self.colorBSpinBox.value())
        self.layersComboBox.currentData().set_property({'name': self.nameLineEdit.text(),
                                                        'priority': self.priority_spinbox.text(),
                                                        'color': color,
                                                        'alpha': self.alphaSpinBox.value(),
                                                        'a1': None,
                                                        'a2': None,
                                                        })
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
            save_as_json(data=lay.get_figure_as_dict(), filename=lay.name)
        pass


class LayerEditObserver(Observer):
    def __init__(self, handlers: [Callable]):
        super(LayerEditObserver, self).__init__()
        self.__handlers = list[Callable]()
        self.add_handlers(handlers)

    def add_handler(self, handler: Callable) -> None:
        self.__handlers.append(handler)

    def add_handlers(self, handlers: [Callable]) -> None:
        for handler in handlers:
            self.add_handler(handler)

    def update(self, subject: Subject) -> None:
        print('-----update-------')
        for handler in self.__handlers:
            handler()
