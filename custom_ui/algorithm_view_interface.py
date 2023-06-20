from abc import ABC, abstractmethod, ABCMeta
from PyQt5.QtWidgets import QWidget

# ChatGPT told me this is how to create an interface in Python.
# See heuristic_graph_view.py for how to use this
class HybridMeta(ABCMeta, type(QWidget)):
    pass

class AlgorithmViewInterface(ABC, metaclass = HybridMeta):

    # This method gets called in main before the User interface switches to your View.
    # It should run your algorithm and initiate all variables, so you can show your View.
    # filename is really just the default filename that is used to save the graph later.
    # cases is the preprocessed data to be used in your algorithm. They look like test0.txt in the 'tests' folder, but is a list of lists
    @abstractmethod
    def startMining(self, filename, cases):
        raise NotImplementedError('users must define startMining() to use this base class')
    
    # This method gets called in main before the User interface switches.
    # It should load a pickle file (a stream saved version of your Model class) to support quickloading past saved projects.
    # Look at heuristic_graph_view.py to see how its done.
    @abstractmethod
    def loadModel(self):
        return NotImplementedError('users must define loadModel() to use this base class')
    
    # a png called graph_viz.png must be created in the temp folder.
    # The export png function only copies this file to wherever wished.
    @abstractmethod
    def generate_png(self):
        raise NotImplementedError('users must define generate_png() to use this base class')
    
    # a svg called graph_viz.svg must be created in the temp folder.
    # The export svg function only copies this file to wherever wished.
    @abstractmethod
    def generate_svg(self):
        raise NotImplementedError('users must define generate_svg() to use this base class')
    
    # a dot called graph_viz.dot must be created in the temp folder.
    # The export dot function only copies this file to wherever wished.
    @abstractmethod
    def generate_dot(self):
        raise NotImplementedError('users must define generate_dot() to use this base class')
    
    # Clean up after yourself. Don't litter around.
    @abstractmethod
    def clear(self):
        raise NotImplementedError('users must define clear() to use this base class')
    