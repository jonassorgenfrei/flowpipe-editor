import os
import textwrap
import webbrowser
# pylint: disable=no-name-in-module
from Qt import QtCore, QtWidgets


class DescriptionWidget(QtWidgets.QWidget):
    def __init__(self, flowpipe_node, parent=None):
        super(DescriptionWidget, self).__init__(parent)

        self.fp_node = flowpipe_node

        self.node_type_label = QtWidgets.QLabel(self)
        self.node_type_label.setMinimumSize(QtCore.QSize(0, 30))

        self.open_code_btn = QtWidgets.QPushButton("Open Code", self)

        self.open_code_btn.setEnabled(
            os.path.isfile(self.fp_node.file_location)
        )

        self.description_textedit = QtWidgets.QTextEdit(self)
        self.description_textedit.setMinimumSize(QtCore.QSize(0, 30))
        self.description_textedit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description_textedit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.description_textedit.setReadOnly(True)
        self.description_textedit.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.description_textedit.setObjectName("description_textedit")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.node_type_label)
        layout.addWidget(self.description_textedit)
        layout.addWidget(self.open_code_btn)

        self.setLayout(layout)

        self.node_type_label.setText(flowpipe_node.__class__.__name__)
        self.description_textedit.setPlainText(
            textwrap.dedent(flowpipe_node.__doc__ or "").strip()
        )
        self.open_code_btn.clicked.connect(self.open_code)

    def open_code(self):
        webbrowser.open(self.fp_node.file_location)
