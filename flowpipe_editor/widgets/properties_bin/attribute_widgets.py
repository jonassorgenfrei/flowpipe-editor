"""AttributesWidget for displaying flowpipe node attributes in a Qt Widget."""

from __future__ import annotations

import json

from flowpipe.plug import IPlug

# pylint: disable=no-name-in-module
from Qt import QtGui, QtWidgets


class PopeUpLineEdit(QtWidgets.QLineEdit):
    """A QLineEdit that opens a popup dialog on double-click to show/edit its content."""

    def __init__(self, label: str, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.label = label

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        # Open popup dialog on double-click
        dialog = PopupDialog(self.label, self.text(), self)
        dialog.exec_()
        # Optionally call the parent event if you still want default behavior
        super().mouseDoubleClickEvent(event)


class PopupDialog(QtWidgets.QDialog):
    """A popup dialog that displays a larger text area for editing/viewing content."""

    def __init__(
        self, label: str, value: str, parent: QtWidgets.QWidget = None
    ):
        super().__init__(parent=parent)
        self.setWindowTitle(label)
        self.resize(400, 400)

        layout = QtWidgets.QVBoxLayout()

        self.input_field = QtWidgets.QTextEdit()
        self.input_field.setText(value)
        self.input_field.setReadOnly(True)
        layout.addWidget(self.input_field)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)


class IPlugWidget(QtWidgets.QWidget):
    """Base class for plug widgets."""

    def __init__(self, parent: QtWidgets.QWidget, plug=None):
        super().__init__(parent)
        self.plug = plug


class DefaultPlugWidget(QtWidgets.QWidget):
    """Default widget for displaying plug attributes."""

    def __init__(self, parent: QtWidgets, plug: IPlug):
        """Initialize the DefaultPlugWidget with a parent and a plug.
        Args:
            parent (QtWidgets.QWidget): Parent widget.
            plug (IPlug): The plug to display attributes for.
        """
        super().__init__(parent)
        self.plug = plug
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.lineedit = PopeUpLineEdit(self.plug.name, self)
        if isinstance(self.plug.value, dict):
            try:
                self.lineedit.setText(json.dumps(self.plug.value, indent=1))
            except TypeError:
                # If the value cannot be serialized, fall back to str
                self.lineedit.setText(str(self.plug.value))
        else:
            self.lineedit.setText(str(self.plug.value))
        self.layout().addWidget(self.lineedit)
        self.lineedit.setReadOnly(True)
