"""Nested graphs are supported in flowpipe."""
import sys
from Qt import QtWidgets

from flowpipe import Graph, Node
from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget


@Node(outputs=["file"])
def MyNode(file):
    # Something is done in here ...
    return {"file": file}

if __name__ == "__main__":
    # A graph that fixes an incoming file, cleaning up messy names etc.
    #
    # +-----------------------+          +-------------------------+
    # |   Cleanup Filename    |          |   Change Lineendings    |
    # |-----------------------|          |-------------------------|
    # o file<>                |     +--->o file<>                  |
    # |                  file o-----+    |                    file o
    # +-----------------------+          +-------------------------+
    fix_file = Graph(name="fix_file")
    cleanup_filename = MyNode(name="Cleanup Filename", graph=fix_file)
    change_lineendings = MyNode(name="Change Lineendings", graph=fix_file)
    cleanup_filename.outputs["file"].connect(change_lineendings.inputs["file"])


    # A second graph reads finds files, and extracts their contents into a database
    # +----------------+          +----------------------------+          +----------------+
    # |   Find File    |          |   Read Values from File    |          |   Update DB    |
    # |----------------|          |----------------------------|          |----------------|
    # o file<>         |     +--->o file<>                     |     +--->o file<>         |
    # |           file o-----+    |                       file o-----+    |           file o
    # +----------------+          +----------------------------+          +----------------+
    udpate_db_from_file = Graph(name="udpate_db_from_file")
    find_file = MyNode(name="Find File", graph=udpate_db_from_file)
    values_from_file = MyNode(
        name="Read Values from File", graph=udpate_db_from_file
    )
    update_db = MyNode(name="Update DB", graph=udpate_db_from_file)
    find_file.outputs["file"].connect(values_from_file.inputs["file"])
    values_from_file.outputs["file"].connect(update_db.inputs["file"])


    # The second graph however relies on clean input files so the first graph can
    # be used within the second "udpate db" graph.
    # For this purpose, graphs can promote input and output plugs from their nodes
    # to the graph level, making other graphs aware of them:
    fix_file["Cleanup Filename"].inputs["file"].promote_to_graph(
        name="file_to_clean"
    )
    fix_file["Change Lineendings"].outputs["file"].promote_to_graph(
        name="clean_file"
    )

    # Now the update_db graph can connect nodes to the fix_file graph
    find_file.outputs["file"].connect(fix_file.inputs["file_to_clean"])
    fix_file.outputs["clean_file"].connect(
        udpate_db_from_file["Read Values from File"].inputs["file"]
    )

    # Display the graph
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor Nestd Graphs Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(parent=window)
    flowpipe_editor_widget.load_graph(fix_file)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(flowpipe_editor_widget)
    window.setLayout(layout)

    window.show()

    sys.exit(app.exec())
