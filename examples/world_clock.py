import sys
from datetime import datetime
from time import time
from pathlib import Path

from flowpipe import Graph, INode, InputPlug, Node, OutputPlug
from Qt import QtGui,QtWidgets

from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

BASE_PATH = Path(__file__).parent.parent.resolve()

@Node(outputs=["time"])
def CurrentTime():
    """The @Node decorator turns the wrapped function into a Node object.

    Any arguments to the function are used as input plugs to the Node.
    The outputs are defined in the decorator explicitely.
    """
    return {"time": time()}

class ConvertTime(INode):
    """A node can be derived from the INode interface.

    The plugs are defined in the init method.
    The compute method received the inputs from any connected upstream nodes.
    """

    def __init__(self, time=None, timezone=0, **kwargs):
        super(ConvertTime, self).__init__(**kwargs)
        InputPlug("time", self)
        InputPlug("timezone", self, timezone)
        OutputPlug("converted_time", self)

    def compute(self, time, timezone):
        return {"converted_time": time + timezone * 60 * 60}

@Node()
def ShowTimes(times):
    """Nodes do not necessarily have to define output and input plugs."""
    print("-- World Clock -------------------")
    for location, t in times.items():
        print(
            "It is now: {time:%H:%M} in {location}".format(
                time=datetime.fromtimestamp(t), location=location
            )
        )
    print("----------------------------------")

if __name__ == "__main__":
    # The Graph holds the nodes
    graph = Graph(name="World Clock")
    current_time = CurrentTime(graph=graph)
    van = ConvertTime(name="Vancouver", timezone=-8, graph=graph)
    ldn = ConvertTime(name="London", timezone=0, graph=graph)
    muc = ConvertTime(name="Munich", timezone=1, graph=graph)
    world_clock = ShowTimes(graph=graph)

    # Connecting nodes can be done via the bit shift operator as well
    current_time.outputs["time"].connect(van.inputs["time"])
    current_time.outputs["time"].connect(ldn.inputs["time"])
    current_time.outputs["time"].connect(muc.inputs["time"])
    van.outputs["converted_time"] >> world_clock.inputs["times"]["Vancouver"]
    ldn.outputs["converted_time"] >> world_clock.inputs["times"]["London"]
    muc.outputs["converted_time"] >> world_clock.inputs["times"]["Munich"]

    # Display the graph
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(Path(BASE_PATH, 'flowpipe_editor', 'icons', 'flowpipe.png'))))

    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor World Clock Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(parent=window)
    flowpipe_editor_widget.load_graph(graph)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(flowpipe_editor_widget)
    window.setLayout(layout)

    window.show()

    sys.exit(app.exec())