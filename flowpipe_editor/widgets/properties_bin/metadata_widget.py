'"""MetadataWidget for displaying metadata in a Qt Widget."""'

import json
from pathlib import Path

# pylint: disable=no-name-in-module
from Qt import QtWidgets


def json_safe(obj):
    """JSON serializer for objects not serializable by default json code."""
    if isinstance(obj, Path):
        return str(obj)
    return str(obj)  # optional fallback for other unknown types


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

        self.text_edit.setPlainText(
            json.dumps(metadata, indent=4, default=json_safe)
        )
