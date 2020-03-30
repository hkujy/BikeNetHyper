# test assignment model
from assignment.assign import frank_wolfe
# from assignment.line import *
from assignment.graph import * 
from assignment.line import *
import time
import set_input
import myplot as mplt
# initialize the network
 

if __name__ == "__main__":
    start_time = time.perf_counter()
    od_flow, origins, destinations = set_input.od_demand()
    nt_a = set_input.read_network_auto()
    nt_b = set_input.read_network_bike()
    vol_a,vol_b,time_cost = frank_wolfe(nt_a, nt_b, od_flow, origins, destinations)
    elapsed_time = time.perf_counter() - start_time
    print(time_cost)
    print('time of f-w: ', elapsed_time)
    print("*****Print Link Flow***************")
    if gl.isOutPutDetail:
        for link in vol_a.keys():
            print("{0},{1}".format(link,vol_a[link]))
        for link in vol_b.keys():
            print("{0},{1}".format(link,vol_b[link]))
    
    mplt.plot_main()
        
