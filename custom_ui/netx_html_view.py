from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from custom_ui.netx_html_widget import HTMLWidget

class NetXHTMLView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.algorithmView = None # optional for getting back to a previous view

        main_layout = QVBoxLayout()
        self.html_widget = HTMLWidget(self)

        self.return_button = QPushButton('Back')
        self.return_button.setFixedSize(80, 40)
        self.return_button.clicked.connect(self.__return_to_previous_view)

        main_layout.addWidget(self.html_widget)
        main_layout.addWidget(self.return_button)

        self.setLayout(main_layout)

    # CALL BEFORE USAGE
    def start_server(self):
        return self.html_widget.start_server()
    
    def load_algorithm(self, algorithmView):
        self.algorithmView = algorithmView

    def clear(self):
        self.html_widget.clear()

    def __return_to_previous_view(self):
        if not self.algorithmView:
            self.parent.switch_to_start_view()
        else:
            self.parent.switch_to_view(self.algorithmView)