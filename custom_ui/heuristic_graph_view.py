from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel,QVBoxLayout, QHBoxLayout, QFrame
from algorithms.heuristic_mining import HeuristicMining
from custom_ui.algorithm_view_interface import AlgorithmViewInterface
from custom_ui.d3_html_widget import HTMLWidget
from algorithms.pickle_save import pickle_load
from custom_ui.custom_widgets import SaveProjectButton, ExportButton, CustomQSlider

class HeuristicGraphView(QWidget, AlgorithmViewInterface):
    def __init__(self, parent, saveFolder = "saves/", workingDirectory = 'temp/graph_viz'):
        super().__init__()
        self.parent = parent
        self.initialized = False

        #modifiers and global variables
        self.dependency_threshold = 0.5
        self.min_frequency = 1
        self.max_frequency = 100
        self.saveFolder = saveFolder
        self.workingDirectory = workingDirectory # the working directory is where the graphviz file is stored for display and export
        self.Heuristic_Model = None 
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
        self.Heuristic_Model = HeuristicMining(cases)
        self.max_frequency = self.Heuristic_Model.get_max_frequency()
        self.freq_slider.setRange(1,self.max_frequency)
        self.graph_widget.start_server()
        self.initialized=True
        self.__mine_and_draw()

    # CALL BEFORE USAGE (option 2 for mining existing models)
    def loadModel(self):
        try:
            filename, model = self.__load()
            if model == -1:
                return -1
        except TypeError:
            print("HeuristicGraphView loadModel(): Error: Something went wrong while loading an existing model.")
            return -1
        
        #self.filename= filename
        self.saveProject_button.load_filename(filename)
        self.Heuristic_Model = model
        self.max_frequency = self.Heuristic_Model.get_max_frequency()

        # set the first slider
        self.min_frequency = self.Heuristic_Model.get_min_freq()
        self.freq_slider.setText(f"Min. Frequency: {self.min_frequency}")

        # set the second slider
        self.dependency_threshold = self.Heuristic_Model.get_threshold()
        self.thresh_slider.setText(f"Dependency Threshold: {self.dependency_threshold:.2f}")
        
        # Using setValue triggers valueChanged(). 
        # If the function below setValue, calls a model function,
        # it leads to what I can only assume is undefined behaviour.
        # This bug also only occurs on initial loadModel(). 
        # All consequent loadModel function calls work just fine for some reason.
        # To bypass this weird bug, I call the model functions first BEFORE I setValue() 
        self.freq_slider.setValue(self.min_frequency)
        self.thresh_slider.setValue(int(self.dependency_threshold*100))
        
        self.freq_slider.setRange(1,self.max_frequency)
        self.graph_widget.start_server()
        self.initialized = True
        self.__mine_and_draw()

    # this function is given to the Save Project button. It is called whenever we save the model.
    def getModel(self):
        return self.Heuristic_Model
    
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

    def __load(self):
        
        file_path, _ = QFileDialog.getOpenFileName(None, "Select file", self.saveFolder, "Pickle files (*.pickle)")
        # If the user cancels the file dialog, return
        if not file_path:
            return -1, -1
        return file_path, pickle_load(file_path)

    def __mine_and_draw(self):

        '''with graphviz'''
        self.graphviz_graph = self.Heuristic_Model.create_dependency_graph_with_graphviz(self.dependency_threshold,self.min_frequency)
        
        # generate dot
        self.graphviz_graph.render(self.workingDirectory,format = 'dot')
        print("heuristic_graph_view: CSV mined")

        # Load the image and add it to the QGraphicsScene
        filename = self.workingDirectory + '.dot'
        self.graph_widget.set_source(filename)
        self.graph_widget.reload()

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
