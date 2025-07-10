import json
# pylint: disable=no-name-in-module
from Qt import QtWidgets


class MetadataWidget(QtWidgets.QWidget):
    def __init__(self, metadata, parent=None):
        super(MetadataWidget, self).__init__(parent)

        # Create widgets
        self.text_edit = QtWidgets.QTextEdit()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.text_edit.setPlainText(json.dumps(metadata, indent=4))
