import os
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QDir, QFile, QTimer, QUrl
from PyQt5.QtWidgets import QLabel, QStyleFactory, QApplication,QVBoxLayout,QPushButton,QWidget, QMainWindow, QStackedWidget, QMessageBox, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from custom_ui.column_selection_view import ColumnSelectionView
from custom_ui.heuristic_graph_view import HeuristicGraphView
from custom_ui.start_view import StartView
from custom_ui.dot_editor_view import HTMLView
from custom_ui.export_view import ExportView
from custom_ui.html_widget import HTMLWidget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 600)
        # Create a QWebEngineView widget
        self.main_Widget = HTMLWidget(self)
        self.main_Widget.start_server()
        

        self.setCentralWidget(self.main_Widget)
        self.show()
    
    def closeEvent(self, event):
        self.main_Widget.clear()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion')) # table header coloring won't work on windows style.
    window = MainWindow()
    sys.exit(app.exec_())
