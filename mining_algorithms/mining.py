from .csv_reader import read
from .heuristic_mining import HeuristicMining
#get csv input
def mining(csv):
    #group events by cases
    cases = read(csv)
    #run in heuristic algorithm
    heuristic = HeuristicMining(cases)
    graph_input = heuristic.mine(0.5,1)
    #TODO:
    #generate dot file?
    #return c-net
    return graph_input