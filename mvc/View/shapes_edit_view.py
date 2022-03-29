from os import environ

from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QColorDialog

from mvc.Controller.draw_shape import Plot3d, DrawVoxels
from mvc.Controller.qt_matplotlib_connector import EditorFigureController
from utils.file import FileEdit
from mvc.Model.shape import Shape
from mvc.Model.map import Map, ExportMap
from utils.observer import ObjectObserver
from utils.filedialog import dict_from_json
from mvc.View.roof_profile_view import RoofProfileEditWindow
from mvc.View.split_edit_view import SplitEditWindow
from mvc.View.surface_draw_view import SurfaceEditWindow


class ShapeEditWindow(QMainWindow):
    def __init__(self):
        super(ShapeEditWindow, self).__init__()
        uic.loadUi(environ['project'] + '/ui/shape_edit.ui', self)

        self.map, self.file_edit = Map(), FileEdit(self)
        self.connector = EditorFigureController(self.viewFrame)
        self.voxels = DrawVoxels(self.map, Plot3d(self.connector))
        self.load_default_shape()
        self.handlers_connect()

        self.map.attach(ObjectObserver([self.update_all, self.save_map]))
        self.update_all()
        # self.debug()

    def debug(self):
        self.edit_layer()

    def load_default_shape(self):
        base_dict = dict_from_json(environ['project'] + '/base.json')
        if base_dict != {}:
            self.file_edit.file_used = environ['project'] + '/base.json'
            self.map.load_from_dict(base_dict)

    def save_map(self):
        self.file_edit.save_file(self.map.get_as_dict())

    def handlers_connect(self) -> None:
        self.create_file_action.triggered.connect(lambda: self.map.load_from_json(self.file_edit.create_file()))

        self.open_file_action.triggered.connect(lambda: self.map.load_from_json(self.file_edit.open_file()))
        self.exportMapAction.triggered.connect(lambda: FileEdit(self).save_file(ExportMap(self.map)()))
        self.save_file_action.triggered.connect(self.save_map)

        save_shape: () = lambda: self.file_edit.save_file(self.layersComboBox.currentData().get_as_dict)
        self.saveLayerButton.clicked.connect(save_shape)

        load_layer: () = lambda: self.layersComboBox.currentData().load_from_json(self.file_edit.open_file())
        self.loadLayerButton.clicked.connect(load_layer)

        del_def: () = lambda: self.map.delete_layer(figure=self.layersComboBox.currentData())
        self.deleteLayerButton.clicked.connect(del_def)

        self.addLayerButton.clicked.connect(lambda: self.map.add_layer())
        self.acceptSettingsButton.clicked.connect(self.accept_settings)
        self.editLayerButton.clicked.connect(self.edit_layer)
        self.redrawButton.clicked.connect(self.voxels.redraw)
        self.updateButton.clicked.connect(self.update_all)
        self.acceptLayersChange.clicked.connect(self.accept_view)

        self.allLayersCheckBox.stateChanged.connect(self.change_all_layers_show)
        self.layersComboBox.activated.connect(self.update_layers_info)

        self.nameLineEdit.editingFinished.connect(self.accept_settings)
        self.priority_spinbox.editingFinished.connect(self.accept_settings)
        self.fillerCheckBox.stateChanged.connect(self.accept_filler)

        self.xEndSpinbox.editingFinished.connect(self.accept_size)
        self.xEndSpinbox.setValue(self.map.size.x_constraints.end)

        self.yEndSpinbox.editingFinished.connect(self.accept_size)
        self.yEndSpinbox.setValue(self.map.size.y_constraints.end)

        self.zStartSpinbox.editingFinished.connect(self.accept_size)
        self.zEndSpinbox.editingFinished.connect(self.accept_size)

        self.colorButton.clicked.connect(lambda: self.show_palette(self.set_color_shape))

        self.shapePartNameComboBox.activated.connect(self.update_part_info)

        self.split_handlers_connect()
        self.speedPlotDrawComboBox.activated.connect(self.change_draw_speed)

    def change_draw_speed(self):
        self.map.draw_speed = self.speedPlotDrawComboBox.currentText()
        if self.map.draw_speed != 'Polygon':
            self.voxels.redraw()

    def change_part_offset(self):
        layer: Shape = self.layersComboBox.currentData()
        part_name: str = self.shapePartNameComboBox.currentText()
        layer.parts_property.get(part_name).offset = self.partOffsetSpinBox.value()

    def split_handlers_connect(self):
        self.partOffsetSpinBox.editingFinished.connect(self.change_part_offset)

    def set_color_part(self, color: QColor):
        r, g, b, _ = color.getRgb()

        self.layersComboBox.currentData().split_controller. \
            change_part_color(int(self.partNumberComboBox.currentText()) - 1, [r, g, b])

    def set_color_shape(self, color: QColor):
        alpha = color.alpha() / 255
        r, g, b, _ = color.getRgb()
        self.layersComboBox.currentData().load_from_dict({'color': [r, g, b],
                                                          'alpha': alpha})

    def show_palette(self, handler):
        if self.layersComboBox.currentData():
            r, g, b = self.layersComboBox.currentData().color
            alpha = self.layersComboBox.currentData().alpha * 255
            cd = QColorDialog(QColor(r, g, b, alpha=alpha), self)
            cd.setOption(QColorDialog.ShowAlphaChannel, on=True)
            cd.colorSelected.connect(handler)
            cd.show()

    def accept_size(self):
        x = self.map.height if self.map.height >= int(self.zEndSpinbox.text()) else int(self.zEndSpinbox.text())
        self.zEndSpinbox.setValue(x)
        x_end, y_end = self.xEndSpinbox.value(), self.yEndSpinbox.value()
        z_start, z_end = self.zStartSpinbox.value(), self.zEndSpinbox.value()
        self.map.size.change_constraints(None, x_end, None, y_end, z_start, z_end)

    def update_all(self):
        self.accept_size()
        self.update_layers_info()
        self.list_displayed_layers()
        self.voxels.redraw()

    def update_layers_info(self) -> None:
        current_index = self.layersComboBox.currentIndex() if self.layersComboBox.currentIndex() >= 0 else 0
        self.layersComboBox.clear()

        for layer in self.map.get_shapes():
            self.layersComboBox.addItem(layer.name, layer)

        self.layersComboBox.setCurrentIndex(current_index)

        layer: Shape = self.layersComboBox.currentData()
        if type(layer) is Shape:
            self.editLabel.setText('Edit ({0})'.format(layer.name))
            self.layerNameLabel.setText(layer.name)
            self.nameLineEdit.setText(layer.name)
            self.priority_spinbox.setValue(layer.priority)
            self.fillerCheckBox.setChecked(layer.filler)
            self.shapePartNameComboBox.clear()

            for part in layer.parts_property:
                self.shapePartNameComboBox.addItem(part)

        self.update_part_info()

    def update_part_info(self):
        layer: Shape = self.layersComboBox.currentData()
        part_name: str = self.shapePartNameComboBox.currentText()
        try:
            self.partOffsetSpinBox.setValue(layer.parts_property.get(part_name).offset)
        except AttributeError:
            pass

    def list_displayed_layers(self):
        for i in reversed(range(self.showLayersScrollArea.count())):
            self.showLayersScrollArea.itemAt(i).widget().setParent(None)

        layers = self.map.get_shape_with_part()

        for i in range(len(layers)):
            widget = QCheckBox(layers[i].name + layers[i].sub_name)
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
        edit_text: str = self.editPropertyComboBox.currentText()
        if edit_text.__contains__('Layer'):
            self.edit_window = SurfaceEditWindow(shape=self.layersComboBox.currentData())
        elif edit_text.__contains__('Split'):
            self.edit_window = SplitEditWindow(self.layersComboBox.currentData())
        elif edit_text.__contains__('Roof'):
            self.edit_window = RoofProfileEditWindow(self.map)
        else:
            return
        self.edit_window.show()

    def accept_settings(self):
        self.layersComboBox.currentData().load_from_dict({'name': self.nameLineEdit.text(),
                                                          'filler': self.fillerCheckBox.isChecked(),
                                                          'priority': self.priority_spinbox.text()})
        self.update_layers_info()

    def accept_filler(self):
        self.layersComboBox.currentData().load_from_dict({'filler': self.fillerCheckBox.isChecked()})
        self.update_layers_info()
