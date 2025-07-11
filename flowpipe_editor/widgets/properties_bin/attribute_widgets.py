"""AttributesWidget for displaying flowpipe node attributes in a Qt Widget."""

import json

# pylint: disable=no-name-in-module
from Qt import QtWidgets

from flowpipe.plug import IPlug


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
        self.lineedit = QtWidgets.QLineEdit(self)
        if isinstance(self.plug.value, dict):
            self.lineedit.setText(json.dumps(self.plug.value))
        else:
            self.lineedit.setText(str(self.plug.value))
        self.layout().addWidget(self.lineedit)
        self.lineedit.setReadOnly(True)
