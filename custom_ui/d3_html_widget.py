from custom_ui.server_thread import ServerThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from dash import dcc, html
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from flask import Flask
from dash import html, Dash
from dash.dependencies import Input, Output
import dash_interactive_graphviz


class HTMLWidget(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.state = False

        # default variables
        self.dotFile = "temp/graph_viz.dot"

        # Define the widget and its layout
        self.browser = QWebEngineView()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.browser)
        self.setLayout(self.main_layout)
        

    # CALL BEFORE USAGE
    def start_server(self):
        if self.state == True:
            return ''
        
        self.server = HTMLServer(self)
        self.url = self.server.getURL()
        self.browser.setUrl(QUrl(self.url))

        status = self.reload()
        
        self.server.start_server()
        print('server started')
        self.state = True
        return status
    
    def reload(self):
        try:
            self.__draw_graph()
        except FileNotFoundError:
            return f'FileNotFoundError: {self.dotFile} does not exist'
        return ''

    def set_source(self, filepath):
        self.dotFile = filepath

    # This clear shuts down the server and should only be used on exit. Because restarting Threads is not possible.
    def clear(self, var=0):
        # var is not used but during testing, the button to trigger this function required a second argument
        if self.state == False:
            return
        print('shutting down server')
        self.server.shutdown_server()
        self.state = False
    
    # Callback from html. Do something with it.
    def react(self, data):
        print('HTMLWidget: ' + str(data))

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
                    style=dict(display="flex", flexDirection="column"),
                ),
            ],
            style=dict(position="absolute", height="100%", width="100%", display="flex"),
        )
        self.server.change_layout(dash_layout)

class HTMLServer():
    global flask_app
    flask_app = Flask('myapp')
    # App routes defined here
    global dash_app
    dash_app = Dash(__name__, server=flask_app)

    def __init__(self, parentWidget):
        # parent is global, because dash_app callback throws an error if I try to make self a parameter
        global parent
        parent = parentWidget
        global dash_app
        global flask_app

        # Define the layout of the Dash app
        dash_app.layout = html.Div([
            html.H1('Nothing to show')
        ])

        self.server = ServerThread(flask_app, 8050)

    @dash_app.callback(
        [Output("gv", "dot_source"), Output("gv", "engine")],
        [Input("input", "value"), Input("engine", "value")],
    )
    def display_output(value, engine):
        return value, engine
    
    @dash_app.callback(Output("selected", "children"), [Input("gv", "selected")])
    def show_selected(value):
        global parent
        parent.react(value)
        return html.Div(value)
    
    def change_layout(self, layout):
        global dash_app
        dash_app.layout = layout
    
    def getURL(self):
        return self.server.getURL()
    
    def start_server(self):
        self.server.start()
    
    def shutdown_server(self):
        self.server.shutdown()