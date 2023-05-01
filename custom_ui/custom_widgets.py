from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QWidget, QSlider,QLabel,QVBoxLayout, QHBoxLayout, QFrame, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPainter, QTransform

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

    # change the png
    def setScene(self, filename):
        self.image = QPixmap(filename)
        self.scene.clear()
        self.item = self.scene.addPixmap(self.image)

    def clear(self):
        self.scene.clear()
