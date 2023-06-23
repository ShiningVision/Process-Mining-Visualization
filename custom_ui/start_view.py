import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg') # When I tested the project on ubuntu, there was a conflict between Qt5Agg and tkAgg. Program did not run.
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StartView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Welcome text
        self.figure = plt.figure(figsize=(50, 50))
        welcome_text = "This is a process mining tool.\nIt can create nice looking graphs out of CSV files!"
        plt.text(0.5, 0.5, welcome_text, fontsize=24, ha='center', va='center')
        plt.axis('off')
        self.canvas = FigureCanvas(self.figure)

        # Wrap together the Welcome Text and the 2 buttons
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def clear(self):
        return