from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFileDialog, QSlider, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QTransform
import os
from algorithms.pickle_save import pickle_save


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
        self.view.setTransform(QTransform().scale(
            self.zoom_factor, self.zoom_factor))

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
        self.view.setTransform(QTransform().scale(
            self.zoom_factor, self.zoom_factor))

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
        self.setFixedSize(150, 20)


class BottomOperationInterfaceLayoutWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        # parent should be QMainWindow
        self.parent = parent

        # Set up algorithm selector combo box
        self.selected_algorithm = 0
        self.algorithm_selector = CustomQComboBox()
        self.algorithm_selector.currentIndexChanged.connect(
            self.__algorithm_selected)

        # Two buttons 'LOAD EXISTING PROCESS' 'MINE NEW PROCESS FROM CSV'
        load_button = QPushButton("LOAD EXISTING PROCESS")
        load_button.setFixedSize(200, 40)
        load_button.setStyleSheet("background-color: #00FF7F; color: #333333;")
        load_button.clicked.connect(self.mine_existing_process)

        mine_button = QPushButton("MINE NEW PROCESS\nFROM CSV")
        mine_button.setFixedSize(200, 40)
        mine_button.setStyleSheet("background-color: #00BFFF; color: #333333;")
        mine_button.clicked.connect(self.mine_new_process)

        # 'LOAD EXISTING PROCESS' needs a drop down menu to its side
        load_process_layout = QHBoxLayout()
        load_process_layout.addWidget(load_button)
        load_process_layout.addWidget(self.algorithm_selector)

        # Wrap together the 2 buttons.
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(mine_button)
        button_layout.addLayout(load_process_layout)

        self.setLayout(button_layout)

    # CALL BEFORE USAGE
    def load_algorithms(self, array):
        for element in array:
            self.algorithm_selector.addItem(element)

    def mine_existing_process(self):
        self.parent.mine_existing_process(self.selected_algorithm)

    def mine_new_process(self):
        self.parent.switch_to_column_selection_view()

    def __algorithm_selected(self, index):
        self.algorithm_selector.setCurrentIndex(index)
        self.selected_algorithm = index


class BottomOperationInterfaceWrapper(QWidget):
    def __init__(self, parent, view, algorithms):
        super().__init__()
        # parent should be QMainWindow
        self.parent = parent
        self.topWidget = view
        self.bottomWidget = BottomOperationInterfaceLayoutWidget(parent)

        # There is a QCombobox in the bottom layout that needs labels.
        self.bottomWidget.load_algorithms(algorithms)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.topWidget)
        self.layout.addWidget(self.bottomWidget)

        self.setLayout(self.layout)

    # God praise this holy method. Enabling all the functions of the View without having to inherit from it.
    def __getattr__(self, attr):
        return getattr(self.topWidget, attr)


class SaveProjectButton(QWidget):
    def __init__(self, parent, saveFolder, getModelFunction, filename="graphviz_project", text="Save Project"):
        super().__init__()
        self.parent = parent
        self.filename = filename
        self.saveFolder = saveFolder
        self.text = text
        self.Mining_Model = None
        self.getModelFunction = getModelFunction
        quicksave_button = QPushButton(text)
        quicksave_button.clicked.connect(self.__save)
        self.layout = QVBoxLayout()
        self.layout.addWidget(quicksave_button)
        self.setLayout(self.layout)

    def load_filename(self, filename):
        self.filename = filename

    def __save(self):
        self.Mining_Model = self.getModelFunction()

        # get the basename of the original file
        basename = os.path.splitext(os.path.basename(self.filename))[0]

        # create the save folder if it does not exist:
        if not os.path.exists(self.saveFolder):
            os.makedirs(self.saveFolder)

        filename = self.saveFolder + basename
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", filename)
        if not file_path:
            return -1

        # save the model as a pickle datastream
        status = pickle_save(self.Mining_Model, file_path)
        if status == -1:
            return -1

        projectname = os.path.splitext(os.path.basename(file_path))[0]

        # notify the user that the model has been saved:
        self.parent.show_pop_up_message(f"Project saved as {projectname}")


class ExportButton(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        text = "Export as image"
        button = QPushButton(text)
        button.clicked.connect(self.__export)
        self.layout = QVBoxLayout()
        self.layout.addWidget(button)
        self.setLayout(self.layout)

    def __export(self):
        self.parent.switch_to_export_view()


class CustomQSlider(QWidget):
    def __init__(self, onSlide, QtDirection=Qt.Vertical):
        super().__init__()

        self.onSlideFunction = onSlide
        self.slider = QSlider(QtDirection)
        self.slider.valueChanged.connect(self.__slider_changed)
        self.slider_label = QLabel(f"slider: value")
        self.slider_label.setAlignment(Qt.AlignCenter)

        self.slider_box = QHBoxLayout()
        self.slider_box.addStretch(0)
        self.slider_box.addWidget(self.slider)
        self.slider_box.addStretch(0)

        slider_layout = QVBoxLayout()
        slider_layout.addLayout(self.slider_box)
        slider_layout.addWidget(self.slider_label)

        self.setLayout(slider_layout)

    def setText(self, text):
        self.slider_label.setText(text)

    def setRange(self, min, max):
        self.slider.setRange(min, max)

    def setValue(self, value):
        self.slider.setValue(value)

    def __slider_changed(self, value):
        self.onSlideFunction(value)
