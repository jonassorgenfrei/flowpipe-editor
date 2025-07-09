from Qt import QtWidgets

from . import attribute_widgets


class AttributesWidget(QtWidgets.QWidget):
    def __init__(self, plugs, parent=None):
        super(AttributesWidget, self).__init__(parent)
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
