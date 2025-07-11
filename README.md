# flowpipe-editor
[![Version](https://img.shields.io/pypi/v/flowpipe_editor.svg)](https://pypi.org/project/flowpipe_editor/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flowpipe_editor)  [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

QT Editor for the flowpipe framework based on NodeGraphQt.

![flowpipe-editor](https://raw.githubusercontent.com/jonassorgenfrei/flowpipe-editor/main/docs/img/flowpipe-editor.png)

NOTE: In it's current state the Widget is a visualizer only not an editor.

## Example
```python
from flowpipe import Graph
from flowpipe_editor.flowpipe_editor_widget import FlowpipeEditorWidget

graph = Graph(name="Rendering")

# ... create nodes and append to graph ...

window = QtWidgets.QWidget()

flowpipe_editor_widget = FlowpipeEditorWidget(parent=parentWidget)
flowpipe_editor_widget.load_graph(graph)

# .. add widget to window 

```

## Requirements
The requirements can be installed via pip.

* [flowpipe](https://github.com/PaulSchweizer/flowpipe) 
* [NodeGraphQT](https://github.com/jchanvfx/NodeGraphQt)
