from PyQt5.QtCore import Qt, QDir, QFile
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QFileDialog
from custom_ui.custom_widgets import PNGViewer, CustomQComboBox
import os
class ExportView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.png_path = 'temp/graph_viz.png'
        self.algorithmView = None
        self.supported_formats = ['PNG','SVG','DOT']
        main_layout = QHBoxLayout()
        self.leftside = PNGViewer()

        self.leftside.setScene(self.png_path)

        self.rightside = QVBoxLayout()

        self.return_button = QPushButton('Back')
        self.return_button.setFixedSize(80, 40)
        self.return_button.clicked.connect(self.__return_to_previous_view)

        self.selected_format = 0
        self.format_selector = CustomQComboBox()
        self.format_selector.setFixedSize(120, 20)
        self.__load_formats()
        self.format_selector.currentIndexChanged.connect(self.__format_selected)

        self.export_button = QPushButton("EXPORT")
        self.export_button.setFixedSize(180, 70)
        self.export_button.setStyleSheet("background-color: rgb(30, 144, 255)")
        self.export_button.clicked.connect(self.__export)

        self.rightside.addWidget(self.return_button)
        self.rightside.addWidget(self.format_selector)
        self.rightside.addWidget(self.export_button)

        main_layout.addWidget(self.leftside)
        main_layout.addLayout(self.rightside)

        self.setLayout(main_layout)

    # CALL BEFORE USAGE
    def load_algorithm(self, algorithmView):
        self.algorithmView = algorithmView

        # refresh the scene
        self.leftside.setScene(self.png_path)

    def __load_formats(self):
        for element in self.supported_formats:
            self.format_selector.addItem(element)

    def __format_selected(self, index):
        self.selected_format = index
        self.format_selector.setCurrentIndex(index)

    def __return_to_previous_view(self):
        self.parent.switch_to_view(self.algorithmView)

    def __export(self):
        if self.selected_format == 0:
            self.export_current_image_as_png()
        elif self.selected_format == 1:
            self.export_current_image_as_svg()
        elif self.selected_format == 2:
            self.export_current_image_as_dot()
        else:
            print("export_view: ERROR Invalid export format selected")
            return
        #back to the last page
        self.__return_to_previous_view()

    def export_current_image_as_png(self):

        #This is the name the graphviz library saves its png as by default.
        file_name = 'graph_viz.png'

        # Current algorithm should generate a svg in temp now.
        self.algorithmView.generate_png()

        self.__save_file(file_name)

    def export_current_image_as_svg(self):

        #This is the name the graphviz library saves its svg as by default.
        file_name = 'graph_viz.svg'
        # Current algorithm should generate a svg in temp now.
        self.algorithmView.generate_svg()

        self.__save_file(file_name)

    def export_current_image_as_dot(self):

        #This is the name the graphviz library saves its dot as by default.
        file_name = 'graph_viz.dot'
        # Current algorithm should generate a svg in temp now.
        self.algorithmView.generate_dot()
        
        self.__save_file(file_name)

    def __save_file(self, file_name):
        # Open a file dialog to allow users to select a folder
        source_folder = QDir.currentPath() + '/temp'
        filename = QFileDialog.getSaveFileName(
            self, "Save File", file_name)
        # Copy the file from the source folder to the destination folder
        source_file_path = os.path.join(source_folder, file_name)
        destination_file_path = filename[0]#os.path.join(destination_folder, file_name)
        if QFile.exists(destination_file_path):
            QFile.remove(destination_file_path)
        QFile.copy(source_file_path, destination_file_path)