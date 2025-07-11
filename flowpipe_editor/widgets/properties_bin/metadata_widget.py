'"""MetadataWidget for displaying metadata in a Qt Widget."""'

import json

# pylint: disable=no-name-in-module
from Qt import QtWidgets


class MetadataWidget(QtWidgets.QWidget):
    """Widget for displaying metadata in a formatted text area."""
    def __init__(self, metadata: dict, parent: QtWidgets.QWidget = None):
        """Initialize the MetadataWidget with metadata and parent widget.
        Args:
            metadata (dict): Metadata to display.
            parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        # Create widgets
        self.text_edit = QtWidgets.QTextEdit()

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

        self.text_edit.setPlainText(json.dumps(metadata, indent=4))
