from .causal_net import CausalNet
import networkx as nx
import numpy as np

class HeuristicMining():
    def __init__(self, log):
        self.log = log
        self.events = self.__filter_out_all_events()
        self.succession_matrix = self.__create_succession_matrix()
        self.dependency_matrix = self.__create_dependency_matrix()

    def mine(self, dependency_treshhold, min_frequency):
        dependency_graph = self.__create_dependency_graph(dependency_treshhold,min_frequency)
        DG = self.__create_dependency_graph_with_networkx(dependency_graph)
        #TODO:
        #join and splits
        #return c-net
        return DG
    
    def __create_dependency_graph_with_networkx(self, dependency_graph):
        G = nx.DiGraph()
        G.add_nodes_from(self.events)
        edgelist = []
        for x in range(len(dependency_graph)):
            for y in range(len(dependency_graph[0])):
                if(dependency_graph[x][y]!=0):
                    edgelist.append((self.events[x],self.events[y], {'weight':self.succession_matrix[x][y] }))
        G.add_edges_from(edgelist)
        return G
        

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