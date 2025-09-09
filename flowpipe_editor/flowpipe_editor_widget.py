"""Class that provides the Qt Widget."""

from pathlib import Path

from flowpipe import Graph, INode
from NodeGraphQt import BaseNode, NodeGraph

# pylint: disable=no-name-in-module
from Qt import QtCore, QtWidgets

from flowpipe_editor.widgets.dark_theme import apply_dark_theme
from flowpipe_editor.widgets.properties_bin.node_property_widgets import (
    PropertiesBinWidget,
)

BASE_PATH = Path(__file__).parent.resolve()
ICONS_PATH = Path(BASE_PATH, "icons")


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

    def __init__(
        self,
        expanded_properties: bool = False,
        parent: QtWidgets.QWidget = None,
    ):
        """Initialize the Flowpipe editor widget.

        Args:
            expanded_properties (bool, optional): Whether to expand the properties
                                                    bin initially. Defaults to False.
            parent (QtWidgets.QWidget, optional): Parent Qt Widget. Defaults to None.
        """
        super().__init__(parent)

        self.setLayout(QtWidgets.QHBoxLayout(self))

        # Create a horizontal splitter (left/right layout)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, parent=self)

        self.layout().setContentsMargins(0, 0, 0, 0)

        self.graph = NodeGraph(parent=self)
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
        if not expanded_properties:
            self.collapse_properties_bin()
        else:
            self.expand_properties_bin()

        # wire function to "node_double_clicked" signal.
        self.graph.node_selected.connect(self.expand_properties_bin)

        # get the main context menu.
        context_menu = self.graph.get_context_menu("graph")

        # add a layout menu
        layout_menu = context_menu.add_menu("Layout")
        layout_menu.add_command(
            "Horizontal", self.layout_graph_down, "Shift+1"
        )
        layout_menu.add_command("Vertical", self.layout_graph_up, "Shift+2")
        apply_dark_theme(self)

    def collapse_properties_bin(self):
        """Collapse the properties bin to show node properties."""
        self.splitter.setSizes([1, 0])

    def expand_properties_bin(self):
        """Expand the properties bin to show node properties."""
        if self.splitter.sizes()[1] == 0:
            self.splitter.setSizes([700, 10])

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

    def _add_node(self, fp_node: INode, point: QtCore.QPoint) -> BaseNode:
        """Helper function to add a Flowpipe node to the graph.

        Args:
            fp_node (INode): Flowpipe node to add
            point (QtCore.QPoint): Position to place the node in the graph
        Returns:
            BaseNode: The created NodegraphQT Node instance
        """
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
            icon_path = Path(ICONS_PATH, f"{interpreter}.png")
            if icon_path.exists():
                qt_node.set_icon(str(icon_path))
            elif interpreter:
                qt_node.set_icon(
                    str(Path(Path(BASE_PATH, "icons"), "python.png"))
                )
        else:
            qt_node.set_icon(str(Path(Path(BASE_PATH, "icons"), "python.png")))

        for input_ in fp_node.all_inputs().values():
            qt_node.add_input(input_.name)
        for output in fp_node.all_outputs().values():
            qt_node.add_output(output.name)

        self.graph.clear_selection()

        return qt_node

    def load_graph(self, graph: Graph):
        """Load a Flowpipe graph into the editor widget.

        Args:
            graph (Graph): Flowpipe graph to load
        """
        self.clear()
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
        self.graph.center_on(nodes=nodes)
        self.graph.fit_to_selection()

def toggle_node_search(graph):
    """
    show/hide the node search widget.
    """
    graph.toggle_node_search()
