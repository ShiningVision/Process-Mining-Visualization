from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem, QWidget, QVBoxLayout
import csv

class ColumnSelectionView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        #assign default labels
        self.timeLabel = ""
        self.caseLabel = ""
        self.eventLabel = ""
        self.selected_column = 0

        self.table = QTableWidget(self)
        self.table.setGeometry(QRect(10, 10, 580, 280))
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().sectionClicked.connect(self.column_header_clicked)

        self.column_selector = QComboBox(self)
        self.column_selector.setGeometry(QRect(10, 300, 200, 30))
        self.column_selector.currentIndexChanged.connect(self.__column_selected)

        self.timeColumn_button = QPushButton('Assign to Timestamp', self)
        self.timeColumn_button.setGeometry(QRect(220, 300, 150, 30))
        self.timeColumn_button.clicked.connect(self.__assign_timeColumn)

        self.caseColumn_button = QPushButton('Assign to Case', self)
        self.caseColumn_button.setGeometry(QRect(380, 300, 150, 30))
        self.caseColumn_button.clicked.connect(self.__assign_caseColumn)

        self.eventColumn_button = QPushButton('Assign to Event', self)
        self.eventColumn_button.setGeometry(QRect(540, 300, 150, 30))
        self.eventColumn_button.clicked.connect(self.__assign_eventColumn)

        self.start_import_button = QPushButton('Start Import', self)
        self.start_import_button.setGeometry(QRect(10, 340, 580, 30))
        self.start_import_button.clicked.connect(self.__start_import)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.column_selector)
        layout.addWidget(self.caseColumn_button)
        layout.addWidget(self.eventColumn_button)
        layout.addWidget(self.timeColumn_button)
        layout.addWidget(self.start_import_button)

    def load_csv(self, filepath):
        with open(filepath, 'r') as file:
            # use csv.Sniffer() to try to detect the delimiter
            dialect = csv.Sniffer().sniff(file.read(1024))
            
            # reset the file pointer to the beginning of the file
            file.seek(0)
            
            # create a CSV reader using the detected dialect
            reader = csv.reader(file, dialect)

            headers = next(reader)
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            self.column_selector.addItems(headers)
            for row_index, row_data in enumerate(reader):
                self.table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(col_data))

    def column_header_clicked(self, index):
        self.column_selector.setCurrentIndex(index)
        self.selected_column = index
    
    def __column_selected(self, index):
        self.selected_column = index

    def __assign_timeColumn(self):
        self.timeLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.timeLabel + " assigned as time column")

    def __assign_caseColumn(self):
        self.caseLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.caseLabel + " assigned as case column")

    def __assign_eventColumn(self):
        self.eventLabel = self.table.horizontalHeaderItem(self.selected_column).text()
        print(self.eventLabel + " assigned as event column")

    def clear(self):
        self.timeLabel = ""
        self.caseLabel = ""
        self.eventLabel = ""
        self.selected_column = 0
        self.column_selector.clear()

    def __start_import(self):
        msgBox = QMessageBox()
        msgBox.setText("Time label is "+self.timeLabel+"\n"+"Case label is "+self.caseLabel+"\n"+"Event label is "+self.eventLabel)
        msgBox.setInformativeText("Are these columns correct?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        ret = msgBox.exec_()

        if ret == QMessageBox.Cancel:
            return
        
        self.parent.display_mining_result(self.timeLabel, self.caseLabel, self.eventLabel)
    
