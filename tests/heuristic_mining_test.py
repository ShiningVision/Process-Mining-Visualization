'''
As of writing this the tests in this file only create images of graphs in the 'temp' folder that then need to be verified manually.
There is no auto verification of png-files, since I have not implemented it.
'''

import unittest
from mining_algorithms.heuristic_mining import HeuristicMining
import networkx as nx
import matplotlib.pyplot as plt
from mining_algorithms.csv_reader import read

class TestHeuristic(unittest.TestCase):

    def test_create_dependency_graph_with_networkx(self):
        #print('nxtest started')
        filename = 'tests/test0.txt'
        log = self.__read_cases(filename)
        Heuristic = HeuristicMining(log)
        #print('nxtest read')
        nxGraph = Heuristic.create_dependency_graph_with_networkx(0.5,1)
        #print('nxtest mined')

        plt.figure(figsize = (12,12))
        nx.draw(nxGraph,nx.spring_layout(nxGraph), with_labels = True)
        #print('nxtest drawn')
        plt.savefig('temp/test0_nx.png', format="PNG")
        #print('nxtest saved')
        pass

    def test_create_dependency_graph_with_graphviz(self):
        Heuristic = HeuristicMining(self.__read_cases('tests/test0.txt'))
        G = Heuristic.create_dependency_graph_with_graphviz(0.5,1)
        G.render('temp/test0_viz',format='png')
        pass

    def test_create_dependency_graph_with_graphviz_using_test_csv(self):
        Heuristic = HeuristicMining(read('tests/test_csv.csv'))
        G = Heuristic.create_dependency_graph_with_graphviz(0.5,1)
        G.render('temp/test_csv_viz',format = 'png')
        pass

    #read test cases that are txt files
    def __read_cases(self, filename):
        log = []
        #cwd = os.getcwd()
        #path = os.path.join(cwd, filename)
        with open(filename, 'r') as f:
            for line in f.readlines():
                assert isinstance(line, str)
                log.append(list(line.split()))
        return log
        
