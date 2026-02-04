"""Class that provides the Qt Widget."""

from pathlib import Path

from flowpipe import Graph, INode
from flowpipe.plug import InputPlugGroup
from NodeGraphQt import BaseNode, GroupNode, NodeGraph
from NodeGraphQt.constants import NodePropWidgetEnum

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
        self.set_port_deletion_allowed(True)
        self.fp_node = None
        if not self.has_property("fp_identifier"):
            self.create_property(
                "fp_identifier", "", widget_type=NodePropWidgetEnum.HIDDEN
            )


class FlowpipeGroupNode(GroupNode):
    """Group node that can re-hydrate Flowpipe nodes on expand."""

    __identifier__ = "flowpipe"
    NODE_NAME = "FlowpipeGroup"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._expand_callback = None
        self.fp_graph = None

    def set_expand_callback(self, callback):
        """Set a callback that receives the expanded subgraph."""
        self._expand_callback = callback

    def expand(self):
        sub_graph = super().expand()
        if self._expand_callback:
            self._expand_callback(sub_graph)
        return sub_graph


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
        self._fp_nodes_by_id = {}
        self._graph_input_targets = {}
        self._graph_output_sources = {}
        self.graph.register_node(FlowpipeNode)
        self.graph.register_node(GroupNode)
        self.graph.register_node(FlowpipeGroupNode)

        self.splitter.addWidget(self.graph.widget)

        self.layout().addWidget(self.splitter)

        # create a node properties bin widget.
        self.properties_bin = PropertiesBinWidget(
            parent=self, node_graph=self.graph
        )

        self.properties_bin.setAutoFillBackground(True)
        self.splitter.addWidget(self.properties_bin)

        # hide initially
        if not expanded_properties:
            self.collapse_properties_bin()
        else:
            self.expand_properties_bin()

        # wire function to "node_double_clicked" signal.
        self.graph.node_selected.connect(self.expand_properties_bin)

        # get the main context menu.
        context_menu = self.graph.get_context_menu("graph")
        
        context_menu.add_command(
            "Expand Group Node", self.expand_group_node, "Alt+Enter"
        )
        
        # add a layout menu
        layout_menu = context_menu.add_menu("Layout")
        layout_menu.add_command(
            "Horizontal", self.layout_graph_down, "Shift+1"
        )
        layout_menu.add_command("Vertical", self.layout_graph_up, "Shift+2")
        
        apply_dark_theme(self)

    def expand_group_node(self):
        """
        Expand selected group node.
        """
        selected_nodes = self.graph.selected_nodes()
        if not selected_nodes:
            self.graph.message_dialog('Please select a "GroupNode" to expand.')
            return
        node = selected_nodes[0]
        if isinstance(node, FlowpipeGroupNode):
            node.expand()
        else:
            self.graph.expand_group_node(node)

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
        self._fp_nodes_by_id = {}
        self._graph_input_targets = {}
        self._graph_output_sources = {}
        self.graph.clear_session()

    def _add_node(
        self,
        fp_node: INode,
        point: QtCore.QPoint,
        node_graph: NodeGraph = None,
    ) -> BaseNode:
        """Helper function to add a Flowpipe node to the graph.

        Args:
            fp_node (INode): Flowpipe node to add
            point (QtCore.QPoint): Position to place the node in the graph
            node_graph (NodeGraph, optional): NodeGraphQt graph to add node to
        Returns:
            BaseNode: The created NodegraphQT Node instance
        """
        node_graph = node_graph or self.graph
        qt_node = node_graph.create_node(
            "flowpipe.FlowpipeNode",
            name=fp_node.name,
            pos=[point.x(), point.y()],
        )
        qt_node.fp_node = fp_node
        if qt_node.has_property("fp_identifier"):
            qt_node.set_property(
                "fp_identifier", fp_node.identifier, push_undo=False
            )
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

        node_graph.clear_selection()

        return qt_node

    def _hydrate_flowpipe_nodes(self, node_graph: NodeGraph):
        """Bind Flowpipe nodes to NodeGraphQt nodes using identifiers."""
        node_map = {}
        if not self._fp_nodes_by_id:
            return node_map

        for qt_node in node_graph.all_nodes():
            if not isinstance(qt_node, FlowpipeNode):
                continue
            fp_id = None
            if qt_node.has_property("fp_identifier"):
                fp_id = qt_node.get_property("fp_identifier")
            if not fp_id:
                continue
            fp_node = self._fp_nodes_by_id.get(fp_id)
            if not fp_node:
                continue
            qt_node.fp_node = fp_node
            node_map[fp_node] = qt_node

        return node_map

    def _ensure_subgraph_connections(
        self,
        fp_graph: Graph,
        sub_graph: NodeGraph,
        node_map: dict,
    ):
        """Ensure internal and graph IO connections exist in the subgraph."""
        if not fp_graph or not sub_graph:
            return
        if node_map is None:
            node_map = {}

        input_nodes = {
            node.name(): node for node in sub_graph.get_input_port_nodes()
        }
        output_nodes = {
            node.name(): node for node in sub_graph.get_output_port_nodes()
        }

        for fp_node in fp_graph.nodes:
            src_qt_node = node_map.get(fp_node)
            if not src_qt_node:
                continue
            for output in fp_node.all_outputs().values():
                out_port = src_qt_node.outputs().get(output.name)
                if not out_port:
                    continue
                for connection in output.connections:
                    if connection.node.graph is not fp_graph:
                        continue
                    dst_qt_node = node_map.get(connection.node)
                    if not dst_qt_node:
                        continue
                    in_port = dst_qt_node.inputs().get(connection.name)
                    if not in_port:
                        continue
                    if in_port in out_port.connected_ports():
                        continue
                    out_port.connect_to(in_port)

        input_targets = self._graph_input_targets.get(fp_graph, {})
        output_sources = self._graph_output_sources.get(fp_graph, {})

        for name, target_plugs in input_targets.items():
            port_node = input_nodes.get(name)
            if not port_node:
                continue
            out_port = port_node.output(0)
            for target_plug in target_plugs:
                target_qt_node = node_map.get(target_plug.node)
                if not target_qt_node:
                    continue
                in_port = target_qt_node.inputs().get(target_plug.name)
                if not in_port:
                    continue
                if in_port in out_port.connected_ports():
                    continue
                out_port.connect_to(in_port)

        for name, plug in output_sources.items():
            port_node = output_nodes.get(name)
            if not port_node:
                continue
            source_qt_node = node_map.get(plug.node)
            if not source_qt_node:
                continue
            out_port = source_qt_node.outputs().get(plug.name)
            if not out_port:
                continue
            in_port = port_node.input(0)
            if in_port in out_port.connected_ports():
                continue
            out_port.connect_to(in_port)

    def _on_group_expanded(self, sub_graph: NodeGraph):
        """Re-hydrate Flowpipe nodes and connections after expand."""
        fp_graph = getattr(sub_graph.node, "fp_graph", None)
        node_map = self._hydrate_flowpipe_nodes(sub_graph)
        self._ensure_subgraph_connections(fp_graph, sub_graph, node_map)
        if hasattr(self, "properties_bin"):
            self.properties_bin.register_graph(sub_graph)

    @staticmethod
    def _collect_connected_graphs(graph: Graph):
        """Collect all graphs connected to the given graph (recursively)."""
        graphs = []
        seen = set()
        queue = [graph]
        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)
            graphs.append(current)
            for sub_graph in sorted(
                current.subgraphs.values(), key=lambda g: g.name
            ):
                if sub_graph not in seen:
                    queue.append(sub_graph)
        return graphs

    @staticmethod
    def _evaluation_matrix_for_nodes(nodes):
        """Return an evaluation matrix for the given nodes only."""
        nodes_set = set(nodes)
        if not nodes_set:
            return []

        parents = {
            node: {p for p in node.parents if p in nodes_set}
            for node in nodes_set
        }
        matrix = []
        sorted_nodes = set()
        next_level = {node for node in nodes_set if not parents[node]}

        while next_level:
            level = sorted(next_level, key=lambda node: node.name)
            matrix.append(level)
            sorted_nodes |= next_level

            next_level = set()
            for node in level:
                for candidate in node.children:
                    if candidate not in nodes_set or candidate in sorted_nodes:
                        continue
                    if all(
                        parent in sorted_nodes for parent in parents[candidate]
                    ):
                        next_level.add(candidate)

        remaining = nodes_set - sorted_nodes
        if remaining:
            matrix.append(sorted(remaining, key=lambda node: node.name))

        return matrix

    def load_graph(self, graph: Graph):
        """Load a Flowpipe graph into the editor widget.

        Args:
            graph (Graph): Flowpipe graph to load
        """
        self.clear()
        self.flowpipe_graph = graph
        self._fp_nodes_by_id = {
            node.identifier: node for node in graph.all_nodes
        }
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

    def load_subgraphs(self, graph: Graph):
        """Load a Flowpipe graph and its subgraphs using group nodes.

        Args:
            graph (Graph): Flowpipe graph to load
        """
        self.clear()
        self.flowpipe_graph = graph

        root_graph = graph
        graphs = self._collect_connected_graphs(graph)
        self._fp_nodes_by_id = {
            node.identifier: node for fp_graph in graphs for node in fp_graph.nodes
        }

        def unique_port_name(existing, base_name):
            name = base_name
            index = 1
            while name in existing:
                name = f"{base_name}_{index}"
                index += 1
            return name

        graph_input_port_by_plug = {}
        graph_output_port_by_plug = {}
        graph_input_targets = {}
        graph_output_sources = {}
        for fp_graph in graphs:
            input_lookup = {}
            input_targets = {}
            for name, plug in fp_graph.inputs.items():
                if isinstance(plug, InputPlugGroup):
                    input_targets[name] = list(plug.plugs)
                    for input_plug in plug.plugs:
                        input_lookup[input_plug] = name
                else:
                    input_targets[name] = [plug]
                    input_lookup[plug] = name

            output_lookup = {
                plug: name for name, plug in fp_graph.outputs.items()
            }
            output_sources = {
                name: plug for name, plug in fp_graph.outputs.items()
            }

            graph_input_port_by_plug[fp_graph] = input_lookup
            graph_output_port_by_plug[fp_graph] = output_lookup
            graph_input_targets[fp_graph] = input_targets
            graph_output_sources[fp_graph] = output_sources

        self._graph_input_targets = graph_input_targets
        self._graph_output_sources = graph_output_sources

        for fp_graph in graphs:
            for fp_node in fp_graph.nodes:
                for output in fp_node.all_outputs().values():
                    for connection in output.connections:
                        src_graph = fp_node.graph
                        dst_graph = connection.node.graph
                        if src_graph is dst_graph:
                            continue

                        if src_graph is not root_graph:
                            if (
                                output
                                not in graph_output_port_by_plug[src_graph]
                            ):
                                base = f"{output.node.name}.{output.name}"
                                port_name = unique_port_name(
                                    graph_output_sources[src_graph], base
                                )
                                graph_output_port_by_plug[src_graph][
                                    output
                                ] = port_name
                                graph_output_sources[src_graph][
                                    port_name
                                ] = output

                        if dst_graph is not root_graph:
                            if (
                                connection
                                not in graph_input_port_by_plug[dst_graph]
                            ):
                                base = (
                                    f"{connection.node.name}.{connection.name}"
                                )
                                port_name = unique_port_name(
                                    graph_input_targets[dst_graph], base
                                )
                                graph_input_port_by_plug[dst_graph][
                                    connection
                                ] = port_name
                                graph_input_targets[dst_graph].setdefault(
                                    port_name, []
                                ).append(connection)

        graph_containers = {root_graph: self.graph}
        group_nodes = {}
        group_input_ports = {}
        group_output_ports = {}

        subgraphs = [g for g in graphs if g is not root_graph]
        x_pos = 0
        x_diff = 350
        for fp_graph in subgraphs:
            group_node = self.graph.create_node(
                "flowpipe.FlowpipeGroupNode",
                name=fp_graph.name,
                pos=[x_pos, 0],
            )
            group_node.fp_graph = fp_graph
            group_node.set_expand_callback(self._on_group_expanded)
            group_nodes[fp_graph] = group_node
            for name in sorted(graph_input_targets[fp_graph].keys()):
                group_node.add_input(name)
            for name in sorted(graph_output_sources[fp_graph].keys()):
                group_node.add_output(name)

            sub_graph = group_node.expand()
            graph_containers[fp_graph] = sub_graph
            group_input_ports[fp_graph] = group_node.inputs()
            group_output_ports[fp_graph] = group_node.outputs()

            x_pos += x_diff

        node_map = {}
        for fp_graph in graphs:
            node_graph = graph_containers[fp_graph]
            x_pos = 0
            for row in self._evaluation_matrix_for_nodes(fp_graph.nodes):
                y_pos = 0
                for fp_node in row:
                    qt_node = self._add_node(
                        fp_node,
                        QtCore.QPoint(int(x_pos), int(y_pos)),
                        node_graph=node_graph,
                    )
                    node_map[fp_node] = qt_node
                    y_pos += 150
                x_pos += 250

        connected_pairs = set()
        for fp_graph in graphs:
            for fp_node in fp_graph.nodes:
                src_qt_node = node_map.get(fp_node)
                if not src_qt_node:
                    continue
                for output in fp_node.all_outputs().values():
                    out_port = src_qt_node.outputs().get(output.name)
                    if not out_port:
                        continue
                    for connection in output.connections:
                        if connection.node.graph is not fp_graph:
                            continue
                        dst_qt_node = node_map.get(connection.node)
                        if not dst_qt_node:
                            continue
                        in_port = dst_qt_node.inputs().get(connection.name)
                        if not in_port:
                            continue
                        key = (id(out_port), id(in_port))
                        if key in connected_pairs:
                            continue
                        out_port.connect_to(in_port)
                        connected_pairs.add(key)

        for fp_graph in subgraphs:
            sub_graph = graph_containers[fp_graph]
            input_nodes = {
                node.name(): node for node in sub_graph.get_input_port_nodes()
            }
            output_nodes = {
                node.name(): node for node in sub_graph.get_output_port_nodes()
            }

            for name, target_plugs in graph_input_targets[fp_graph].items():
                port_node = input_nodes.get(name)
                if not port_node:
                    continue
                for target_plug in target_plugs:
                    target_qt_node = node_map.get(target_plug.node)
                    if not target_qt_node:
                        continue
                    in_port = target_qt_node.inputs().get(target_plug.name)
                    if not in_port:
                        continue
                    out_port = port_node.output(0)
                    key = (id(out_port), id(in_port))
                    if key in connected_pairs:
                        continue
                    out_port.connect_to(in_port)
                    connected_pairs.add(key)

            for name, plug in graph_output_sources[fp_graph].items():
                port_node = output_nodes.get(name)
                if not port_node:
                    continue
                source_qt_node = node_map.get(plug.node)
                if not source_qt_node:
                    continue
                out_port = source_qt_node.outputs().get(plug.name)
                if not out_port:
                    continue
                in_port = port_node.input(0)
                key = (id(out_port), id(in_port))
                if key in connected_pairs:
                    continue
                out_port.connect_to(in_port)
                connected_pairs.add(key)

        for fp_graph in subgraphs:
            sub_graph = graph_containers[fp_graph]
            sub_graph.auto_layout_nodes(nodes=sub_graph.all_nodes())
            sub_graph.clear_selection()

        for fp_graph in subgraphs:
            group_nodes[fp_graph].collapse()

        for fp_graph in graphs:
            for fp_node in fp_graph.nodes:
                for output in fp_node.all_outputs().values():
                    for connection in output.connections:
                        src_graph = fp_node.graph
                        dst_graph = connection.node.graph
                        if src_graph is dst_graph:
                            continue

                        if src_graph is root_graph:
                            src_qt_node = node_map.get(fp_node)
                            if not src_qt_node:
                                continue
                            src_port = src_qt_node.outputs().get(output.name)
                        else:
                            port_name = graph_output_port_by_plug[
                                src_graph
                            ].get(output)
                            if not port_name:
                                continue
                            src_port = group_output_ports[src_graph].get(
                                port_name
                            )

                        if dst_graph is root_graph:
                            dst_qt_node = node_map.get(connection.node)
                            if not dst_qt_node:
                                continue
                            dst_port = dst_qt_node.inputs().get(
                                connection.name
                            )
                        else:
                            port_name = graph_input_port_by_plug[
                                dst_graph
                            ].get(connection)
                            if not port_name:
                                continue
                            dst_port = group_input_ports[dst_graph].get(
                                port_name
                            )

                        if not src_port or not dst_port:
                            continue
                        key = (id(src_port), id(dst_port))
                        if key in connected_pairs:
                            continue
                        src_port.connect_to(dst_port)
                        connected_pairs.add(key)

        nodes = self.graph.all_nodes()
        self.graph.auto_layout_nodes(nodes=nodes, down_stream=True)
        self.graph.center_on(nodes=nodes)
        self.graph.fit_to_selection()


def toggle_node_search(graph):
    """
    show/hide the node search widget.
    """
    graph.toggle_node_search()
