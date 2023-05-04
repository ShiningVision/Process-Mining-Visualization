# This project was assisted by ChatGPT

import sys
import os
from PyQt5.QtCore import QDir, QFile
from PyQt5.QtWidgets import QStyleFactory, QApplication, QMainWindow, QStackedWidget, QMessageBox, QFileDialog
from custom_ui.column_selection_view import ColumnSelectionView
from custom_ui.heuristic_graph_view import HeuristicGraphView
from custom_ui.start_view import StartView
from custom_ui.html_view import HTMLView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set default window size
        self.setMinimumSize(1200, 600)

        # global variables with default values
        self.img_generated = False
        self.filepath = None
        self.current_Algorithm = 0

        # Add a view widget for the homepage
        self.welcomeView = StartView(self)

        # Add a view widget for html viewer (.dot Editor)
        self.htmlView = HTMLView(self)

        # Add a view widget for assigning the necessary column-labels of the csv
        self.columnSelectionView = ColumnSelectionView(self)

        # Add a view widget for diplaying heuristic graphs
        self.heuristicGraphView = HeuristicGraphView(self)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ADD YOUR ALGORITHM HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # ADD NEW ALGORITHM NAME IN THIS algorithms ARRAY
        # Create your algorithm view page like the heuristicGraphView above.
        # AND THEN append() YOUR ALGORITHMVIEW TO THE algorithmViews ARRAY
        # MAKE SURE THE INDEXING of both arrays match.
        self.algorithms = ["Heuristic Mining"]
        self.algorithmViews = []
        self.algorithmViews.append(self.heuristicGraphView)

        # Create a main widget that is stacked and can change depending on the needs
        self.mainWidget = QStackedWidget(self)
        self.mainWidget.addWidget(self.welcomeView)
        self.mainWidget.addWidget(self.columnSelectionView)
        self.mainWidget.addWidget(self.htmlView)

        # Add all the algorithm views
        for view in self.algorithmViews:
            self.mainWidget.addWidget(view)
        
        # Set welcome page as default
        self.welcomeView.load_algorithms(self.algorithms)
        self.mainWidget.setCurrentWidget(self.welcomeView)
        self.setCentralWidget(self.mainWidget)

        # Add a file menu to allow users to upload csv files and so on.
        file_menu = self.menuBar().addMenu("File")
        upload_action_mine_csv = file_menu.addAction("MINE NEW PROCESS FROM CSV")
        edit_dot = file_menu.addAction("Edit dot file")
        export_current_image_png = file_menu.addAction("Export png")
        export_current_image_svg = file_menu.addAction("Export svg")
        export_current_image_dot = file_menu.addAction("Export dot")
        upload_action_mine_csv.triggered.connect(self.mine_new_process)
        export_current_image_png.triggered.connect(self.export_current_image_as_png)
        export_current_image_svg.triggered.connect(self.export_current_image_as_svg)
        export_current_image_dot.triggered.connect(self.export_current_image_as_dot)
        edit_dot.triggered.connect(self.view_html)

        # Set the window title and show the window
        self.setWindowTitle("Graph Viewer")
        self.show()

    # gets called by start_view.py 'create new process' button
    # opens Column Selection View
    def mine_new_process(self):

        # Open a file dialog to allow users to select a CSV file
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV files (*.csv)")

        # If the user cancels the file dialog, return
        if not filename:
            return

        self.filepath = filename

        # Change to Column Selection View
        self.__reset_canvas()
        self.columnSelectionView.load_csv(self.filepath)
        self.columnSelectionView.load_algorithms(self.algorithms)
        self.mainWidget.setCurrentWidget(self.columnSelectionView)

    def export_current_image_as_png(self):
        # if there is no image, warn with a pop up and return.
        if not self.img_generated:
            popup = QMessageBox(self)
            popup.setText("Nothing to export. Please mine a model.")

            close_button = popup.addButton("Close", QMessageBox.AcceptRole)
            close_button.clicked.connect(popup.close)

            # Show the pop-up message
            popup.exec_()

            return

        # Open a file dialog to allow users to select a folder
        source_folder = QDir.currentPath() + '/temp'
        destination_folder = QFileDialog.getExistingDirectory(
            self, "Select a folder", QDir.currentPath())

        file_name = 'graph_viz.png'

        # Current algorithm should generate a png in temp now.
        self.algorithmViews[self.current_Algorithm].generate_png()
        # Copy the file from the source folder to the destination folder
        source_file_path = os.path.join(source_folder, file_name)
        destination_file_path = os.path.join(destination_folder, file_name)
        QFile.copy(source_file_path, destination_file_path)

    def export_current_image_as_svg(self):
        # if there is no image, warn with a pop up and return.
        if not self.img_generated:
            popup = QMessageBox(self)
            popup.setText("Nothing to export. Please mine a model.")

            close_button = popup.addButton("Close", QMessageBox.AcceptRole)
            close_button.clicked.connect(popup.close)

            # Show the pop-up message
            popup.exec_()

            return

        # Open a file dialog to allow users to select a folder
        source_folder = QDir.currentPath() + '/temp'
        destination_folder = QFileDialog.getExistingDirectory(
            self, "Select a folder", QDir.currentPath())

        file_name = 'graph_viz.svg'
        # Current algorithm should generate a svg in temp now.
        self.algorithmViews[self.current_Algorithm].generate_svg()
        # Copy the file from the source folder to the destination folder
        source_file_path = os.path.join(source_folder, file_name)
        destination_file_path = os.path.join(destination_folder, file_name)
        QFile.copy(source_file_path, destination_file_path)

    def export_current_image_as_dot(self):
            # if there is no image, warn with a pop up and return.
            if not self.img_generated:
                popup = QMessageBox(self)
                popup.setText("Nothing to export. Please mine a model.")

                close_button = popup.addButton("Close", QMessageBox.AcceptRole)
                close_button.clicked.connect(popup.close)

                # Show the pop-up message
                popup.exec_()

                return

            # Open a file dialog to allow users to select a folder
            source_folder = QDir.currentPath() + '/temp'
            destination_folder = QFileDialog.getExistingDirectory(
                self, "Select a folder", QDir.currentPath())

            file_name = 'graph_viz.dot'
            # Current algorithm should generate a svg in temp now.
            self.algorithmViews[self.current_Algorithm].generate_dot()
            # Copy the file from the source folder to the destination folder
            source_file_path = os.path.join(source_folder, file_name)
            destination_file_path = os.path.join(destination_folder, file_name)
            QFile.copy(source_file_path, destination_file_path)

    def view_html(self):
        loaded = self.htmlView.load_file()
        if loaded:
            self.img_generated = True
            self.mainWidget.setCurrentWidget(self.htmlView)

    def mine_process(self, cases, algorithm = 0):

        try:
            index = self.algorithmViews[algorithm]
        except IndexError:
            print("main.py: ERROR Algorithm with index "+str(algorithm)+" not defined!")
            return
        
        self.__reset_canvas()
        self.current_Algorithm = algorithm
        self.algorithmViews[algorithm].startMining(cases)
        self.img_generated = True
        self.mainWidget.setCurrentWidget(self.algorithmViews[algorithm])

    def __reset_canvas(self):
        self.htmlView.clear()
        self.welcomeView.clear()
        self.columnSelectionView.clear()
        for view in self.algorithmViews:
            view.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion')) # table header coloring won't work on windows style.
    window = MainWindow()
    sys.exit(app.exec_())
