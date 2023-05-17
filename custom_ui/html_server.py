from threading import Thread
from werkzeug.serving import make_server
from flask import Flask
from dash import html, Dash
from dash.dependencies import Input, Output


# It is important to declare the thread global, so it can be referenced from anywhere.
# Declare the ServerThread global like this:
# global server
# server = ServerThread(app)
# server.start()
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

        self.server = ServerThread(flask_app)

    @dash_app.callback(Output('selected-data', 'children'),[Input('Graph','selectedData')])
    def display_selected_data(selectedData):
        if not selectedData:
            return
        num_of_nodes = len(selectedData['points'])
        text = [html.P('Num of nodes selected: '+str(num_of_nodes))]
        #for x in selectedData['points']:
            #material = int(x['text'].split('<br>')[0][10:])
            #text.append(html.P(str(material)))
        global parent
        parent.react(selectedData)
        return text
    
    def change_layout(self, layout):
        global dash_app
        dash_app.layout = layout
    
    def start_server(self):
        self.server.start()
    
    def shutdown_server(self):
        self.server.shutdown()