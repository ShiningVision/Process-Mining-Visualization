from PyQt5.QtCore import Qt, QDir, QFile
from PyQt5.QtWidgets import QApplication, QMainWindow,QStackedWidget,QMessageBox, QFileDialog,QTableWidget, QTableWidgetItem, QDockWidget,QSlider,QLabel,QWidget,QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mining_algorithms.heuristic_mining import HeuristicMining
from mining_algorithms.csv_reader import read

class HeuristicGraphDisplayView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.figure = plt.figure(figsize=(50, 50))
        self.canvas = FigureCanvas(self.figure)
        self.dependency_treshhold = 0.5
        self.min_frequency = 1
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def mine(self, filepath, timeLabel, caseLabel, eventLabel):
        cases = read(filepath, timeLabel, caseLabel, eventLabel)
        self.Heuristic_Model = HeuristicMining(cases)
        self.__mine_and_draw_csv()

        self.__create_slider_dock_widget()
        self.parent.add_dock_widget( self.slider_dock_widget)

    def __freq_slider_changed(self, value):
        # Update the label with the slider value
        self.freq_slider_label.setText(f"Min. Frequency: {value}")
        # Redraw graph when value changes
        self.min_frequency = value
        self.__mine_and_draw_csv()
    
    def __thresh_slider_changed(self, value):
        # Update the label with the slider value
        self.thresh_slider_label.setText(f"Dependency Threshhold: {value/100:.2f}")
        # Redraw graph when value changes
        self.dependency_treshhold = value/100
        self.__mine_and_draw_csv()

    def __create_slider_dock_widget(self):
        # Add the dock widget for the slider and canvas
        self.slider_dock_widget = QDockWidget("Heuristic variables")

        # Create the slider and label widgets
        self.freq_slider = QSlider(Qt.Vertical)
        self.freq_slider.setRange(0, 100)
        self.freq_slider.setValue(1)
        self.freq_slider.valueChanged.connect(self.__freq_slider_changed)

        self.freq_slider_label = QLabel("Min Frequency: 1")
        self.freq_slider_label.setAlignment(Qt.AlignCenter)

        # Create the second slider and label widgets
        self.thresh_slider = QSlider(Qt.Vertical)
        self.thresh_slider.setRange(0, 100)
        self.thresh_slider.setValue(50)
        self.thresh_slider.valueChanged.connect(self.__thresh_slider_changed)

        self.thresh_slider_label = QLabel("Dependency Threshhold: 0.50")
        self.thresh_slider_label.setAlignment(Qt.AlignCenter)

        # Create a new widget for the slider and canvas
        slider_widget = QWidget()
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.freq_slider)
        slider_layout.addWidget(self.freq_slider_label)
        slider_layout.addWidget(self.thresh_slider)
        slider_layout.addWidget(self.thresh_slider_label)
        slider_widget.setLayout(slider_layout)

        # Adjust the size of the slider widget
        slider_widget.setMinimumWidth(100)

        # Add the slider and canvas widget to the dock widget
        self.slider_dock_widget.setWidget(slider_widget)

        # Create a new canvas for the right dock widget
        self.right_canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.slider_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
    
    def __mine_and_draw_csv(self):

        '''with graphviz'''
        graphviz_graph = self.Heuristic_Model.create_dependency_graph_with_graphviz(self.dependency_treshhold,self.min_frequency)
        
        self.filepath = 'temp/graph_viz'
        filename = self.filepath + '.png'
        graphviz_graph.render(self.filepath,format = 'png')

        self.figure.clear()
        
        graph = plt.imread(filename)

        plt.imshow(graph)
        # Set axis limits to size of image
        plt.xlim([0, graph.shape[1]])
        plt.ylim([graph.shape[0], 0])

        # Turn off axis labels and tick marks
        plt.axis('off')

        self.canvas.draw()
        print("CSV mined")

    def clear(self):
        self.dependency_treshhold= 0.5
        self.min_frequency = 1
