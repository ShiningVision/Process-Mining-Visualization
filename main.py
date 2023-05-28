# This project was assisted by ChatGPT

import sys
import os
from PyQt5.QtCore import QDir, QFile, QTimer
from PyQt5.QtWidgets import QLabel, QStyleFactory, QApplication, QMainWindow, QStackedWidget, QMessageBox, QFileDialog
from custom_ui.column_selection_view import ColumnSelectionView
from custom_ui.heuristic_graph_view import HeuristicGraphView
from custom_ui.start_view import StartView
from custom_ui.dot_editor_view import DotEditorView
from custom_ui.html_widget import HTMLWidget
from custom_ui.export_view import ExportView

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
        self.startView = StartView(self)

        # Add a view widget for dot edit viewer (.dot Editor)
        self.dotEditorView = DotEditorView(self)

        # Add the experimental interactive HTMLView
        self.htmlView = HTMLWidget(self)

        # Export view
        self.exportView = ExportView(self)

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
        self.mainWidget.addWidget(self.startView)
        self.mainWidget.addWidget(self.columnSelectionView)
        self.mainWidget.addWidget(self.dotEditorView)
        self.mainWidget.addWidget(self.htmlView)
        self.mainWidget.addWidget(self.exportView)

        # Add all the algorithm views
        for view in self.algorithmViews:
            self.mainWidget.addWidget(view)
        
        # Set welcome page as default
        self.startView.load_algorithms(self.algorithms)
        self.mainWidget.setCurrentWidget(self.startView)
        self.setCentralWidget(self.mainWidget)

        # Add a file menu to allow users to upload csv files and so on.
        file_menu = self.menuBar().addMenu("File")
        upload_action_mine_csv = file_menu.addAction("MINE NEW PROCESS FROM CSV")
        upload_action_mine_csv.triggered.connect(self.switch_to_column_selection_view)
        edit_dot = file_menu.addAction("Edit dot file")
        edit_dot.triggered.connect(self.switch_to_dot_editor)
        interactive_graph = file_menu.addAction("Experimental interactive graph view")
        interactive_graph.triggered.connect(self.switch_to_html_view)
        export = file_menu.addAction("Export")
        export.triggered.connect(self.switch_to_export_view)


        #create a status Bar to display quick notifications
        self.statusBar()

        # Set the window title and show the window
        self.setWindowTitle("Graph Viewer")
        self.show()

    # gets called by start_view.py 'create new process' button
    # opens Column Selection View
    def switch_to_column_selection_view(self):

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

    def switch_to_export_view(self):
        if not self.img_generated:
            popup = QMessageBox(self)
            popup.setText("Nothing to export. Please mine a model.")

            close_button = popup.addButton("Close", QMessageBox.AcceptRole)
            close_button.clicked.connect(popup.close)

            # Show the pop-up message
            popup.exec_()

            return
        
        self.exportView.load_algorithm(self.algorithmViews[self.current_Algorithm])
        self.mainWidget.setCurrentWidget(self.exportView)
 
    def switch_to_dot_editor(self):
        loaded = self.dotEditorView.load_file()
        if loaded:
            self.img_generated = True
            self.mainWidget.setCurrentWidget(self.dotEditorView)

    def switch_to_html_view(self):
        errorMessage = self.htmlView.start_server()
        if errorMessage != '':
            self.show_pop_up_message(errorMessage)
            return
        self.mainWidget.setCurrentWidget(self.htmlView)

    # used in export_view.py After export the view should return to the algorithm
    def switch_to_view(self, view):
        self.mainWidget.setCurrentWidget(view)

    # Column Selection View 'Cancel Selection' uses this 
    def switch_to_start_view(self):
        self.mainWidget.setCurrentWidget(self.startView)
        self.__reset_canvas()

    def mine_process(self, filepath, cases, algorithm = 0):

        try:
            index = self.algorithmViews[algorithm]
        except IndexError:
            print("main.py: ERROR Algorithm with index "+str(algorithm)+" not defined!")
            return
        
        self.__reset_canvas()
        self.current_Algorithm = algorithm
        self.algorithmViews[algorithm].startMining(filepath, cases)
        self.img_generated = True
        self.mainWidget.setCurrentWidget(self.algorithmViews[algorithm])
    
    # shows a quick status update/warning
    def show_pop_up_message(self, message):
        duration = 3000
        # create a QLabel widget and set its text
        label = QLabel(message, self)

        # set the label's properties (background color, text color, etc.)
        label.setAutoFillBackground(True)
        label.setStyleSheet('background-color: #ffff99; color: #333333; padding: 5px; border-radius: 3px;')

        # add the label to the status bar
        self.statusBar().addWidget(label)

        # create a timer to hide the label after the specified duration
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.__msg_timeout(label)) # use a lambda function to delete the label
        timer.start(duration)

    # used by BottomOperationInterfaceLayoutWidget
    def mine_existing_process(self, algorithm):
        try:
            filepath, cases = self.__load()
        except TypeError:
            return
        
        self.mine_process(filepath, cases, algorithm)

    def __load(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Select file", "saves/", "Text files (*.txt)")

        # If the user cancels the file dialog, return
        if not file_path:
            return
        
        # Convert the txt content back to array
        with open(file_path, "r") as f:
            array = []
            for line in f:
                array.append(line.strip().split(','))
        return file_path, array

    def __msg_timeout(self, label):
        self.statusBar().removeWidget(label)

    def __reset_canvas(self):
        self.dotEditorView.clear()
        #self.startView.clear()
        self.columnSelectionView.clear()
        self.htmlView.clear()
        for view in self.algorithmViews:
            view.clear()
    
    # overwrite closeEvent function
    def closeEvent(self, event):
        self.htmlView.clear() # It is important to shut down the html server. The rest of this function is not necessary
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion')) # table header coloring won't work on windows style.
    window = MainWindow()
    sys.exit(app.exec_())
