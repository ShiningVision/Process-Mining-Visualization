import networkx as nx
from graphviz import Digraph
import numpy as np

class HeuristicMining():
    def __init__(self, log):
        self.log = log
        self.events = self.__filter_out_all_events()
        self.succession_matrix = self.__create_succession_matrix()
        self.dependency_matrix = self.__create_dependency_matrix()
        self.edge_thickness_amplifier = 1.5

    def create_dependency_graph_with_networkx(self, dependency_treshhold, min_frequency):
        dependency_graph = self.__create_dependency_graph(dependency_treshhold, min_frequency)
        G = nx.DiGraph()
        G.add_nodes_from(self.events)
        edgelist = []
        for x in range(len(dependency_graph)):
            for y in range(len(dependency_graph[0])):
                if(dependency_graph[x][y]!=0):
                    edgelist.append((self.events[x],self.events[y], {'weight':self.succession_matrix[x][y] }))
        G.add_edges_from(edgelist)
        return G
    
    def create_dependency_graph_with_graphviz(self, dependency_treshhold, min_frequency):
        dependency_graph = self.__create_dependency_graph(dependency_treshhold, min_frequency)
        
        # create graph
        graph = Digraph()

        # add nodes to graph
        for node in self.events:
            graph.node(node)

        graph.node
        # add edges to graph
        for i in range(len(self.events)):
            for j in range(len(self.events)):
                if dependency_graph[i][j] == 1.:
                    edge_thickness = self.dependency_matrix[i][j]/dependency_treshhold * self.edge_thickness_amplifier
                    graph.edge(self.events[i], self.events[j], penwidth = str(edge_thickness))

        #make start node look nice
        start_node = self.__get_start_node()
        graph.node(start_node, shape='doublecircle', style='filled',fillcolor='green')

        #make end node look nice
        end_node = self.__get_end_node()
        graph.node(end_node, shape='doublecircle', style='filled',fillcolor='red')
            
        return graph

    def __filter_out_all_events(self):
        dic = {}
        for trace in self.log:
            for activity in trace:
                if activity in dic:
                    dic[activity] = dic[activity]+1
                else:
                    dic[activity] = 1

        activities = list(dic.keys())
        return activities

    def __create_succession_matrix(self):
        succession_matrix = np.zeros((len(self.events),len(self.events)))
        for trace in self.log:
            index_x = -1
            for element in trace:
                
                if index_x <0:
                    index_x +=1
                    continue
                x = self.events.index(trace[index_x])
                y = self.events.index(element)
                succession_matrix[x][y]+=1
                index_x +=1
        return succession_matrix
    
    def __get_start_node(self):
        #start node is the node where an entire column in the succession_matrix is 0.
        for column in range(len(self.succession_matrix)):
            incoming_edges = 0
            for row in range(len(self.succession_matrix)):
                if self.succession_matrix[row][column] != 0:
                    incoming_edges +=1
            if incoming_edges == 0:
                return self.events[column]
        #if there are no start nodes (which should not happen), add one to signify the problem.
        return 'start'
        
    
    def __get_end_node(self):
        #end node is the node where an entire row in the succession_matrix is 0.
        for row in range(len(self.succession_matrix)):
            outgoing_edges = 0
            for column in range(len(self.succession_matrix)):
                if self.succession_matrix[row][column] != 0:
                    outgoing_edges +=1
            if outgoing_edges == 0:
                return self.events[row]
        #if there are no end nodes (which should also not happen), add one to signify the problem.
        return 'end'

    def __create_dependency_matrix(self):
        dependency_matrix = np.zeros(self.succession_matrix.shape)
        y = 0
        for row in self.succession_matrix:
            x = 0
            for i in row:
                if x == y:
                    dependency_matrix[x][y] = self.succession_matrix[x][y]/(self.succession_matrix[x][y]+1)
                else:
                    dependency_matrix[x][y] = (self.succession_matrix[x][y]-self.succession_matrix[y][x])/(self.succession_matrix[x][y]+self.succession_matrix[y][x]+1)
                x+=1
            y+=1
        return dependency_matrix

    def __create_dependency_graph(self, dependency_treshhold, min_frequency):
        dependency_graph = np.zeros(self.dependency_matrix.shape)
        y = 0
        for row in dependency_graph:
            for x in range(len(row)):
                if self.dependency_matrix[y][x] >= dependency_treshhold and self.succession_matrix[y][x] >= min_frequency:
                    dependency_graph[y][x]+= 1          
            y+=1

        return dependency_graph