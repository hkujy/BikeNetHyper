from assignment.assign import frank_wolfe
from assignment.line import *
from assignment.graph import *


"""

"""

def read_network_auto(_label_lane):
    
    nt_a = network_a('net_a')
    node_a = vertex_a("a_a")
    

    # read from csv
    with open('network_Copy.csv','r') as fo:
        lines = fo.readlines()
        for ln in lines:
            eg_a = ln.split(',')
            nt_a.add_edge(edge_a(eg_a))
    # initialize cost_auto
    nt_a.init_cost1(_label_lane)
    return nt_a

def read_network_bike(_label_lane):
    
    nt_b = network_b('net_b')
    node_b= vertex_b("a_b")

    # read from csv
    with open('network_Copybike.txt','r') as fo:
      
        lines = fo.readlines()
        for ln in lines:
            eg_b = ln.split(',')
            nt_b.add_edge(edge_b(eg_b))
    # initialize cost_bike
    nt_b.init_cost2(_label_lane)
    return nt_b


def od_demand():


# read from json
    # read od flow
    od_flow = {
        'N001': {'N002':1000,'N003':1000}}
    origins = ['N001']
    destinations = ['N002','N003']
    return od_flow, origins, destinations
