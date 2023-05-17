import sys
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from flask import Flask, request
from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import subprocess
# Create a Flask app
flask_app = Flask(__name__)

# Create a Dash app
dash_app = dash.Dash(__name__, server=flask_app)

# Define the layout of the Dash app
dash_app.layout = html.Div([
    dcc.Graph(id='example-graph', figure={
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    })
])

# Define a callback function for the Dash app
@dash_app.callback(Output('example-graph', 'figure'), [Input('example-graph', 'clickData')])
def update_graph(clickData):
    if clickData:
        print(clickData)
    return {'data': []}


# Create a PyQT5 desktop application
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 600)
        # Create a QWebEngineView widget
        self.browser = QWebEngineView()
        self.main_layout = QVBoxLayout()
        self.button = QPushButton()
        self.button.clicked.connect(self.shutdown)
        self.main_layout.addWidget(self.browser)
        self.main_layout.addWidget(self.button)
        self.main_Widget = QWidget()
        self.main_Widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_Widget)
        self.show()
        

        # Load the local server running the Dash app
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))

    def shutdown(self):
        global server
        server.shutdown()
        
from threading import Thread
from werkzeug.serving import make_server

class ServerThread(Thread):

    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    global server
    server = ServerThread(flask_app)
    server.start()
    # try:
    #     t = Thread(target=lambda: flask_app.run(host='127.0.0.1', port=5000, debug=True, use_reloader = False))
    #     t.start()
    # except Exception as e:
    #     print("Error starting Flask app thread:", e)

    # Create a PyQT5 application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    #I am running out of ideas of how to properly shutdown the server.
    #request.environ.get('werkzeug.server.shutdown') returns None. So it does can't be executed to shut down the server
    # I managed to do it with ServerThread

    # Run the application event loop until sys.exit() is called
    sys.exit(app.exec_())