'''
This unittest tests the integrity of the heuristic_graph_controller which holds the HeuristicMining Model.
'''
import pydot
import unittest
from custom_ui.heuristic_graph_ui.heuristic_graph_controller import HeuristicGraphController
from mining_algorithms.heuristic_mining import HeuristicMining
from api.csv_preprocessor import read

# I am using networkx here because GRAPHVIZ does not provide ANY GET-FUNCTIONS!
import networkx as nx

class TestHeuristic(unittest.TestCase):

    def test_create_dependency_graph_using_preprocessed_txt(self):
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

    def test_create_dependency_graph_using_test_csv(self):
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

    def test_create_dependency_graph_using_CallcenterExample(self):
        print("-------------- Running large CallcenterExample ----------------")
        self.__run_CallcenterExample_csv(0.5, 1)
        print("---------------- CallcenterExample passed! ----------------")

    def test_loading_pickle_HeuristicMining_model(self):
        print("----------- Running pickle loading test ----------")
        print("(This test fails if you messed with the HeuristicMining class)")
        print("(Replace the pickle file with a new one if you did)")
        self.__run_pickle_loading_test("tests/testpickle/test_csv.pickle")
        print("---------------- pickle loading test passed! ----------------")

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
        Controller = HeuristicGraphController('temp/graph_viz')
        Controller.startMining(self.__read_cases('tests/testlogs/'+filename+'.txt'))
        G = Controller.create_dependency_graph(0.5,1)
        target = 'temp/'+filename
        dotsource = target+'.dot'
        G.render(target,format="dot")
        self.__check_graph_integrity_with_netx(dotsource)

    def __run_test_csv(self, threshold, min_freq):
        Controller = HeuristicGraphController('temp/graph_viz')
        Controller.startMining(read('tests/testcsv/test_csv.csv'))
        G = Controller.create_dependency_graph(threshold, min_freq)  # G is a graphviz Digraph
        target = 'temp/test_csv'
        dot_source = target+'.dot'
        G.render(target,format="dot")
        self.__check_graph_integrity_with_netx(dot_source)

    def __run_CallcenterExample_csv(self, threshold, min_freq):
        Controller = HeuristicGraphController('temp/graphviz')
        Controller.startMining(
            read('tests/testcsv/CallcenterExample.csv',caseLabel='Service ID',eventLabel='Operation',
                timeLabel='Start Date'))
        G = Controller.create_dependency_graph(threshold, min_freq)  # G is a graphviz Digraph
        target = 'temp/callcenter'
        dot_source = target+'.dot'
        G.render(target,format="dot")
        self.__check_graph_integrity_with_netx(dot_source)


    def __run_pickle_loading_test(self, pickleFile):
        Controller = HeuristicGraphController( 'temp/graph_viz')
        Controller.loadModel(pickleFile)

        self.assertIsInstance(Controller.getModel(), HeuristicMining)
        
        G = Controller.create_dependency_graph(0.2, 4)
        self.assertIsNotNone(G)
        
        max_frequency = Controller.get_max_frequency()
        self.assertIsNotNone(max_frequency)
        
        min_frequency = Controller.get_min_frequency()
        self.assertIsNotNone(min_frequency)
        
        threshold = Controller.get_threshold()
        self.assertIsNotNone(threshold)

    def __check_graph_integrity_with_netx(self, dotsource):
        # Read in dot file with NetworkX
        
        # The commented code below uses Pygraphviz. Pydot is deprecated. 
        # But pygraphviz is a nightmare to install on Windows and requires a C/C++ compiler.
        # This is something I can not require from any non professional user. (Not even from a professional developer)
        # -- Anton Chen, June 2023
        #nx_graph = nx.drawing.nx_agraph.read_dot(dotsource)

        # This is code using pydot. A deprecated library without reliable replacement.
        # So I will stick with it despite its deprecation status. 
        # Maybe someday PyGraphviz will be stable enough to replace it?
        graph = pydot.graph_from_dot_file(dotsource)
        nx_graph = nx.nx_pydot.from_pydot(graph[0])

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
