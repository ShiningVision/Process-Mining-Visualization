
import sys
import pydot
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    
        # Set up the user interface
        self.figure = plt.figure(figsize=(10, 10))
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)

        # Add a file menu to allow users to upload a CSV file
        file_menu = self.menuBar().addMenu("File")
        upload_action_dot = file_menu.addAction("Upload DOT File")
        upload_action_dot.triggered.connect(self.upload_dot)


        # Set the window title and show the window
        self.setWindowTitle("Graph Viewer")
        self.show()
    
    def upload_dot(self):
        # Open a file dialog to allow users to select a DOT file
        filename, _ = QFileDialog.getOpenFileName(self, "Open DOT File", "", "DOT files (*.dot)")

        # If the user cancels the file dialog, return
        if not filename:
            return

        graph = pydot.graph_from_dot_file(filename)
        nx_graph = nx.nx_pydot.from_pydot(graph[0])
        self.figure.clear()
        nx.draw_networkx(nx_graph, with_labels=True)
        self.canvas.draw()

        print("DOT uploaded")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

