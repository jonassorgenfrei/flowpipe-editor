from __future__ import annotations

import logging
import os
import webbrowser

from flowpipe.graph import Graph
from NodeGraphQt import BaseNode, NodeGraph
from Qt import QtCore, QtWidgets
from qt_json_view import model

from . import flowpipe_editor_ui
# todo implement
from .import getQtParent
from . import dedent_doc

log = logging.getLogger(__name__)


class FlowpipeNode(BaseNode):
    __identifier__ = "flowpipe"
    NODE_NAME = "FlowpipeNode"


class FlowpipeEditor(QtWidgets.QMainWindow, flowpipe_editor_ui.Ui_FlowpipeEditorWindow):
    INSTANCE = None

    def __init__(self, allow_submission=False, parent=None):
        """Opens a QT Widget showing a flowpipe graph

        Args:
            allow_submission (bool, optional): If set to true it shows the submission panel. Defaults to False.
            parent (QtWidget, optional): Parent Widet. Defaults to None.
        """
        super(FlowpipeEditor, self).__init__(parent=parent)
        self.setupUi(self)

        self.qt_graph = NodeGraph()
        self.qt_graph.register_node(FlowpipeNode)

        self.graph_name_lineedit.setPlaceholderText("<Workflow Name>")

        self.fp_nodes_map = {}
        self.qt_nodes_map = {}
        self.logs = {}
        self.graph = None
        self.selected_fp_node = None
        self.workflow = None
        self.loaded_workflow = None
        self.graph_viewer = self.qt_graph.viewer()
        self.graph_widget.layout().addWidget(self.graph_viewer)
        self.graph_name_lineedit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.submit_to_farm_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.evaluate_locally_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.metadata_model = model.JsonModel()
        self.metadata_view.setModel(self.metadata_model)

        self.evaluation_dock.setEnabled(allow_submission)

        # get the main context menu.
        context_menu = self.qt_graph.get_context_menu("graph")

        # add a layout menu
        layout_menu = context_menu.add_menu("Layout")
        layout_menu.add_command("Horizontal", self.layout_graph_down, "Shift+1")
        layout_menu.add_command("Vertical", self.layout_graph_up, "Shift+2")

        self.connectSignals()
        self.new()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            self.qt_graph.toggle_node_search()
            # If you want to prevent the focus change, you can accept the event
            event.accept()
        elif event.key() == QtCore.Qt.Key_Delete:
            self.qt_graph.delete_nodes(self.qt_graph.selected_nodes())
            event.accept()
        else:
            super().keyPressEvent(event)

    def layout_graph_down(self):
        """
        Auto layout the nodes down stream.
        """
        nodes = self.qt_graph.selected_nodes() or self.qt_graph.all_nodes()
        self.qt_graph.auto_layout_nodes(nodes=nodes, down_stream=True)

    def layout_graph_up(self):
        """
        Auto layout the nodes up stream.
        """
        nodes = self.qt_graph.selected_nodes() or self.qt_graph.all_nodes()
        self.qt_graph.auto_layout_nodes(nodes=nodes, down_stream=False)

    def connectSignals(self):
        """Setup all widget signals."""
        self.open_code_button.clicked.connect(self.open_code)
        self.graph_viewer.node_selection_changed.connect(self.node_selection_changed)

    def disconnectSignals(self):
        """Teardown and remove all widget signals."""
        self.open_code_button.clicked.disconnect(self.open_code)
        self.graph_viewer.node_selection_changed.disconnect(self.node_selection_changed)

    def new(self):
        self.fp_nodes_map = {}
        self.qt_nodes_map = {}
        self.graph = Graph()
        self.qt_graph.clear_session()
        self.node_deselected()

    def open_code(self):
        webbrowser.open(self.selected_fp_node.file_location)

    def _add_node(self, fp_node, point):
        qt_node = self.qt_graph.create_node(
            "flowpipe.FlowpipeNode", name=fp_node.name, pos=[point.x(), point.y()]
        )
        for input_ in fp_node.all_inputs().values():
            qt_node.add_input(input_.name)
        for output in fp_node.all_outputs().values():
            qt_node.add_output(output.name)
        self.fp_nodes_map[qt_node.id] = fp_node
        self.qt_nodes_map[qt_node.id] = qt_node
        self.qt_graph.clear_selection()
        return qt_node

    def node_selection_changed(self, selected, deselected):
        selection = self.graph_viewer.selected_nodes()
        if len(selection) == 1:
            self.node_selected(selection[0].id)
        else:
            self.node_deselected()

    def node_selected(self, qt_node_id):
        fp_node = self.fp_nodes_map[qt_node_id]
        self.selected_fp_node = fp_node
        self.refresh_node_attributes()

    def refresh_node_attributes(self):
        if self.selected_fp_node is None:
            self.node_deselected()
            return

        self.node_name_widget.setEnabled(True)
        self.node_inputs_widget.setEnabled(True)
        self.node_outputs_widget.setEnabled(True)
        self.node_metadata_widget.setEnabled(True)
        self.open_code_button.setEnabled(
            os.path.isfile(self.selected_fp_node.file_location)
        )

        self.name_lineedit.setText(self.selected_fp_node.name)
        self.node_type_label.setText(self.selected_fp_node.__class__.__name__)
        self.description_textedit.setPlainText(
            dedent_doc(self.selected_fp_node.__doc__)
        )

        inputs = {}
        for name, in_ in self.selected_fp_node.inputs.items():
            if in_._sub_plugs:
                inputs[name] = {}
                for sub_name, sub_plug in in_._sub_plugs.items():
                    inputs[name][sub_name] = sub_plug
            else:
                inputs[name] = in_

        outputs = {}
        for name, out in self.selected_fp_node.outputs.items():
            if out._sub_plugs:
                outputs[name] = {}
                for sub_name, sub_plug in out._sub_plugs.items():
                    outputs[name][sub_name] = sub_plug
            else:
                outputs[name] = out
        self.metadata_model.init(
            self.selected_fp_node.metadata or {}, editable_values=False
        )

        self.description_textedit.setStyleSheet("background-color: palette(window)")
        self.description_textedit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        self.node_inputs_widget.initialize(plugs=self.selected_fp_node.inputs)
        self.node_outputs_widget.initialize(plugs=self.selected_fp_node.outputs)

    def node_deselected(self):
        self.selected_fp_node = None
        self.name_lineedit.clear()
        self.node_type_label.clear()
        self.description_textedit.clear()
        self.node_inputs_widget.initialize(plugs={})
        self.node_outputs_widget.initialize(plugs={})
        self.node_name_widget.setEnabled(False)
        self.node_inputs_widget.setEnabled(False)
        self.node_outputs_widget.setEnabled(False)
        self.node_metadata_widget.setEnabled(False)

    def load_graph(self, graph):
        self.new()
        self.graph = graph
        self.graph_name_lineedit.setText(graph.name)
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
                    self.qt_graph.get_node_by_name(fp_node.name).set_output(
                        i,
                        self.qt_graph.get_node_by_name(connection.node.name).input(
                            in_index
                        ),
                    )

        nodes = self.qt_graph.all_nodes()
        self.qt_graph.auto_layout_nodes(nodes=nodes, down_stream=True)



def visualize(graph, allow_submission=False):
    """Load the given `flowpipe.Graph` in the FlowpipeEditor.
    If an Qt App instance is already running this returns the widget.

    Args:
        graph (lowpipe.graph.Graph): A flowpipe graph to display and/or submit.
        allow_submission (bool, optional): Flag if the ui should allow submission of the graph. Defaults to False.

    Returns:
        widget (QWidget): The editor widget.
    """
    open_app = False
    if not QtWidgets.QApplication.instance():
        open_app = True
        app = QtWidgets.QApplication([])

    if FlowpipeEditor.INSTANCE is None:
        FlowpipeEditor.INSTANCE = FlowpipeEditor(
            allow_submission=allow_submission, parent=getQtParent()
        )
    FlowpipeEditor.INSTANCE.load_graph(graph)
    FlowpipeEditor.INSTANCE.show()

    if open_app:
        app.exec_()
    else:
        return FlowpipeEditor.INSTANCE
