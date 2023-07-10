from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel,QVBoxLayout, QHBoxLayout, QFrame
from api.custom_error import FileNotFoundException
from custom_ui.heuristic_graph_ui.heuristic_graph_controller import HeuristicGraphController
from custom_ui.algorithm_view_interface import AlgorithmViewInterface
from custom_ui.d3_html_widget import HTMLWidget
from custom_ui.custom_widgets import SaveProjectButton, ExportButton, CustomQSlider

class HeuristicGraphView(QWidget, AlgorithmViewInterface):
    def __init__(self, parent, saveFolder = "saves/", workingDirectory = 'temp/graph_viz'):
        super().__init__()
        self.parent = parent
        self.initialized = False

        #modifiers and global variables
        self.default_dependency_threshold = 0.5
        self.dependency_threshold = self.default_dependency_threshold
        self.default_min_frequency = 1
        self.min_frequency = self.default_min_frequency
        self.max_frequency = 100
        self.saveFolder = saveFolder
        self.workingDirectory = workingDirectory # the working directory is where the graphviz file is stored for display and export
        self.HeuristicGraphController = HeuristicGraphController(workingDirectory, self.dependency_threshold, self.min_frequency) 
        self.graphviz_graph = None # the graphviz object

        self.graph_widget = HTMLWidget(parent)
        
        # Create the slider frame
        slider_frame = QFrame()
        slider_frame.setFrameShape(QFrame.StyledPanel)
        slider_frame.setFrameShadow(QFrame.Sunken)
        slider_frame.setMinimumWidth(200)

        self.freq_slider = CustomQSlider(self.__freq_slider_changed, Qt.Vertical)
        self.freq_slider.setRange(self.min_frequency, self.max_frequency)
        self.freq_slider.setValue(self.min_frequency)

        self.thresh_slider = CustomQSlider(self.__thresh_slider_changed, Qt.Vertical)
        self.thresh_slider.setRange(0, 100)
        self.thresh_slider.setValue(50)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.freq_slider)
        slider_layout.addWidget(self.thresh_slider)

        self.saveProject_button = SaveProjectButton(self.parent,self.saveFolder,self.getModel)
        self.export_button = ExportButton(self.parent)
        slider_frame_layout = QVBoxLayout()
        slider_frame_layout.addWidget(QLabel("Heuristic Mining Modifiers", alignment=Qt.AlignCenter))
        slider_frame_layout.addLayout(slider_layout)
        slider_frame_layout.addWidget(self.saveProject_button)
        slider_frame_layout.addWidget(self.export_button)
        slider_frame.setLayout(slider_frame_layout)

        # Create the main layout
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.graph_widget, stretch=3)
        main_layout.addWidget(slider_frame, stretch=1)

        self.setLayout(main_layout)

    # CALL BEFORE USAGE (option 1 for mining new models) 
    def startMining(self, filename, cases):

        self.saveProject_button.load_filename(filename)
        self.HeuristicGraphController.startMining(cases)
        
        self.min_frequency = self.default_min_frequency
        self.dependency_threshold = self.default_dependency_threshold
        self.max_frequency = self.HeuristicGraphController.get_max_frequency()
        self.freq_slider.setRange(1,self.max_frequency)
        self.__set_slider_values(self.min_frequency,self.dependency_threshold)

        self.graph_widget.start_server()
        self.initialized=True
        self.__mine_and_draw()

    # CALL BEFORE USAGE (option 2 for mining existing models)
    def loadModel(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(None, "Select file", self.saveFolder, "Pickle files (*.pickle)")
            # If the user cancels the file dialog, return
            if not file_path:
                return -1
            filename = self.HeuristicGraphController.loadModel(file_path)
            if filename == -1:
                return -1
        except TypeError as e:
            message = "HeuristicGraphView loadModel(): Error: Something went wrong while loading an existing model."
            print(str(e))
            self.parent.show_pop_up_message(message, 6000)
            return -1
        
        self.saveProject_button.load_filename(filename)

        self.max_frequency = self.HeuristicGraphController.get_max_frequency()
        self.freq_slider.setRange(1,self.max_frequency)
        self.min_frequency = self.HeuristicGraphController.get_min_frequency()
        self.dependency_threshold = self.HeuristicGraphController.get_threshold()
        
        self.__set_slider_values(self.min_frequency,self.dependency_threshold)
        
        self.graph_widget.start_server()
        self.initialized = True
        self.__mine_and_draw()

    # this function is given to the Save Project button. It is called whenever we save the model.
    def getModel(self):
        return self.HeuristicGraphController.getModel()
    
    def __freq_slider_changed(self, value):

        # Update the label with the slider value
        self.freq_slider.setText(f"Min. Frequency: {value}")

        if not self.initialized:
            return
        
        # Redraw graph when value changes
        self.min_frequency = value

        self.__mine_and_draw()
    
    def __thresh_slider_changed(self, value):
        # Update the label with the slider value
        self.thresh_slider.setText(f"Dependency Threshold: {value/100:.2f}")

        if not self.initialized:
            return
        
        # Redraw graph when value changes
        self.dependency_threshold = value/100
    
        self.__mine_and_draw()

    def __set_slider_values(self, min_freq, threshold):
        self.thresh_slider.setText(f"Dependency Threshold: {threshold:.2f}")
        self.freq_slider.setText(f"Min. Frequency: {min_freq}")
        self.thresh_slider.setValue(int(threshold*100))
        self.freq_slider.setValue(min_freq)

    def __mine_and_draw(self):

        '''with graphviz'''
        self.graphviz_graph = self.HeuristicGraphController.create_dependency_graph(self.dependency_threshold,self.min_frequency)

        # Load the image and add it to the QGraphicsScene
        filename = self.workingDirectory + '.dot'
        self.graph_widget.set_source(filename)
        try:
            self.graph_widget.reload()
        except FileNotFoundException as e:
            print(e.message)

    def __ensure_graphviz_graph_exists(self):
        # just to make sure everything works as intended.
        if not self.graphviz_graph:
            print("HeuristicGraphView ERROR: graphviz_graph is NONE.")
            return False
        return True

    def generate_png(self):
        if not self.__ensure_graphviz_graph_exists():
            return
        self.graphviz_graph.render(self.workingDirectory,format = 'png')
        print("heuristic_graph_view: PNG generated")
        return

    def generate_svg(self):
        if not self.__ensure_graphviz_graph_exists():
            return
        self.graphviz_graph.render(self.workingDirectory,format = 'svg')
        print("heuristic_graph_view: SVG generated")

    def generate_dot(self):
        if not self.__ensure_graphviz_graph_exists():
            return
        self.graphviz_graph.render(self.workingDirectory,format = 'dot')
        print("heuristic_graph_view: DOT generated")

    def clear(self):
        self.graph_widget.clear()
        self.dependency_threshold= 0.5
        self.min_frequency = 1
        self.zoom_factor = 1.0
