import sys
from pathlib import Path

from flowpipe import Graph, Node
from Qt import QtGui, QtWidgets

from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

BASE_PATH = Path(__file__).parent.parent.resolve()

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
    graph = Graph(name="Celebrate a Birthday Party")

    @Node(outputs=["people"])
    def InvitePeople(amount):
        people = ["John", "Jane", "Mike", "Michelle"]
        d = {"people.{0}".format(i): people[i] for i in range(amount)}
        d["people"] = {people[i]: people[i] for i in range(amount)}
        return d

    invite = InvitePeople(graph=graph, amount=4)
    birthday_party = Party(graph=graph, name="Birthday Party")
    invite.outputs["people"] >> birthday_party.inputs["attendees"]

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

    sys.exit(app.exec())