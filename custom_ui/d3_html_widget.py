from api.custom_error import FileNotFoundException
from custom_ui.server_thread import ServerThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSignal,QObject
from flask import Flask
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import dash_interactive_graphviz

# This HTMLWidget displays a dot file as an interactive graph 
class HTMLWidget(QWidget):
    react_signal = pyqtSignal(str, str)
    def __init__(self, parent, dotFile = "temp/graph_viz.dot"):
        super().__init__()
        self.parent = parent
        self.state = False

        # default variables
        self.dotFile = dotFile

        # Define the widget and its layout
        self.browser = QWebEngineView()
        self.react_signal.connect(self.react)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.browser)
        
        self.setLayout(self.main_layout)
        

    # CALL BEFORE USAGE
    def start_server(self, port = 8050):
        if self.state == True:
            return ''
        
        self.server = HTMLServer(self, port)
        self.server.react_signal.connect(self.react)
        self.url = self.server.getURL()
        
        self.browser.setUrl(QUrl(self.url))
        
        self.reload()
        
        self.server.start_server()
        print('server started. Running on '+ str(self.url))
        self.state = True
    
    def reload(self):
        try:
            self.__draw_graph()
            self.browser.reload()
        except FileNotFoundError:
            raise FileNotFoundException(f'{self.dotFile} does not exist')

    # if the default path is wrong
    def set_source(self, filepath):
        self.dotFile = filepath

    # This clear shuts down the server and should only be used on exit. Because restarting Threads is not possible.
    def clear(self, var=0):
        # var is not used, but during testing the button to trigger this function required a second argument
        if self.state == False:
            return
        print('shutting down server')
        self.server.shutdown_server()
        self.state = False
    
    # Callback from html. Do something with it.
    def react(self, data):
        print('HTMLWidget: ' + str(data))
        if not data:
            return
        self.__show_detail_in_popup(str(data))

    def __show_detail_in_popup(self, data):

        popup = QMessageBox()
        popup.setText(data)
        popup.setWindowTitle("Selected Node")
        popup.setStandardButtons(QMessageBox.Close)
        popup.exec_()

    def __draw_graph(self):

        with open(self.dotFile, 'r') as file:
            initial_dot_source = file.read()

        # upload the layout
        dash_layout =  html.Div(
            [
                html.Div(
                    dash_interactive_graphviz.DashInteractiveGraphviz(id="gv"),
                    style=dict(flexGrow=1, position="relative"),
                ),
                html.Div(
                    [
                        html.H3("Selected element"),
                        html.Div(id="selected"),
                        html.H3("Dot Source"),
                        dcc.Textarea(
                            id="input",
                            value=initial_dot_source,
                            style=dict(flexGrow=1, position="relative"),
                        ),
                        html.H3("Engine"),
                        dcc.Dropdown(
                            id="engine",
                            value="dot",
                            options=[
                                dict(label=engine, value=engine)
                                for engine in [
                                    "dot",
                                    "fdp",
                                    "neato",
                                    "circo",
                                    "osage",
                                    "patchwork",
                                    "twopi",
                                ]
                            ],
                        ),
                    ],
                    style=dict(display="none", flexDirection="column"),
                ),
            ],
            style=dict(position="absolute", height="100%", width="100%", display="flex"),
        )
        
        self.server.change_layout(dash_layout)

class HTMLServer(QObject):
    react_signal = pyqtSignal(object)
    def __init__(self, parentWidget, port = 8050):
        super().__init__()
        # parent is global, because dash_app callback throws an error if I try to make self a parameter
        self.parent = parentWidget
        self.flask_app = Flask('myapp')
        self.dash_app = Dash(__name__, server=self.flask_app)

        # Define the layout of the Dash app
        self.dash_app.layout = html.Div([
            html.H1('Nothing to show')
        ])

        self.server = ServerThread(self.flask_app, port)

    def register_callbacks(self):
        @self.dash_app.callback(
            [Output("gv", "dot_source"), Output("gv", "engine")],
            [Input("input", "value"), Input("engine", "value")],
        )
        def display_output(value, engine):
            return value, engine
    
        @self.dash_app.callback(Output("selected", "children"), [Input("gv", "selected")])
        def show_selected(value):
            self.react_signal.emit(value)
            return html.Div(value)
    
    def change_layout(self, layout):
        self.dash_app.layout = layout
    
    def getURL(self):
        return self.server.getURL()
    
    def start_server(self):
        self.server.start()
        self.register_callbacks()
    
    def shutdown_server(self):
        self.server.shutdown()