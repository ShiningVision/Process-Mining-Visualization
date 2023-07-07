from mining_algorithms.heuristic_mining import HeuristicMining
from api.pickle_save import pickle_load

class HeuristicGraphController():
    def __init__(self, workingDirectory):
        super().__init__()
        self.model = None
        self.workingDirectory = workingDirectory

    #CALL BEFORE USAGE (option 1 for mining new models)
    def startMining(self, cases):
        self.model = HeuristicMining(cases)

    #CALL BEFORE USAGE (option 2 for mining existing models)
    def loadModel(self, file_path):
        self.model = pickle_load(file_path)
        return file_path

    def create_dependency_graph(self, dependency_threshold, min_frequency):
        graph = self.model.create_dependency_graph_with_graphviz(dependency_threshold,min_frequency)
        graph.render(self.workingDirectory,format = 'dot')    
        #print("HeuristicGraphController: CSV mined")
        return graph
    
    def get_min_frequency(self):
        return self.model.get_min_frequency()
    
    def get_threshold(self):
        return self.model.get_threshold()
    
    def get_max_frequency(self):
        return self.model.get_max_frequency()
    
    def getModel(self):
        return self.model
    



