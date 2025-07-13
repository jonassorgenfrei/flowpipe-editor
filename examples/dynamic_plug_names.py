import sys
from pathlib import Path

from flowpipe import Graph, INode, InputPlug, OutputPlug
from Qt import QtWidgets, QtGui

from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

BASE_PATH = Path(__file__).parent.parent.resolve()


def compute_embeddings(image):
    """A mock function for a call to a deep learning model or a web service."""
    del image  # this is just a mock and doesn't do anything with the input
    return 42


def compare_embeddings(image_emb, reference_emb, threshold=2):
    """A mock function for the appropriate comparison of embeddings."""
    return abs(image_emb - reference_emb) < threshold


class EmbeddingNode(INode):
    """The embedding node computes facial features from an image."""

    def __init__(self, input_name, output_name, **kwargs):
        """Set up a new EmbeddingNode with given names for plugs."""
        super().__init__(**kwargs)

        self.input_name = input_name  # Needed to access the value in compute
        InputPlug(input_name, self)

        self.output_name = output_name  # Needed to access the value in compute
        OutputPlug(output_name, self)

    # Accept generic keyword arguments, since the names of the inputs are
    # undefined until at runtime
    def compute(self, **kwargs):
        image = kwargs.pop(self.input_name)

        embedding = compute_embeddings(image)

        return {self.output_name: embedding}


class MatchNode(INode):
    """The match node compares two embeddings."""

    def __init__(self, threshold=2, **kwargs):
        super().__init__(**kwargs)
        self.threshold = threshold

        InputPlug("image_emb", self)
        InputPlug("reference_emb", self)

        OutputPlug("facematch", self)

    def compute(self, image_emb, reference_emb):
        """Compare the embeddings."""
        match = compare_embeddings(image_emb, reference_emb, self.threshold)
        return {"facematch": match}


def get_facematch_graph(threshold):
    """Set up facematching e.g. with paramters taken from a config."""
    facematch_graph = Graph()

    # It is useful to define
    image_node = EmbeddingNode(
        input_name="image",
        output_name="image_emb",
        graph=facematch_graph,
        name="ImageEmbeddings",
    )

    reference_node = EmbeddingNode(
        input_name="reference",
        output_name="reference_emb",
        graph=facematch_graph,
        name="ReferenceEmbeddings",
    )

    match_node = MatchNode(threshold=threshold, graph=facematch_graph)

    image_node.outputs["image_emb"] >> match_node.inputs["image_emb"]
    (
        reference_node.outputs["reference_emb"]
        >> match_node.inputs["reference_emb"]
    )

    match_node.outputs["facematch"].promote_to_graph("result")

    return facematch_graph


if __name__ == "__main__":
    facematch = get_facematch_graph(1)

    # Display the graph
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(
        QtGui.QIcon(
            str(Path(BASE_PATH, "flowpipe_editor", "icons", "flowpipe.png"))
        )
    )

    window = QtWidgets.QWidget()
    window.setWindowTitle("Flowpipe-Editor Dynamic Plug Names Example")
    window.resize(1100, 800)

    flowpipe_editor_widget = FlowpipeEditorWidget(parent=window)
    flowpipe_editor_widget.load_graph(facematch)
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(flowpipe_editor_widget)
    window.setLayout(layout)

    window.show()

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())
