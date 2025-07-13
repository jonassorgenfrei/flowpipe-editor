"""Flowpipe Node Property Editor Widget"""

from collections import defaultdict

from NodeGraphQt.constants import NodeEnum
from NodeGraphQt.custom_widgets.properties_bin.node_property_factory import (
    NodePropertyWidgetFactory,
)
from NodeGraphQt.custom_widgets.properties_bin.node_property_widgets import (
    _PortConnectionsContainer,
    _PropertiesContainer,
    _PropertiesList,
)
from NodeGraphQt.custom_widgets.properties_bin.prop_widgets_base import (
    PropLineEdit,
)

# pylint: disable=no-name-in-module
from Qt import QtCompat, QtCore, QtGui, QtWidgets

from ..dark_theme import apply_dark_theme
from .attributes_widget import AttributesWidget
from .description import DescriptionWidget
from .metadata_widget import MetadataWidget


class FlowpipeNodePropEditorWidget(QtWidgets.QWidget):
    """
    Node properties editor widget for display a Node object.

    Args:
        parent (QtWidgets.QWidget): parent object.
        node (NodeGraphQtCore.Qt.NodeObject): node.
    """

    #: signal (node_id, prop_name, prop_value)
    property_changed = QtCore.Signal(str, str, object)
    property_closed = QtCore.Signal(str)

    def __init__(self, parent=None, node=None):
        super().__init__(parent)
        self.__node_id = node.id
        self.__tab_windows = {}
        self.__tab = QtWidgets.QTabWidget()

        pixmap = QtGui.QPixmap()
        if node.icon():
            pixmap = QtGui.QPixmap(node.icon())

            if pixmap.size().height() > NodeEnum.ICON_SIZE.value:
                pixmap = pixmap.scaledToHeight(
                    NodeEnum.ICON_SIZE.value, QtCore.Qt.SmoothTransformation
                )
            if pixmap.size().width() > NodeEnum.ICON_SIZE.value:
                pixmap = pixmap.scaledToWidth(
                    NodeEnum.ICON_SIZE.value, QtCore.Qt.SmoothTransformation
                )

        icon_label = QtWidgets.QLabel(self)
        icon_label.setPixmap(pixmap)
        icon_label.setStyleSheet("background: transparent;")

        close_btn = QtWidgets.QPushButton()
        close_btn.setIcon(
            QtGui.QIcon(
                self.style().standardIcon(
                    QtWidgets.QStyle.SP_DialogCloseButton
                )
            )
        )
        close_btn.setMaximumWidth(40)
        close_btn.setToolTip("close property")
        close_btn.clicked.connect(self._on_close)

        self.name_wgt = PropLineEdit()
        self.name_wgt.set_name("name")
        self.name_wgt.setToolTip("name\nSet the node name.")
        self.name_wgt.set_value(node.name())
        self.name_wgt.value_changed.connect(self._on_property_changed)

        self.type_wgt = QtWidgets.QLabel(node.type_)
        self.type_wgt.setAlignment(QtCore.Qt.AlignRight)
        self.type_wgt.setToolTip(
            "type_\nNode type identifier followed by the class name."
        )
        font = self.type_wgt.font()
        font.setPointSize(10)
        self.type_wgt.setFont(font)

        name_layout = QtWidgets.QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.addWidget(icon_label)
        name_layout.addWidget(self.name_wgt)
        name_layout.addWidget(close_btn)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(4)
        layout.addLayout(name_layout)
        layout.addWidget(self.__tab)
        layout.addWidget(self.type_wgt)

        self._port_connections = self._read_node(node)

    def __repr__(self):
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"

    def _on_close(self):
        """
        called by the close button.
        """
        self.property_closed.emit(self.__node_id)

    def _on_property_changed(self, name, value):
        """
        slot function called when a property widget has changed.

        Args:
            name (str): property name.
            value (object): new value.
        """
        self.property_changed.emit(self.__node_id, name, value)

    # pylint: disable=R0912
    def _read_node(self, node):
        """
        Populate widget from a node.

        Args:
            node (NodeGraphQtCore.Qt.BaseNode): node class.

        Returns:
            _PortConnectionsContainer: ports container widget.
        """
        model = node.model
        graph_model = node.graph.model

        common_props = graph_model.get_node_common_properties(node.type_)

        # sort tabs and properties.
        tab_mapping = defaultdict(list)
        for prop_name, prop_val in model.custom_properties.items():
            tab_name = model.get_tab_name(prop_name)
            tab_mapping[tab_name].append((prop_name, prop_val))

        # add tabs.
        reserved_tabs = [
            "Description",
            "Inputs",
            "Outputs",
            "MetaData",
            "Node",
            "Ports",
        ]
        for tab in sorted(tab_mapping.keys()):
            if tab in reserved_tabs:
                print(
                    'tab name "{}" is reserved by the "NodePropWidget" '
                    "please use a different tab name."
                )
                continue
            self.add_tab(tab)

        # property widget factory.
        widget_factory = NodePropertyWidgetFactory()

        # populate tab properties.
        for tab in sorted(tab_mapping.keys()):
            prop_window = self.__tab_windows[tab]
            for prop_name, value in tab_mapping[tab]:
                wid_type = model.get_widget_type(prop_name)
                if wid_type == 0:
                    continue

                widget = widget_factory.get_widget(wid_type)
                widget.set_name(prop_name)

                tooltip = None
                if prop_name in common_props.keys():
                    if "items" in common_props[prop_name].keys():
                        widget.set_items(common_props[prop_name]["items"])
                    if "range" in common_props[prop_name].keys():
                        prop_range = common_props[prop_name]["range"]
                        widget.set_min(prop_range[0])
                        widget.set_max(prop_range[1])
                    if "tooltip" in common_props[prop_name].keys():
                        tooltip = common_props[prop_name]["tooltip"]
                prop_window.add_widget(
                    name=prop_name,
                    widget=widget,
                    value=value,
                    label=prop_name.replace("_", " "),
                    tooltip=tooltip,
                )
                widget.value_changed.connect(self._on_property_changed)

        # Flowpipe patch
        if hasattr(node, "fp_node"):
            self.__tab.addTab(
                DescriptionWidget(flowpipe_node=node.fp_node, parent=self),
                "Description",
            )
            self.__tab.addTab(
                AttributesWidget(plugs=node.fp_node.inputs, parent=self),
                "Inputs",
            )
            self.__tab.addTab(
                AttributesWidget(plugs=node.fp_node.outputs, parent=self),
                "Outputs",
            )
            self.__tab.addTab(
                MetadataWidget(metadata=node.fp_node.metadata, parent=self),
                "MetaData",
            )

        # add "Node" tab properties. (default props)
        self.add_tab("Node")
        default_props = {
            "color": "Node base color.",
            "text_color": "Node text color.",
            "border_color": "Node border color.",
            "disabled": "Disable/Enable node state.",
            "id": "Unique identifier string to the node.",
        }
        prop_window = self.__tab_windows["Node"]
        for prop_name, tooltip in default_props.items():
            wid_type = model.get_widget_type(prop_name)
            widget = widget_factory.get_widget(wid_type)
            widget.set_name(prop_name)
            prop_window.add_widget(
                name=prop_name,
                widget=widget,
                value=model.get_property(prop_name),
                label=prop_name.replace("_", " "),
                tooltip=tooltip,
            )

            widget.value_changed.connect(self._on_property_changed)

        self.type_wgt.setText(model.get_property("type_") or "")

        # add "ports" tab connections.
        ports_container = None
        if node.inputs() or node.outputs():
            ports_container = _PortConnectionsContainer(self, node=node)
            self.__tab.addTab(ports_container, "Ports")

        return ports_container

    def node_id(self):
        """
        Returns the node id linked to the widget.

        Returns:
            str: node id
        """
        return self.__node_id

    def add_widget(self, name, widget, tab="Properties"):
        """
        add new node property widget.

        Args:
            name (str): property name.
            widget (BaseProperty): property widget.
            tab (str): tab name.
        """
        if tab not in self._widgets.keys():
            tab = "Properties"
        window = self.__tab_windows[tab]
        window.add_widget(name, widget)
        widget.value_changed.connect(self._on_property_changed)

    def add_tab(self, name):
        """
        add a new tab.

        Args:
            name (str): tab name.

        Returns:
            PropListWidget: tab child widget.
        """
        if name in self.__tab_windows:
            raise AssertionError(f"Tab name {name} already taken!")
        self.__tab_windows[name] = _PropertiesContainer(self)
        self.__tab.addTab(self.__tab_windows[name], name)
        return self.__tab_windows[name]

    def get_tab_widget(self):
        """
        Returns the underlying tab widget.

        Returns:
            QtWidgets.QTabWidget: tab widget.
        """
        return self.__tab

    def get_widget(self, name):
        """
        get property widget.

        Args:
            name (str): property name.

        Returns:
            BaseProperty: property widget.
        """
        if name == "name":
            return self.name_wgt
        for prop_win in self.__tab_windows.values():
            widget = prop_win.get_widget(name)
            if widget:
                return widget
        return None

    def get_all_property_widgets(self):
        """
        get all the node property widgets.

        Returns:
            list[BaseProperty]: property widgets.
        """
        widgets = [self.name_wgt]
        for prop_win in self.__tab_windows.values():
            for widget in prop_win.get_all_widgets().values():
                widgets.append(widget)
        return widgets

    def get_port_connection_widget(self):
        """
        Returns the ports connections container widget.

        Returns:
            _PortConnectionsContainer: port container widget.
        """
        return self._port_connections

    def set_port_lock_widgets_disabled(self, disabled=True):
        """
        Enable/Disable port lock column widgets.

        Args:
            disabled (bool): true to disable checkbox.
        """
        self._port_connections.set_lock_controls_disable(disabled)


class PropertiesBinWidget(QtWidgets.QWidget):
    """
    The :class:`NodeGraphQtCore.Qt.PropertiesBinWidget` is a list widget for displaying
    and editing a nodes properties.

    .. inheritance-diagram:: NodeGraphQtCore.Qt.PropertiesBinWidget
        :parts: 1

    .. image:: ../_images/prop_bin.png
        :width: 950px

    .. code-block:: python
        :linenos:

        from NodeGraphQt import NodeGraph, PropertiesBinWidget

        # create node graph.
        graph = NodeGraph()

        # create properties bin widget.
        properties_bin = PropertiesBinWidget(parent=None, node_graph=graph)
        properties_bin.show()

    See Also:
            :meth:`NodeGraphQtCore.Qt.BaseNode.add_custom_widget`,
            :meth:`NodeGraphQtCore.Qt.NodeObject.create_property`,
            :attr:`NodeGraphQtCore.Qt.constants.NodePropWidgetEnum`

    Args:
        parent (QtWidgets.QWidget): parent of the new widget.
        node_graph (NodeGraphQtCore.Qt.NodeGraph): node graph.
    """

    #: Signal emitted (node_id, prop_name, prop_value)
    property_changed = QtCore.Signal(str, str, object)

    def __init__(self, parent=None, node_graph=None):
        super().__init__(parent)
        self.setWindowTitle("Properties Bin")
        self._prop_list = _PropertiesList()
        self._limit = QtWidgets.QSpinBox()
        self._limit.setToolTip("Set display nodes limit.")
        self._limit.setMaximum(10)
        self._limit.setMinimum(0)
        self._limit.setValue(2)
        self._limit.valueChanged.connect(self.__on_limit_changed)
        self.resize(450, 400)

        # this attribute to block signals if for the "on_property_changed" signal
        # in case devs that don't implement the ".prop_widgets_abstract.BaseProperty"
        # widget properly to prevent an infinite loop.
        self._block_signal = False

        self._lock = False
        self._btn_lock = QtWidgets.QPushButton("Lock")
        self._btn_lock.setToolTip(
            "Lock the properties bin prevent nodes from being loaded."
        )
        self._btn_lock.clicked.connect(self.lock_bin)

        btn_clr = QtWidgets.QPushButton("Clear")
        btn_clr.setToolTip("Clear the properties bin.")
        btn_clr.clicked.connect(self.clear_bin)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setSpacing(2)
        top_layout.addWidget(self._limit)
        top_layout.addStretch(1)
        top_layout.addWidget(self._btn_lock)
        top_layout.addWidget(btn_clr)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self._prop_list, 1)

        # wire up node graph.
        node_graph.add_properties_bin(self)
        node_graph.node_selected.connect(self.add_node)
        node_graph.nodes_deleted.connect(self.__on_nodes_deleted)
        node_graph.property_changed.connect(self.__on_graph_property_changed)

        apply_dark_theme(self)

    def __repr__(self):
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"

    def __on_port_tree_visible_changed(self, node_id, visible, tree_widget):
        """
        Triggered when the visibility of the port tree widget changes we
        resize the property list table row.

        Args:
            node_id (str): node id.
            visible (bool): visibility state.
            tree_widget (QtWidgets.QTreeWidget): ports tree widget.
        """
        items = self._prop_list.findItems(node_id, QtCore.Qt.MatchExactly)
        if items:
            tree_widget.setVisible(visible)
            widget = self._prop_list.cellWidget(items[0].row(), 0)
            widget.adjustSize()
            QtCompat.QHeaderView.setSectionResizeMode(
                self._prop_list.verticalHeader(),
                QtWidgets.QHeaderView.ResizeToContents,
            )

    def __on_prop_close(self, node_id):
        """
        Triggered when a node property widget is requested to be removed from
        the property list widget.

        Args:
            node_id (str): node id.
        """
        items = self._prop_list.findItems(node_id, QtCore.Qt.MatchExactly)
        for i in items:
            self._prop_list.removeRow(i.row())

    def __on_limit_changed(self, value):
        """
        Sets the property list widget limit.

        Args:
            value (int): limit value.
        """
        rows = self._prop_list.rowCount()
        if rows > value:
            self._prop_list.removeRow(rows - 1)

    def __on_nodes_deleted(self, nodes):
        """
        Slot function when a node has been deleted.

        Args:
            nodes (list[str]): list of node ids.
        """
        for n in nodes:
            self.__on_prop_close(n)

    def __on_graph_property_changed(self, node, prop_name, prop_value):
        """
        Slot function that updates the property bin from the node graph signal.

        Args:
            node (NodeGraphQtCore.Qt.NodeObject):
            prop_name (str): node property name.
            prop_value (object): node property value.
        """
        properties_widget = self.get_property_editor_widget(node)
        if not properties_widget:
            return

        property_widget = properties_widget.get_widget(prop_name)

        if property_widget and prop_value != property_widget.get_value():
            self._block_signal = True
            property_widget.set_value(prop_value)
            self._block_signal = False

    def __on_property_widget_changed(self, node_id, prop_name, prop_value):
        """
        Slot function triggered when a property widget value has changed.

        Args:
            node_id (str): node id.
            prop_name (str): node property name.
            prop_value (object): node property value.
        """
        if not self._block_signal:
            self.property_changed.emit(node_id, prop_name, prop_value)

    def create_property_editor(self, node):
        """
        Creates a new property editor widget from the provided node.

        (re-implement for displaying custom node property editor widget.)

        Args:
            node (NodeGraphQtCore.Qt.NodeObject): node object.

        Returns:
            NodePropEditorWidget: property editor widget.
        """
        return FlowpipeNodePropEditorWidget(node=node)

    def limit(self):
        """
        Returns the limit for how many nodes can be loaded into the bin.

        Returns:
            int: node limit.
        """
        return int(self._limit.value())

    def set_limit(self, limit):
        """
        Set limit of nodes to display.

        Args:
            limit (int): node limit.
        """
        self._limit.setValue(limit)

    def add_node(self, node):
        """
        Add node to the properties bin.

        Args:
            node (NodeGraphQtCore.Qt.NodeObject): node object.
        """
        if self.limit() == 0 or self._lock:
            return

        itm_find = self._prop_list.findItems(node.id, QtCore.Qt.MatchExactly)
        if itm_find:
            self._prop_list.removeRow(itm_find[0].row())

        self._prop_list.insertRow(0)
        rows = self._prop_list.rowCount() - 1

        if rows >= (self.limit()):
            self._prop_list.removeRow(rows)

        prop_widget = self.create_property_editor(node=node)
        prop_widget.property_closed.connect(self.__on_prop_close)
        prop_widget.property_changed.connect(self.__on_property_widget_changed)
        port_connections = prop_widget.get_port_connection_widget()
        if port_connections:
            port_connections.input_group.clicked.connect(
                lambda v: self.__on_port_tree_visible_changed(
                    prop_widget.node_id(), v, port_connections.input_tree
                )
            )
            port_connections.output_group.clicked.connect(
                lambda v: self.__on_port_tree_visible_changed(
                    prop_widget.node_id(), v, port_connections.output_tree
                )
            )

        self._prop_list.setCellWidget(0, 0, prop_widget)

        item = QtWidgets.QTableWidgetItem(node.id)
        self._prop_list.setItem(0, 0, item)
        self._prop_list.selectRow(0)

    def remove_node(self, node):
        """
        Remove node from the properties bin.

        Args:
            node (str or NodeGraphQtCore.Qt.BaseNode): node id or node object.
        """
        node_id = node if isinstance(node, str) else node.id
        self.__on_prop_close(node_id)

    def lock_bin(self):
        """
        Lock/UnLock the properties bin.
        """
        self._lock = not self._lock
        if self._lock:
            self._btn_lock.setText("UnLock")
        else:
            self._btn_lock.setText("Lock")

    def clear_bin(self):
        """
        Clear the properties bin.
        """
        self._prop_list.setRowCount(0)

    def get_property_editor_widget(self, node):
        """
        Returns the node property editor widget.

        Args:
            node (str or NodeGraphQtCore.Qt.NodeObject): node id or node object.

        Returns:
            NodePropEditorWidget: node property editor widget.
        """
        node_id = node if isinstance(node, str) else node.id
        itm_find = self._prop_list.findItems(node_id, QtCore.Qt.MatchExactly)
        if itm_find:
            item = itm_find[0]
            return self._prop_list.cellWidget(item.row(), 0)
        return None
