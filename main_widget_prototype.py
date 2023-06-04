
import sys
from PyQt5.QtWidgets import QStyleFactory, QApplication,QMainWindow 
from custom_ui.d3_html_view import D3HTMLView

# This file is a quicktest file to see how your widget looks like before adding it to the greater project.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 600)

        #------ custom code here ------

        # This is where you add your widget and all the other code you need:
        self.main_Widget = D3HTMLView(self)
        self.main_Widget.start_server()

        #------ end of customized code ------

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
