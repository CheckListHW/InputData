from os import environ

from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QColorDialog

from Controllers.Editor.draw_shape import Plot3d, DrawVoxels
from Controllers.qt_matplotlib_connector import EditorFigureController
from Model.shape import Shape
from Model.file import MapFile, ShapeFile
from Model.map import Map
from Model.observer import ObjectObserver
from Tools.filedialog import dict_from_json
from View.surface_draw_view import SurfaceEditWindow


class ShapeEditWindow(QMainWindow):
    def __init__(self):
        super(ShapeEditWindow, self).__init__()
        uic.loadUi(environ['project'] + '/ui/shape_edit.ui', self)

        self.map, self.file_map, self.file_shape = Map(), MapFile(self), ShapeFile(self)
        self.map.attach(ObjectObserver([self.update_all]))

        self.connector = EditorFigureController(self.viewFrame)
        self.voxels = DrawVoxels(self.map, Plot3d(self.connector))
        self.load_default_shape()
        self.handlers_connect()
        self.update()

    def load_default_shape(self):
        base_dict = dict_from_json(environ['project'] + '/base.json')
        if base_dict != {}:
            self.map.load_from_dict(base_dict)

    def handlers_connect(self) -> None:
        self.create_file_action.triggered.connect(lambda: self.map.load_from_json(self.file_map.create_file()))

        self.open_file_action.triggered.connect(lambda: self.map.load_from_json(self.file_map.open_file()))
        self.save_file_action.triggered.connect(lambda: self.file_map.save_file(self.map))
        self.saveLayerButton.clicked.connect(lambda: self.file_shape.save_file(self.layersComboBox.currentData()))

        load_layer: () = lambda: self.layersComboBox.currentData().load_from_json(self.file_shape.open_file())
        self.loadLayerButton.clicked.connect(load_layer)

        del_def: () = lambda: self.map.delete_layer(figure=self.layersComboBox.currentData())
        self.deleteLayerButton.clicked.connect(del_def)

        self.addLayerButton.clicked.connect(self.map.add_layer)
        self.acceptSettingsButton.clicked.connect(self.accept_settings)
        self.editLayerButton.clicked.connect(self.edit_layer)
        self.redrawButton.clicked.connect(self.voxels.draw_all_polygon)
        self.updateButton.clicked.connect(self.update_all)
        self.acceptLayersChange.clicked.connect(self.accept_view)
        self.allLayersCheckBox.stateChanged.connect(self.change_all_layers_show)
        self.layersComboBox.activated.connect(self.update_layers_info)
        self.nameLineEdit.editingFinished.connect(self.accept_settings)
        self.priority_spinbox.editingFinished.connect(self.accept_settings)

        self.colorButton.clicked.connect(self.show_palette)

    def show_palette(self):
        if self.layersComboBox.currentData():
            r, g, b = self.layersComboBox.currentData().color
            alpha = self.layersComboBox.currentData().alpha * 255
            cd = QColorDialog(QColor(r, g, b, alpha=alpha), self)
            cd.setOption(QColorDialog.ShowAlphaChannel, on=True)
            cd.colorSelected.connect(self.set_color)
            cd.show()

    def set_color(self, color: QColor):
        alpha = color.alpha()/255
        r, g, b, _ = color.getRgb()
        self.layersComboBox.currentData().set_property({'color': (r, g, b),
                                                        'alpha': alpha})

    def update_all(self):
        x, y, z = self.xSpinbox.text(), self.ySpinbox.text(), self.zSpinbox.text()
        self.map.s
        print(x, y, z)
        self.update_layers_info()
        self.list_displayed_layers()
        self.voxels.draw_all_polygon()

    def update_layers_info(self) -> None:
        current_index = self.layersComboBox.currentIndex() if self.layersComboBox.currentIndex() >= 0 else 0

        self.layersComboBox.clear()
        for layer in self.map.get_shapes():
            self.layersComboBox.addItem(layer.name, layer)

        self.layersComboBox.setCurrentIndex(current_index)

        layer = self.layersComboBox.currentData()
        if type(layer) is Shape:
            self.descriptionLabel.setText('Description ({0})'.format(layer.name))
            self.editLabel.setText('Edit ({0})'.format(layer.name))
            self.layerNameLabel.setText(layer.name)
            self.nameLineEdit.setText(layer.name)
            self.priority_spinbox.setValue(layer.priority)

    def list_displayed_layers(self):
        for i in reversed(range(self.showLayersScrollArea.count())):
            self.showLayersScrollArea.itemAt(i).widget().setParent(None)

        layers = self.map.get_shapes()

        for i in range(len(layers)):
            widget = QCheckBox(layers[i].name)
            widget.setChecked(layers[i].visible)
            widget.setProperty('figure', layers[i])
            widget.stateChanged.connect(self.accept_view)
            self.showLayersScrollArea.addWidget(widget, i, 0)

    def change_all_layers_show(self, check):
        for lay in self.map.get_shapes():
            lay.visible = True if check else False
        self.update_all()

    def accept_view(self):
        for i in range(self.showLayersScrollArea.count()):
            check_box = self.showLayersScrollArea.itemAt(i).widget()
            if type(check_box) is QCheckBox:
                check_box.property('figure').visible = True if check_box.checkState() else False
        self.update_all()

    def edit_layer(self):
        # self.edit_window если оставлять локальной переменной удаляется из памяти!
        self.edit_window = SurfaceEditWindow()
        self.edit_window.surface_editor.set_shape(shape=self.layersComboBox.currentData())
        self.edit_window.show()

    def accept_settings(self):
        self.layersComboBox.currentData().set_property({'name': self.nameLineEdit.text(),
                                                        'priority': self.priority_spinbox.text(),
                                                        'a1': None,
                                                        'a2': None,
                                                        })
        self.update_layers_info()
