from .csv_reader import read
from .heuristic_alg import heuristic_mining
#get csv input
def mining(csv):
    #group events by cases
    dic = read(csv)
    #run in heuristic alg
    graph_input = heuristic_mining(dic)
    #generate dot file

    #return c-net
    return graph_input