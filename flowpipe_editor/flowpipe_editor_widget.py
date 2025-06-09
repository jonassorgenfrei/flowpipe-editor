from Qt import QtWidgets, QtCore

from NodeGraphQt import BaseNode, NodeGraph
from flowpipe import Graph

class FlowpipeNode(BaseNode):
    __identifier__ = "flowpipe"
    NODE_NAME = "FlowpipeNode"

class FlowpipeEditorWidget(QtWidgets.QWidget):
    """Flowpipe editor widget for visualize flowpipe graphs."""
    
    def __init__(self, parent:QtWidgets.QWidget=None):
        super(FlowpipeEditorWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.graph = NodeGraph()
        self.graph.register_node(FlowpipeNode)
        self.layout().addWidget(self.graph.widget)
        
        self.fp_nodes_map = {}
        self.qt_nodes_map = {}
        
    def _add_node(self, fp_node, point):
        qt_node = self.graph.create_node(
            "flowpipe.FlowpipeNode", name=fp_node.name, pos=[point.x(), point.y()]
        )
        for input_ in fp_node.all_inputs().values():
            qt_node.add_input(input_.name)
        for output in fp_node.all_outputs().values():
            qt_node.add_output(output.name)
        self.fp_nodes_map[qt_node.id] = fp_node
        self.qt_nodes_map[qt_node.id] = qt_node
        self.graph.clear_selection()
        return qt_node
        
    def load_graph(self, graph: Graph):
        self.flowpipe_graph = graph
        print(graph.name)
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
                    in_index = list(connection.node.all_inputs().values()).index(
                        connection
                    )
                    self.graph.get_node_by_name(fp_node.name).set_output(
                        i,
                        self.graph.get_node_by_name(connection.node.name).input(
                            in_index
                        ),
                    )

        nodes = self.graph.all_nodes()
        self.graph.auto_layout_nodes(nodes=nodes, down_stream=True)