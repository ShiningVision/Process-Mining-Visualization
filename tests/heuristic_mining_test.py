'''
As of writing this, the tests in this file only create images of graphs in the 'temp' folder that then need to be verified manually.
There is no auto verification of png-files, since I have not implemented it.
'''

import unittest
from algorithms.heuristic_mining import HeuristicMining
from algorithms.csv_preprocessor import read

# I am using networkx here because GRAPHVIZ does not provide ANY GET-FUNCTIONS!
import networkx as nx

class TestHeuristic(unittest.TestCase):

    def test_create_dependency_graph_with_graphviz(self):
        print("-------------- Running test.txt ----------------")
        self.__run_test_txt('test0')
        print("passed test 0")
        self.__run_test_txt('test1')
        print("passed test 1")
        self.__run_test_txt('test2')
        print("passed test 2")
        self.__run_test_txt('test3')
        print("passed test 3")
        print("---------------- test.txt passed! ----------------")

    def test_create_dependency_graph_with_graphviz_using_test_csv(self):
        print("-------------- Running test_csv ----------------")
        self.__run_test_csv(0.5, 1)
        print("passed test 1")
        self.__run_test_csv(0.1, 1)
        print("passed test 2")
        self.__run_test_csv(0.9, 1)
        print("passed test 3")
        self.__run_test_csv(0.5, 10)
        print("passed test 4")
        print("---------------- test_csv passed! ----------------")

    #read test cases that are txt files for testing
    def __read_cases(self, filename):
        log = []
        #cwd = os.getcwd()
        #path = os.path.join(cwd, filename)
        with open(filename, 'r') as f:
            for line in f.readlines():
                assert isinstance(line, str)
                log.append(list(line.split()))
        return log
    
    def __run_test_txt(self, filename):
        Heuristic = HeuristicMining(self.__read_cases('tests/'+filename+'.txt'))
        G = Heuristic.create_dependency_graph_with_graphviz(0.5,1)
        G.render('temp/'+filename,format='dot')
        dotsource = 'temp/'+filename+'.dot'
        self.__run_test(dotsource)

    def __run_test_csv(self, threshold, min_freq):
        Heuristic = HeuristicMining(read('tests/test_csv.csv'))
        G = Heuristic.create_dependency_graph_with_graphviz(threshold, min_freq)  # G is a graphviz Digraph
        G.render('temp/test_csv', format='dot')
        G.render('temp/test_csv', format='png')
        dot_source = 'temp/test_csv.dot'

        self.__run_test(dot_source)

    def __run_test(self, dotsource):
        # Read in dot file with NetworkX
        nx_graph = nx.drawing.nx_agraph.read_dot(dotsource)

        # Check there is a 'start' node that connects to at least 1 other node
        start_node = None
        for node in nx_graph.nodes:
            if nx_graph.in_degree(node) == 0:  # In-degree of 0 indicates a 'start' node
                start_node = node
                break

        assert start_node is not None, "No 'start' node found."
        assert nx_graph.out_degree(start_node) >= 1, "The 'start' node does not connect to any other nodes."

        # Check there is an 'end' node
        end_node = None
        for node in nx_graph.nodes:
            if nx_graph.out_degree(node) == 0:  # Out-degree of 0 indicates an 'end' node
                end_node = node
                break

        assert end_node is not None, "No 'end' node found."

        # Check every node is reachable from some other node
        reachable_nodes = nx.algorithms.dag.descendants(nx_graph, start_node)
        reachable_nodes.add(start_node)

        all_nodes = [node for node in nx_graph.nodes if node.strip() != '\\n' and node.strip() != '']
        assert set(reachable_nodes) == set(all_nodes), "Not all nodes are reachable from the 'start' node."