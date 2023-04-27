from abc import ABC, abstractmethod, ABCMeta
from PyQt5.QtWidgets import QWidget

# ChatGPT told me this is how to create an interface in Python.
# To use this file just import the AlgorithmViewInterface class, like in heuristic_graph_view.py
class HybridMeta(ABCMeta, type(QWidget)):
    pass

class AlgorithmViewInterface(ABC, metaclass = HybridMeta):
    @abstractmethod
    def mine(self):
        raise NotImplementedError('users must define min() to use this base class')
    
    @abstractmethod
    def generate_svg(self):
        raise NotImplementedError('users must define generate_svg() to use this base class')
    
    @abstractmethod
    def clear(self):
        raise NotImplementedError('users must define clear() to use this base class')