"""Class that provides the Qt Widget."""

from pathlib import Path

from flowpipe import Graph
from NodeGraphQt import BaseNode, NodeGraph

# pylint: disable=no-name-in-module
from Qt import QtCore, QtWidgets

from flowpipe_editor.widgets.dark_theme import apply_dark_theme
from flowpipe_editor.widgets.properties_bin.node_property_widgets import (
    PropertiesBinWidget,
)

BASE_PATH = Path(__file__).parent.resolve()


class FlowpipeNode(BaseNode):
    """Flowpipe node for NodeGraphQt."""

    __identifier__ = "flowpipe"
    NODE_NAME = "FlowpipeNode"

    def __init__(self, **kwargs):
        """Initialize the FlowpipeNode."""
        super().__init__(**kwargs)
        self.fp_node = None


class FlowpipeEditorWidget(QtWidgets.QWidget):
    """Flowpipe editor widget for visualize flowpipe graphs."""

    def __init__(self, parent: QtWidgets.QWidget = None):
        """Initialize the Flowpipe editor widget.

        Args:
            parent (QtWidgets.QWidget, optional): Parent Qt Widget. Defaults to None.
        """
        super().__init__(parent)

        # apply_dark_theme(properties_bin)
        self.setLayout(QtWidgets.QHBoxLayout(self))

        # Create a horizontal splitter (left/right layout)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, parent=self)

        self.layout().setContentsMargins(0, 0, 0, 0)

        self.graph = NodeGraph()
        self.flowpipe_graph = None
        self.graph.register_node(FlowpipeNode)

        self.splitter.addWidget(self.graph.widget)

        self.layout().addWidget(self.splitter)

        # create a node properties bin widget.
        properties_bin = PropertiesBinWidget(
            parent=self, node_graph=self.graph
        )

        properties_bin.setAutoFillBackground(True)
        self.splitter.addWidget(properties_bin)

        # hide initially
        self.splitter.setSizes([1, 0])

        # example show the node properties bin widget when a node is double-clicked.
        def display_properties_bin():
            if self.splitter.sizes()[1] == 0:
                self.splitter.setSizes([700, 10])

        # wire function to "node_double_clicked" signal.
        self.graph.node_selected.connect(display_properties_bin)

        # get the main context menu.
        context_menu = self.graph.get_context_menu("graph")

        # add a layout menu
        layout_menu = context_menu.add_menu("Layout")
        layout_menu.add_command(
            "Horizontal", self.layout_graph_down, "Shift+1"
        )
        layout_menu.add_command("Vertical", self.layout_graph_up, "Shift+2")
        apply_dark_theme(self)

    def layout_graph_down(self):
        """
        Auto layout the nodes down stream.
        """
        nodes = self.graph.selected_nodes() or self.graph.all_nodes()
        self.graph.auto_layout_nodes(nodes=nodes, down_stream=True)

    def layout_graph_up(self):
        """
        Auto layout the nodes up stream.
        """
        nodes = self.graph.selected_nodes() or self.graph.all_nodes()
        self.graph.auto_layout_nodes(nodes=nodes, down_stream=False)

    def clear(self):
        """Clear the graph and reset the flowpipe graph."""
        self.flowpipe_graph = Graph()
        self.graph.clear_session()
        self.node_deselected()

    def _add_node(self, fp_node, point):
        """Helper function to add a Flowpipe node to the graph."""
        qt_node = self.graph.create_node(
            "flowpipe.FlowpipeNode",
            name=fp_node.name,
            pos=[point.x(), point.y()],
        )
        qt_node.fp_node = fp_node
        interpreter = (
            fp_node.metadata.get("interpreter") if fp_node.metadata else None
        )

        # set icon based on interpreter
        if interpreter:
            icon_path = Path(BASE_PATH, "icons", f"{interpreter}.png")
            if icon_path.exists():
                qt_node.set_icon(str(icon_path))
            elif interpreter:
                qt_node.set_icon(str(Path(BASE_PATH, "icons", "python.png")))
        else:
            qt_node.set_icon(str(Path(BASE_PATH, "icons", "python.png")))

        for input_ in fp_node.all_inputs().values():
            qt_node.add_input(input_.name)
        for output in fp_node.all_outputs().values():
            qt_node.add_output(output.name)

        self.graph.clear_selection()

        return qt_node

    def load_graph(self, graph: Graph):
        """Load a Flowpipe graph into the editor widget.

        Args:
            graph (Graph): Flowpipe graph to load.
        """
        self.flowpipe_graph = graph
        x_pos = 0
        for row in graph.evaluation_matrix:
            y_pos = 0
            x_diff = 250
            for fp_node in row:
                self._add_node(fp_node, QtCore.QPoint(int(x_pos), int(y_pos)))
                y_pos += 150
            x_pos += x_diff
        for fp_node in graph.all_nodes:
            for i, output in enumerate(fp_node.all_outputs().values()):
                for connection in output.connections:
                    in_index = list(
                        connection.node.all_inputs().values()
                    ).index(connection)
                    self.graph.get_node_by_name(fp_node.name).set_output(
                        i,
                        self.graph.get_node_by_name(
                            connection.node.name
                        ).input(in_index),
                    )

        nodes = self.graph.all_nodes()
        self.graph.auto_layout_nodes(nodes=nodes, down_stream=True)
