import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from custom_ui.custom_widgets import CustomQComboBox

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