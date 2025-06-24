# hghooks: no-pep8 no-pyflakes no-pdb no-jslint
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './flowpipe_editor.ui'
#
# Created: Tue May  7 18:08:27 2024
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets


class Ui_FlowpipeEditorWindow(object):
    def setupUi(self, FlowpipeEditorWindow):
        FlowpipeEditorWindow.setObjectName("FlowpipeEditorWindow")
        FlowpipeEditorWindow.resize(657, 549)
        FlowpipeEditorWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        FlowpipeEditorWindow.setDockNestingEnabled(True)
        FlowpipeEditorWindow.setDockOptions(
            QtWidgets.QMainWindow.AllowNestedDocks
            | QtWidgets.QMainWindow.AllowTabbedDocks
            | QtWidgets.QMainWindow.AnimatedDocks
            | QtWidgets.QMainWindow.ForceTabbedDocks
            | QtWidgets.QMainWindow.VerticalTabs
        )
        self.centralwidget = QtWidgets.QWidget(FlowpipeEditorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.main_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_widget.sizePolicy().hasHeightForWidth())
        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.graph_name_lineedit = QtWidgets.QLineEdit(self.main_widget)
        self.graph_name_lineedit.setText("")
        self.graph_name_lineedit.setReadOnly(True)
        self.graph_name_lineedit.setObjectName("graph_name_lineedit")
        self.verticalLayout_5.addWidget(self.graph_name_lineedit)
        self.graph_widget = QtWidgets.QWidget(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph_widget.sizePolicy().hasHeightForWidth())
        self.graph_widget.setSizePolicy(sizePolicy)
        self.graph_widget.setObjectName("graph_widget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.graph_widget)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_5.addWidget(self.graph_widget)
        self.verticalLayout_6.addWidget(self.main_widget)
        FlowpipeEditorWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FlowpipeEditorWindow)
        self.statusbar.setObjectName("statusbar")
        FlowpipeEditorWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(FlowpipeEditorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 25))
        self.menubar.setObjectName("menubar")
        FlowpipeEditorWindow.setMenuBar(self.menubar)
        self.node_dock = QtWidgets.QDockWidget(FlowpipeEditorWindow)
        self.node_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
        )
        self.node_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.node_dock.setObjectName("node_dock")
        self.node_name_widget = QtWidgets.QWidget()
        self.node_name_widget.setObjectName("node_name_widget")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.node_name_widget)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_lineedit = QtWidgets.QLineEdit(self.node_name_widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.name_lineedit.setFont(font)
        self.name_lineedit.setStyleSheet("")
        self.name_lineedit.setReadOnly(True)
        self.name_lineedit.setObjectName("name_lineedit")
        self.horizontalLayout.addWidget(self.name_lineedit)
        self.open_code_button = QtWidgets.QToolButton(self.node_name_widget)
        self.open_code_button.setObjectName("open_code_button")
        self.horizontalLayout.addWidget(self.open_code_button)
        self.verticalLayout_14.addLayout(self.horizontalLayout)
        self.node_type_label = QtWidgets.QLabel(self.node_name_widget)
        self.node_type_label.setText("")
        self.node_type_label.setObjectName("node_type_label")
        self.verticalLayout_14.addWidget(self.node_type_label)
        self.description_textedit = QtWidgets.QTextEdit(self.node_name_widget)
        self.description_textedit.setMinimumSize(QtCore.QSize(0, 30))
        self.description_textedit.setStyleSheet("background-color: palette(window);")
        self.description_textedit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.description_textedit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.description_textedit.setReadOnly(True)
        self.description_textedit.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.description_textedit.setObjectName("description_textedit")
        self.verticalLayout_14.addWidget(self.description_textedit)
        self.node_dock.setWidget(self.node_name_widget)
        FlowpipeEditorWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.node_dock)
        self.inputs_dock = QtWidgets.QDockWidget(FlowpipeEditorWindow)
        self.inputs_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
        )
        self.inputs_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.inputs_dock.setObjectName("inputs_dock")
        self.node_inputs_widget = AttributesWidget()
        self.node_inputs_widget.setMouseTracking(False)
        self.node_inputs_widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.node_inputs_widget.setObjectName("node_inputs_widget")
        self.inputs_dock.setWidget(self.node_inputs_widget)
        FlowpipeEditorWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.inputs_dock
        )
        self.outputs_dock = QtWidgets.QDockWidget(FlowpipeEditorWindow)
        self.outputs_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
        )
        self.outputs_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.outputs_dock.setObjectName("outputs_dock")
        self.node_outputs_widget = AttributesWidget()
        self.node_outputs_widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.node_outputs_widget.setObjectName("node_outputs_widget")
        self.outputs_dock.setWidget(self.node_outputs_widget)
        FlowpipeEditorWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.outputs_dock
        )
        self.metadata_dock = QtWidgets.QDockWidget(FlowpipeEditorWindow)
        self.metadata_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
        )
        self.metadata_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.metadata_dock.setObjectName("metadata_dock")
        self.node_metadata_widget = QtWidgets.QWidget()
        self.node_metadata_widget.setObjectName("node_metadata_widget")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.node_metadata_widget)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.metadata_view = JsonView(self.node_metadata_widget)
        self.metadata_view.setObjectName("metadata_view")
        self.verticalLayout_15.addWidget(self.metadata_view)
        self.metadata_dock.setWidget(self.node_metadata_widget)
        FlowpipeEditorWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.metadata_dock
        )
        self.evaluation_dock = QtWidgets.QDockWidget(FlowpipeEditorWindow)
        self.evaluation_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable
            | QtWidgets.QDockWidget.DockWidgetMovable
        )
        self.evaluation_dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.evaluation_dock.setObjectName("evaluation_dock")
        self.evaluation_widget = QtWidgets.QWidget()
        self.evaluation_widget.setObjectName("evaluation_widget")
        self.verticalLayout_151 = QtWidgets.QVBoxLayout(self.evaluation_widget)
        self.verticalLayout_151.setObjectName("verticalLayout_151")
        self.submit_to_farm_button = QtWidgets.QPushButton(self.evaluation_widget)
        self.submit_to_farm_button.setObjectName("submit_to_farm_button")
        self.verticalLayout_151.addWidget(self.submit_to_farm_button)
        self.evaluate_locally_button = QtWidgets.QPushButton(self.evaluation_widget)
        self.evaluate_locally_button.setObjectName("evaluate_locally_button")
        self.verticalLayout_151.addWidget(self.evaluate_locally_button)
        self.evaluation_dock.setWidget(self.evaluation_widget)
        FlowpipeEditorWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.evaluation_dock
        )
        self.actionNew = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionOpen_Recent = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionOpen_Recent.setObjectName("actionOpen_Recent")
        self.actionQuit = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionDocumentation = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.evaluate_remotely_action = QtWidgets.QAction(FlowpipeEditorWindow)
        self.evaluate_remotely_action.setObjectName("evaluate_remotely_action")
        self.actionThreaed = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionThreaed.setObjectName("actionThreaed")
        self.actionNon_threaed = QtWidgets.QAction(FlowpipeEditorWindow)
        self.actionNon_threaed.setObjectName("actionNon_threaed")
        self.evaluate_locally_action = QtWidgets.QAction(FlowpipeEditorWindow)
        self.evaluate_locally_action.setObjectName("evaluate_locally_action")
        self.edit_mode_action = QtWidgets.QAction(FlowpipeEditorWindow)
        self.edit_mode_action.setCheckable(True)
        self.edit_mode_action.setObjectName("edit_mode_action")
        self.project_action = QtWidgets.QAction(FlowpipeEditorWindow)
        self.project_action.setObjectName("project_action")

        self.retranslateUi(FlowpipeEditorWindow)
        QtCore.QMetaObject.connectSlotsByName(FlowpipeEditorWindow)

    def retranslateUi(self, FlowpipeEditorWindow):
        FlowpipeEditorWindow.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Flowpipe Editor", None, -1
            )
        )
        self.node_dock.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Node Info", None, -1
            )
        )
        self.open_code_button.setText(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Open", None, -1)
        )
        self.inputs_dock.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Input Plugs", None, -1
            )
        )
        self.outputs_dock.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Output Plugs", None, -1
            )
        )
        self.metadata_dock.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Metadata", None, -1
            )
        )
        self.evaluation_dock.setWindowTitle(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Evaluation", None, -1
            )
        )
        self.submit_to_farm_button.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Submit To Farm", None, -1
            )
        )
        self.evaluate_locally_button.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Evaluate Locally", None, -1
            )
        )
        self.actionNew.setText(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "New", None, -1)
        )
        self.actionNew.setShortcut(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Ctrl+N", None, -1)
        )
        self.actionOpen.setText(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Open", None, -1)
        )
        self.actionOpen.setShortcut(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Ctrl+O", None, -1)
        )
        self.actionSave.setText(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Save", None, -1)
        )
        self.actionSave.setShortcut(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Ctrl+S", None, -1)
        )
        self.actionSave_As.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Save As...", None, -1
            )
        )
        self.actionSave_As.setShortcut(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Ctrl+Shift+S", None, -1
            )
        )
        self.actionOpen_Recent.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Open Recent", None, -1
            )
        )
        self.actionQuit.setText(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Quit", None, -1)
        )
        self.actionQuit.setShortcut(
            QtWidgets.QApplication.translate("FlowpipeEditorWindow", "Ctrl+Q", None, -1)
        )
        self.actionDocumentation.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Documentation", None, -1
            )
        )
        self.evaluate_remotely_action.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Send to Farm", None, -1
            )
        )
        self.actionThreaed.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Threaded", None, -1
            )
        )
        self.actionNon_threaed.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Non-threaded", None, -1
            )
        )
        self.evaluate_locally_action.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Evaluate Locally", None, -1
            )
        )
        self.edit_mode_action.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Edit Mode", None, -1
            )
        )
        self.project_action.setText(
            QtWidgets.QApplication.translate(
                "FlowpipeEditorWindow", "Project...", None, -1
            )
        )


from qt_json_view.view import JsonView
from risefx.flowpipe_editor.attributes.attributes_widget import AttributesWidget
