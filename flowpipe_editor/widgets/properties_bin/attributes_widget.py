"""AttributesWidget for displaying flowpipe node attributes in a Qt Widget."""

# pylint: disable=no-name-in-module
from Qt import QtWidgets
from flowpipe.plug import IPlug
from . import attribute_widgets


class AttributesWidget(QtWidgets.QWidget):
    """A widget to display attributes of Flowpipe node plugs."""

    def __init__(self, plugs: list[IPlug], parent: QtWidgets.QWidget = None):
        """Initialize the AttributesWidget with a list of plugs and an optional parent widget.
        Args:
            plugs (list[IPlug]): List of plugs to display attributes for.
            parent (QtWidgets.QWidget, optional): Parent widget. Defaults to None.
        """

        super().__init__(parent)
        self.attributes = {}
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.scrollarea = QtWidgets.QScrollArea(self)
        self.layout().addWidget(self.scrollarea)
        self.scrollarea.setWidgetResizable(True)
        self.attributes_widget = QtWidgets.QWidget()
        self.form = QtWidgets.QFormLayout(self.attributes_widget)
        self.scrollarea.setWidget(self.attributes_widget)

        for index in list(range(self.form.count()))[::-1]:
            item = self.form.takeAt(index)
            widget = item.widget()
            widget.setParent(None)
            del widget
            del item
        for plug in plugs.values():
            widget = attribute_widgets.DefaultPlugWidget(self, plug=plug)
            self.form.addRow(plug.name, widget)
            self.attributes[plug.name] = widget
