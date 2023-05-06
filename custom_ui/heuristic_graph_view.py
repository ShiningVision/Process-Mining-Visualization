from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy,QPushButton, QWidget, QSlider,QLabel,QVBoxLayout, QHBoxLayout, QFrame
from mining_algorithms.heuristic_mining import HeuristicMining
from custom_ui.algorithm_view_interface import AlgorithmViewInterface
from custom_ui.custom_widgets import PNGViewer
from mining_algorithms.csv_preprocessor import save

class HeuristicGraphView(QWidget, AlgorithmViewInterface):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        #modifiers and global variables
        self.dependency_treshhold = 0.5
        self.min_frequency = 1
        self.max_frequency = 100
        self.filepath = 'temp/graph_viz'
        self.graphviz_graph = None
        self.filename = None
        self.cases = None
        # used for spacing items in those Q BoxLayouts to center stuff.
        # spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.graph_widget = PNGViewer()
        
        # Create the slider frame
        slider_frame = QFrame()
        slider_frame.setFrameShape(QFrame.StyledPanel)
        slider_frame.setFrameShadow(QFrame.Sunken)
        slider_frame.setMinimumWidth(200)

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

        freq_slider_layout = QVBoxLayout()
        freq_slider_layout.addWidget(self.freq_slider)
        freq_slider_layout.addWidget(self.freq_slider_label)

        thresh_slider_layout = QVBoxLayout()
        thresh_slider_layout.addWidget(self.thresh_slider)
        thresh_slider_layout.addWidget(self.thresh_slider_label)

        slider_layout.addLayout(freq_slider_layout)
        slider_layout.addLayout(thresh_slider_layout)

        quicksave_button = QPushButton("quicksave")
        quicksave_button.clicked.connect(self.__save)

        slider_frame_layout = QVBoxLayout()
        slider_frame_layout.addWidget(QLabel("Heuristic Mining Modifiers", alignment=Qt.AlignCenter))
        slider_frame_layout.addLayout(slider_layout)
        slider_frame_layout.addWidget(quicksave_button)
        slider_frame.setLayout(slider_frame_layout)

        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.graph_widget, stretch=3)
        main_layout.addWidget(slider_frame, stretch=1)

        self.setLayout(main_layout)

    # CALL BEFORE INIT
    def startMining(self, filename, cases):
        self.filename = filename
        self.cases = cases
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

    def __save(self):
        save(self.filename, self.cases)
        self.parent.show_message("Project saved")

    def __mine_and_draw_csv(self):

        '''with graphviz'''
        self.graphviz_graph = self.Heuristic_Model.create_dependency_graph_with_graphviz(self.dependency_treshhold,self.min_frequency)
        
        # generate png
        self.graphviz_graph.render(self.filepath,format = 'png')
        print("heuristic_graph_view: CSV mined")

        # Load the image and add it to the QGraphicsScene
        filename = self.filepath + '.png'
        self.graph_widget.setScene(filename)

    def generate_png(self):
        #the heuristic algorithm loads the png to show on the canvas.
        #No need to generate it again, if it is already there.
        return

    def generate_svg(self):
        self.graphviz_graph.render(self.filepath,format = 'svg')
        print("heuristic_graph_view: SVG generated")

    def generate_dot(self):
        self.graphviz_graph.render(self.filepath,format = 'dot')
        print("heuristic_graph_view: DOT generated")

    def clear(self):
        self.graph_widget.clear()
        self.dependency_treshhold= 0.5
        self.min_frequency = 1
        self.zoom_factor = 1.0
