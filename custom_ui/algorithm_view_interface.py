from abc import ABC, abstractmethod, ABCMeta
from PyQt5.QtWidgets import QWidget

# ChatGPT told me this is how to create an interface in Python.
# See heuristic_graph_view.py for how to use this
class HybridMeta(ABCMeta, type(QWidget)):
    pass

class AlgorithmViewInterface(ABC, metaclass = HybridMeta):

    #This method gets called in main before the User interface switches to your View.
    #It should run your algorithm and initiate all variables, so you can show your View.
    @abstractmethod
    def mine(self):
        raise NotImplementedError('users must define mine() to use this base class')
    
    # a png called graph_viz.png must be created in the temp folder.
    # The export png function only copies this file to wherever wished.
    @abstractmethod
    def generate_png(self):
        raise NotImplementedError('users must define generate_png() to use this base class')
    
    # an svg called graph_viz.svg must be created in the temp folder.
    # The export svg function only copies this file to wherever wished.
    @abstractmethod
    def generate_svg(self):
        raise NotImplementedError('users must define generate_svg() to use this base class')
    
    # Clean up after yourself. Don't litter around.
    @abstractmethod
    def clear(self):
        raise NotImplementedError('users must define clear() to use this base class')