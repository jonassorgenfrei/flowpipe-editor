import sys
from dataclasses import asdict
from pathlib import Path

from flowpipe import Graph, Node
from Qt import QtGui, QtWidgets

from flowpipe_editor import flowpipe_editor_widget
from flowpipe_editor.flowpipe_editor_widget import (
    FlowpipeEditorWidget,
    FlowpipeEditorWidgetStyle,
)

BASE_PATH = Path(__file__).parent.parent.resolve()

# example to overwrite the icons path for
flowpipe_editor_widget.ICONS_PATH = Path(
    Path(flowpipe_editor_widget.__file__).parent.resolve(),
    "icons",
)


@Node(
    outputs=["camera_file"],
    metadata={
        "interpreter": "3dequalizer",
        "FlowpipeEditorWidgetStyle": asdict(
            FlowpipeEditorWidgetStyle(color="#1E0500")
        ),
    },
)
def CreateCamera():
    """Creates a shot camera."""
    return {"camera_file": "/abs/camera.abc"}


@Node(
    outputs=["scene_file"],
    metadata={
        "interpreter": "maya",
        "FlowpipeEditorWidgetStyle": asdict(
            FlowpipeEditorWidgetStyle(color="#001574")
        ),
    },
)
def MayaSceneGeneration(camera_file):
    """Creates a Maya scene file for rendering."""
    return {"scene_file": "/usd/scene.usd"}


@Node(
    outputs=["renderings"],
    metadata={
        "interpreter": "houdini",
        "FlowpipeEditorWidgetStyle": asdict(
            FlowpipeEditorWidgetStyle(color="#7A2400")
        ),
    },
)
def HoudiniRender(frames, scene_file):
    """Creates a Houdini scene file for rendering."""
    return {"renderings": "/renderings/file.%04d.exr"}


@Node(outputs=["images"])
def CheckImages(images):
    """Check if the images are valid and return them."""
    return {"images": images}


@Node(
    outputs=["slapcomp"],
    metadata={
        "interpreter": "nuke",
        "FlowpipeEditorWidgetStyle": asdict(
            FlowpipeEditorWidgetStyle(
                color="#1E0500",
                icon=Path(BASE_PATH, "flowpipe_editor", "icons", "star.png"),
            )
        ),
    },
)
def CreateSlapComp(images, template):
    """Create a nuke slapcomp scene file from the given images and template."""
    return {"slapcomp": "slapcomp.nk"}


@Node(outputs=["renderings"], metadata={"interpreter": "nuke"})
def NukeRender(frames, scene_file):
    """Renders the slapcomp scene file using Nuke."""
    return {"renderings": "/renderings/file.%04d.exr"}


@Node(outputs=["quicktime"])
def Quicktime(images):
    """Create a quicktime movie from the rendered images."""
    return {"quicktime": "resulting.mov"}


@Node(outputs=["status"])
def UpdateDatabase(id_, images):
    """Update the database entries of the given asset with the given data."""
    return {"status": True}


if __name__ == "__main__":
    graph = Graph(name="Rendering")
    frames, batch_size = 30, 10
    slapcomp = CreateSlapComp(graph=graph, template="nuke_template.nk")
    update_database = UpdateDatabase(graph=graph, id_=123456)

    camera_creation = CreateCamera(graph=graph)
    scene_creation = MayaSceneGeneration(graph=graph)

    camera_creation.outputs["camera_file"].connect(
        scene_creation.inputs["camera_file"]
    )

    for i in range(0, frames, batch_size):
        houdini_render = HoudiniRender(
            name="HoudiniRender{0}-{1}".format(i, i + batch_size),
            graph=graph,
            frames=range(i, i + batch_size),
        )
        check_images = CheckImages(
            name="CheckImages{0}-{1}".format(i, i + batch_size), graph=graph
        )
        scene_creation.outputs["scene_file"].connect(
            houdini_render.inputs["scene_file"]
        )
        houdini_render.outputs["renderings"].connect(
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

    # Display the graph
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(
        QtGui.QIcon(
            str(Path(BASE_PATH, "flowpipe_editor", "icons", "flowpipe.png"))
        )
    )

    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor VFX Rendering Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(
        expanded_properties=False, parent=window
    )
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
