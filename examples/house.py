import sys
from pathlib import Path

from flowpipe import Graph, INode, InputPlug, Node, OutputPlug
from Qt import QtGui, QtWidgets

from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

BASE_PATH = Path(__file__).parent.parent.resolve()

class HireWorkers(INode):
    """A node can be derived from the INode interface.

    The plugs are defined in the init method.
    The compute method received the inputs from any connected upstream nodes.
    """

    def __init__(self, amount=None, **kwargs):
        super(HireWorkers, self).__init__(**kwargs)
        InputPlug("amount", self, amount)
        OutputPlug("workers", self)

    def compute(self, amount):
        workers = ["John", "Jane", "Mike", "Michelle"]
        print("{0} workers are hired to build the house.".format(amount))
        return {"workers.{0}".format(i): workers[i] for i in range(amount)}


@Node(outputs=["workers"])
def Build(workers, section):
    """A node can also be created by the Node decorator.outputs

    The inputs to the function are turned into InputsPlugs, outputs are defined
    in the decorator itself.
    The wrapped function is used as the compute method.
    """
    print(
        "{0} are building the {1}".format(", ".join(workers.values()), section)
    )
    return {"workers.{0}".format(i): worker for i, worker in workers.items()}


@Node()
def Party(attendees):
    """Nodes do not necessarily need to have output or input plugs."""
    print(
        "{0} and {1} are having a great party!".format(
            ", ".join(list(attendees.values())[:-1]),
            list(attendees.values())[-1],
        )
    )

if __name__ == "__main__":
    graph = Graph(name="Build a House")
    workers = HireWorkers(graph=graph, amount=4)
    build_walls = Build(graph=graph, name="Build Walls", section="walls")
    build_roof = Build(graph=graph, name="Build Roof", section="roof")
    party = Party(graph=graph, name="Housewarming Party")

    # Nodes are connected via their input/output plugs.
    workers.outputs["workers"]["0"].connect(build_walls.inputs["workers"]["0"])
    workers.outputs["workers"]["1"].connect(build_walls.inputs["workers"]["1"])
    workers.outputs["workers"]["2"].connect(build_roof.inputs["workers"]["0"])
    workers.outputs["workers"]["3"].connect(build_roof.inputs["workers"]["1"])

    # Connecting nodes can be done via the bit shift operator as well
    build_walls.outputs["workers"]["0"] >> party.inputs["attendees"]["0"]
    build_walls.outputs["workers"]["1"] >> party.inputs["attendees"]["2"]
    build_roof.outputs["workers"]["0"] >> party.inputs["attendees"]["1"]
    build_roof.outputs["workers"]["1"] >> party.inputs["attendees"]["3"]

    # Initial values can be set onto the input plugs for initialization
    party.inputs["attendees"]["4"].value = "Homeowner"

    # Display the graph
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(Path(BASE_PATH, 'flowpipe_editor', 'icons', 'flowpipe.png'))))

    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor House And Birthday Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(parent=window)
    flowpipe_editor_widget.load_graph(graph)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(flowpipe_editor_widget)
    window.setLayout(layout)

    window.show()

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())