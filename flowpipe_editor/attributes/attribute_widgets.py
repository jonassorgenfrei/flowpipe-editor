"""Flowpipe Editor Attribute Helper Widgets"""
from __future__ import annotations

import json
# pylint: disable=no-name-in-module
from Qt import QtWidgets


class IPlugWidget(QtWidgets.QWidget):
    """Base class for plug widgets."""
    def __init__(self, parent:QtWidgets.QWidget, plug=None):
        super().__init__(parent)
        self.plug = plug


class DefaultPlugWidget(IPlugWidget):
    """Default widget for displaying plug attributes."""
    def __init__(self, parent, plug):
        super().__init__(parent, plug)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.lineedit = QtWidgets.QLineEdit(self)
        if isinstance(self.plug.value, dict):
            self.lineedit.setText(json.dumps(self.plug.value))
        else:
            self.lineedit.setText(str(self.plug.value))
        self.layout().addWidget(self.lineedit)
        self.lineedit.setReadOnly(True)
