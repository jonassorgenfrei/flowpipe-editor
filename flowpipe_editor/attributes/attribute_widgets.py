from __future__ import annotations

import json

from Qt import QtWidgets


class IPlugWidget(QtWidgets.QWidget):
    def __init__(self, parent, plug=None):
        super(IPlugWidget, self).__init__(parent)
        self.plug = plug


class DefaultPlugWidget(IPlugWidget):
    def __init__(self, parent, plug):
        super(DefaultPlugWidget, self).__init__(parent, plug)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.lineedit = QtWidgets.QLineEdit(self)
        if isinstance(self.plug.value, dict):
            self.lineedit.setText(json.dumps(self.plug.value))
        else:
            self.lineedit.setText(str(self.plug.value))
        self.layout().addWidget(self.lineedit)
        self.lineedit.setReadOnly(True)
