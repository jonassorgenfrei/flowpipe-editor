import getpass
import sys
from pathlib import Path

from flowpipe import Graph, Node
from Qt import QtGui, QtWidgets

from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

BASE_PATH = Path(__file__).parent.parent.resolve()

class Workflow(object):
    """Abstract base class defining a workflow, based on a flowpipe graph.

    The Workflow holds a graph and provides two ways to evaluate the graph,
    locally and remotely.
    """

    def __init__(self):
        self.graph = Graph()

    def evaluate_locally(self):
        """Evaluate the graph locally."""
        self.graph.evaluate()


class PublishWorkflow(Workflow):
    """Publish a model and add a turntable render of it to the database."""

    def __init__(self, source_file):
        super(PublishWorkflow, self).__init__()
        publish = Publish(graph=self.graph)
        message = SendMessage(graph=self.graph)
        turntable = CreateTurntable(graph=self.graph)
        update_database = UpdateDatabase(graph=self.graph)
        publish.outputs["published_file"].connect(
            turntable.inputs["alembic_cache"]
        )
        publish.outputs["published_file"].connect(
            message.inputs["values"]["path"]
        )
        turntable.outputs["turntable"].connect(
            update_database.inputs["images"]
        )

        # Initialize the graph from user input
        publish.inputs["source_file"].value = source_file

        # Initialize the graph through pipeline logic
        # These things can also be done in the nodes themselves of course,
        # it's a design choice and depends on the case
        message.inputs["template"].value = (
            "Hello,\n\n"
            "The following file has been published: {path}\n\n"
            "Thank you,\n\n"
            "{sender}"
        )
        message.inputs["values"]["sender"].value = getpass.getuser()
        message.inputs["values"]["recipients"].value = [
            "john@mail.com",
            "jane@mail.com",
        ]
        turntable.inputs["render_template"].value = "template.ma"
        update_database.inputs["asset"].value = source_file.split(".")[0]
        update_database.inputs["status"].value = "published"


# -----------------------------------------------------------------------------
#
# The Nodes used in the Graph
#
# -----------------------------------------------------------------------------


@Node(outputs=["published_file"])
def Publish(source_file):
    """Publish the given source file."""
    return {"published_file": "/published/file.abc"}


@Node(outputs=["return_status"])
def SendMessage(template, values, recipients):
    """Send message to given recipients."""
    print("--------------------------------------")
    print(template.format(**values))
    print("--------------------------------------")
    return {"return_status": 0}


@Node(outputs=["turntable"])
def CreateTurntable(alembic_cache, render_template):
    """Load the given cache into the given template file and render."""
    return {"turntable": "/turntable/turntable.%04d.jpg"}


@Node(outputs=["asset"])
def UpdateDatabase(asset, images, status):
    """Update the database entries of the given asset with the given data."""
    return {"asset": asset}


if __name__ == "__main__":
    workflow = PublishWorkflow("model.ma")
    
    # Display the graph
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(Path(BASE_PATH, 'flowpipe_editor', 'icons', 'flowpipe.png'))))
    
    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor Workflow Design Pattern Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(parent=window)
    flowpipe_editor_widget.load_graph(workflow.graph)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(flowpipe_editor_widget)
    window.setLayout(layout)

    window.show()

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())