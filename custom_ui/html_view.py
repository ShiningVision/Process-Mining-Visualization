from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QPushButton, QVBoxLayout, QTextEdit, QLabel
import subprocess
from custom_ui.custom_widgets import PNGViewer

class HTMLView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.png_path = 'temp/graph_viz.png'
        self.filepath = None
        
        # The HTML editor has a button called 'refresh' that calls __refresh_png()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.__refresh_png)

        # Create a QTextEdit widget to display the DOT file as plain text
        self.text_editor = QTextEdit(self)

        self.png_viewer = PNGViewer()

        self.html_layout = QVBoxLayout()
        self.html_layout.addWidget(QLabel("Experimental .dot editor"))
        self.html_layout.addWidget(self.text_editor)
        self.html_layout.addWidget(self.refresh_button)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.html_layout)
        self.main_layout.addWidget(self.png_viewer)

        self.setLayout(self.main_layout)

    def __refresh_png(self):
        #the changes in HTML editor are saved.
        new_dot_content = self.text_editor.toPlainText()
        with open(self.filepath, "w") as f:
            f.write(new_dot_content)
        print("File saved")

        self.__dot_to_png()
        self.png_viewer.setScene(self.png_path)

    def load_file(self):
        self.filepath, _ = QFileDialog.getOpenFileName(None, "Select file", "", "Dot files (*.dot)")
        if not self.filepath:
            return 0
                # Load the DOT file into a string
        with open(self.filepath, "r") as f:
            dot_content = f.read()

        self.text_editor.setPlainText(dot_content)

        self.__dot_to_png()

        self.png_viewer.setScene(self.png_path)

        return 1
    
    def clear(self):
        self.text_editor.clear()
        self.filepath = None

    #generate the png used to display the graph
    def __dot_to_png(self):
        subprocess.call(["dot", "-Tpng", self.filepath, "-o", self.png_path])