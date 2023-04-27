from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider,QLabel,QWidget,QVBoxLayout, QHBoxLayout, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mining_algorithms.heuristic_mining import HeuristicMining
from mining_algorithms.csv_preprocessor import read

class HeuristicGraphDisplayView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.figure = plt.figure(figsize=(50, 50))
        self.canvas = FigureCanvas(self.figure)
        self.dependency_treshhold = 0.5
        self.min_frequency = 1
        self.max_frequency = 100
        
        # Create the slider frame
        slider_frame = QFrame()
        slider_frame.setFrameShape(QFrame.StyledPanel)
        slider_frame.setFrameShadow(QFrame.Sunken)
        slider_frame.setMinimumWidth(200)

        # Create the sliders
        slider_layout = QHBoxLayout()

        self.freq_slider = QSlider(Qt.Vertical)
        self.freq_slider.setRange(self.min_frequency, self.max_frequency)
        self.freq_slider.setValue(self.min_frequency)
        self.freq_slider.valueChanged.connect(self.__freq_slider_changed)
        self.freq_slider_label = QLabel(f"Min Frequency: {self.min_frequency}")
        self.freq_slider_label.setAlignment(Qt.AlignCenter)

        self.thresh_slider = QSlider(Qt.Vertical)
        self.thresh_slider.setRange(0, 100)
        self.thresh_slider.setValue(50)
        self.thresh_slider.valueChanged.connect(self.__thresh_slider_changed)
        self.thresh_slider_label = QLabel(f"Dependency Threshhold: {self.dependency_treshhold}")
        self.thresh_slider_label.setAlignment(Qt.AlignCenter)

        slider1_layout = QVBoxLayout()
        slider1_layout.addWidget(self.freq_slider)
        slider1_layout.addWidget(self.freq_slider_label)

        slider2_layout = QVBoxLayout()
        slider2_layout.addWidget(self.thresh_slider)
        slider2_layout.addWidget(self.thresh_slider_label)

        slider_layout.addLayout(slider1_layout)
        slider_layout.addLayout(slider2_layout)

        # Create image layout
        image_layout = QVBoxLayout(self)
        
        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.canvas, stretch=3)
        main_layout.addWidget(slider_frame, stretch=1)

        # Add the slider layout to the slider frame layout
        slider_frame_layout = QVBoxLayout()
        slider_frame_layout.addWidget(QLabel("Heuristic Mining Modifiers", alignment=Qt.AlignCenter))
        slider_frame_layout.addLayout(slider_layout)
        slider_frame.setLayout(slider_frame_layout)

        self.setLayout(main_layout)

    def mine(self, filepath, timeLabel, caseLabel, eventLabel):
        cases = read(filepath, timeLabel, caseLabel, eventLabel)
        self.Heuristic_Model = HeuristicMining(cases)
        self.max_frequency = self.Heuristic_Model.get_max_frequency()
        self.freq_slider.setRange(self.min_frequency,self.max_frequency)
        self.__mine_and_draw_csv()

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
