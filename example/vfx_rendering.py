import sys
from Qt import QtWidgets

from flowpipe import Graph, Node
from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

@Node(outputs=["renderings"], metadata={"interpreter": "maya"})
def MayaRender(frames, scene_file):
    return {"renderings": "/renderings/file.%04d.exr"}


@Node(outputs=["images"])
def CheckImages(images):
    return {"images": images}


@Node(outputs=["slapcomp"])
def CreateSlapComp(images, template):
    return {"slapcomp": "slapcomp.nk"}


@Node(outputs=["renderings"], metadata={"interpreter": "nuke"})
def NukeRender(frames, scene_file):
    return {"renderings": "/renderings/file.%04d.exr"}


@Node(outputs=["quicktime"])
def Quicktime(images):
    return {"quicktime": "resulting.mov"}


@Node(outputs=["status"])
def UpdateDatabase(id_, images):
    """Update the database entries of the given asset with the given data."""
    return {"status": True}


if __name__ == "__main__":
    graph = Graph(name="Rendering")
    frames, batch_size=30, 30
    slapcomp = CreateSlapComp(graph=graph, template="nuke_template.nk")
    update_database = UpdateDatabase(graph=graph, id_=123456)

    for i in range(0, frames, batch_size):
        maya_render = MayaRender(
            name="MayaRender{0}-{1}".format(i, i + batch_size),
            graph=graph,
            frames=range(i, i + batch_size),
            scene_file="/scene/for/rendering.ma",
        )
        check_images = CheckImages(
            name="CheckImages{0}-{1}".format(i, i + batch_size), graph=graph
        )
        maya_render.outputs["renderings"].connect(
            check_images.inputs["images"]
        )
        check_images.outputs["images"].connect(
            slapcomp.inputs["images"][str(i)]
        )
        check_images.outputs["images"].connect(
            update_database.inputs["images"][str(i)]
        )

    quicktime = Quicktime()

    for i in range(0, frames, batch_size):
        nuke_render = NukeRender(
            name="NukeRender{0}-{1}".format(i, i + batch_size),
            graph=graph,
            frames=range(i, i + batch_size),
        )
        slapcomp.outputs["slapcomp"].connect(nuke_render.inputs["scene_file"])
        nuke_render.outputs["renderings"].connect(
            quicktime.inputs["images"][str(i)]
        )
    print(graph)
    # Display the graph
    app = QtWidgets.QApplication(sys.argv)

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