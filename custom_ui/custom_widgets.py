from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QGraphicsView, QGraphicsScene, QComboBox
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QImage
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib.figure import Figure
import networkx as nx
import pygraphviz
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


# A png viewer with zoom feature.
class PNGViewer(QWidget):
    def __init__(self):
        super().__init__()

        # global variables
        self.zoom_factor = 1.0

        # Create a QGraphicsView and set its properties
        self.view = QGraphicsView(self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        # Create a QGraphicsScene and set its properties
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        # Set the zoom level of the QGraphicsView
        self.view.setTransform(QTransform().scale(self.zoom_factor, self.zoom_factor))
        
        # Add a slider to to control the zoom level
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(1)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.valueChanged.connect(self.__zoom)

        # png viewer with a zoom feature
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.zoom_slider)
        graph_layout.addWidget(self.view)

        self.setLayout(graph_layout)

    def __zoom(self, value):
        # Calculate the zoom factor based on the slider value
        self.zoom_factor = value / 100.0
        self.view.setTransform(QTransform().scale(self.zoom_factor, self.zoom_factor))

    # CALL BEFORE USAGE
    def setScene(self, filename):
        self.image = QPixmap(filename)
        self.scene.clear()
        self.item = self.scene.addPixmap(self.image)

    def clear(self):
        self.scene.clear()

class CustomQComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFFFFF; color: #333333")
        self.setFixedSize(120, 20)

class HTMLViewWidget(QWidget):
    # idea: I generate a dot file with graphviz. I extract the nodes, edges and positions from the dot file.
    # Might need my own classes for nodes and edges. I generate a networkx graph with my classes. 
    # I generate a html bokeh file with the networkx graph.
    # success?
    def ff():
        return

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.canvas = FigureCanvas(plt.figure())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.canvas.resize(self.size())