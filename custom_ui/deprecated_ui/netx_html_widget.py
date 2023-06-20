from custom_ui.server_thread import ServerThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import networkx as nx
from dash import dcc, html
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import plotly.graph_objs as go
from flask import Flask
from dash import html, Dash
from dash.dependencies import Input, Output


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
        print('HTMLWidget: ' + data['points'][0]['text'])

    def __draw_graph(self):

        # The following code was referenced from:
        # https://medium.com/kenlok/how-to-draw-an-interactive-network-graph-using-dash-b6b744f60931

        # create networkx graph from dot file
        G = nx.DiGraph(nx.drawing.nx_agraph.read_dot(self.dotFile))

        # get the edges from the graph in the form: ('a', 'b'), 
        edges = [(u, v) for u, v in G.edges()]
        
        # get arrays of the coordinates of node position
        # pos becomes of form: {'a': (140,350),'b':(130,350),...}
        # X has form: {'a': 140, 'b': 130,...}
        # Y looks just like X
        pos = nx.get_node_attributes(G, 'pos')
        pos = {node: tuple(map(float, pos[node].split(','))) for node in pos}
        X = {node: pos[node][0] for node in pos}
        Y = {node: pos[node][1] for node in pos}

        # get array of node sizes
        node_sizes = nx.get_node_attributes(G, 'width')
        node_sizes = {node: str(float(size) * 10) for node, size in node_sizes.items()}

        # Create new Edges
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line = dict(width=0.5,color='#888'),
            hoverinfo = 'none',
            mode ='lines')
        
        for edge in edges:
             outgoing = edge[0]
             incoming = edge[1]
             x0 = X[outgoing]
             y0 = Y[outgoing]
             x1 = X[incoming]
             y1 = Y[incoming]
             edge_trace['x'] += tuple([x0, x1, None])
             edge_trace['y'] += tuple([y0, y1, None])

        # Create new Nodes
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=50,
                colorbar=dict(
                    thickness=25,
                    title='Node Appearance Frequency',
                    xanchor='left',
                    titleside='right'
                ),  
                line=dict(width=2)))
        
        for node in pos.keys():
            x = X[node]
            y = Y[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['marker']['color'] += tuple([float(node_sizes[node])])
            node_trace['text'] += tuple([node])
            #node_trace['text']+=tuple([f"{node}<br>Some additional infotext"])
            #print(tuple([x+y]))
            #print(tuple([float(node_sizes[node])]))
            
        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br> This is an experimental interactive graph view, that can be build upon and used in future extensions.<br>',
                titlefont=dict(size=16),
                dragmode='select', # this is where the default tool is set. 'pan', 'select',...
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        # upload the layout
        dash_layout = html.Div([
                html.Div(dcc.Graph(id='Graph',figure=fig)),
                html.Div(className='row', children=[
                    html.Div([html.H2('Overall Data'),
                              html.P('Num of nodes: ' + str(len(G.nodes))),
                              html.P('Num of edges: ' + str(len(G.edges)))],
                              className='three columns'),
                    html.Div([
                            html.H2('Selected Data'),
                            html.Div(id='selected-data'),
                        ], className='six columns')
                    ])
                ])
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

    def getURL(self):
        return self.server.getURL()
    
    def start_server(self):
        self.server.start()
    
    def shutdown_server(self):
        self.server.shutdown()