import os

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from mvc.Model.map import ExportRoof, Map
from utils.file import FileEdit


class RoofExportDialog(QDialog):
    def __init__(self, data_map: Map):
        super(RoofExportDialog, self).__init__()
        uic.loadUi(os.environ['project']+'/ui/roof_export_window.ui', self)
        self.data_map = data_map
        self.buttonBox.accepted.connect(self.export)

    def export(self):
        file = FileEdit(self)
        path = file.create_file(filename=self.fileNameLineEdit.text())
        ExportRoof(self.data_map, path=path, initial_depth=self.initialDepthSpinBox.value(),
                   step_depth=self.stepDepthDoubleSpinBox.value())
