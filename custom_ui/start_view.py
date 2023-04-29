import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StartView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # set up algorithm selector combo box
        self.selected_algorithm = 0
        self.algorithm_selector = QComboBox(self)
        self.algorithm_selector.setFixedSize(120, 20)
        self.algorithm_selector.currentIndexChanged.connect(self.__algorithm_selected)

        # Welcome text
        self.figure = plt.figure(figsize=(50, 50))
        welcome_text = "This is a process mining tool.\nIt can create nice looking graphs out of CSV files!"
        plt.text(0.5, 0.5, welcome_text, fontsize=24, ha='center', va='center')
        plt.axis('off')
        self.canvas = FigureCanvas(self.figure)

        # Two buttons 'LOAD EXISTING PROCESS' 'MINE NEW PROCESS FROM CSV'
        load_button = QPushButton("LOAD EXISTING PROCESS")
        load_button.setFixedSize(150, 70)
        load_button.setStyleSheet("background-color: rgb(0, 128, 0)")
        load_button.clicked.connect(self.load_existing_process)

        mine_button = QPushButton("MINE NEW PROCESS FROM CSV")
        mine_button.setFixedSize(180, 70)
        mine_button.setStyleSheet("background-color: rgb(30, 144, 255)")
        mine_button.clicked.connect(self.mine_new_process)

        # QHBoxLayout for Loading existing process
        load_process_layout = QHBoxLayout()
        load_process_layout.addWidget(self.algorithm_selector)
        load_process_layout.addWidget(load_button)

        # QHBoxLayout with two buttons side by side
        button_layout = QHBoxLayout()
        button_layout.addLayout(load_process_layout)
        button_layout.addWidget(mine_button)

        # QVBoxLayout with welcome text on top and QHBoxLayout with buttons below
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_algorithms(self, array):
        for element in array:
            self.algorithm_selector.addItem(element)

    def load_existing_process(self):
        self.parent.start_mine_txt(self.selected_algorithm)

    def mine_new_process(self):
        self.parent.mine_csv()
        
    def __algorithm_selected(self, index):
        self.algorithm_selector.setCurrentIndex(index)
        self.selected_algorithm = index

    def clear(self):
        self.algorithm_selector.clear()