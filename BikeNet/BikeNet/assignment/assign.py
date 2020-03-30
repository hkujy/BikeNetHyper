from copy import deepcopy
from assignment.graph import *
from assignment.line import *
from assignment.shortest_path import ShortestPath as SPP
import assignment.globalpara as gl
import math

def find_y_flow(_net_a,_net_b,_origins,_dests,od_flow,od_flow_a,od_flow_b,_label_station,per_b):
    va_y = {}
    vb_y = {}
    timecost_b = deepcopy(od_flow)
    assign_flow_a=deepcopy(od_flow)
    assign_flow_b=deepcopy(od_flow)
    for l in _net_a.edge_id_set:
        va_y[l] = 0
    for l in _net_b.edge_id_set:
        vb_y[l] = 0
    for o in _origins:
        for d in _dests:
            cost_a, path_a = SPP.dijkstra(_net_a, o, d)
            cost_b, path_b = SPP.dijkstra(_net_b, o, d)
            timecost_b[o][d] = cost_b
            lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
            lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
            assign_flow_a[o][d] = 0
            assign_flow_b[o][d] = 0
            if od_flow[o][d]==0:
                continue
            elif per_b[o][d]==0:
                assign_flow_a[o][d] = od_flow[o][d]
                assign_flow_b[o][d] = 0
            else: 
                assign_flow_b[o][d] = od_flow[o][d]/(1+math.exp(gl.sita*(cost_b-cost_a+gl.fy)))
                assign_flow_a[o][d] = od_flow[o][d]-assign_flow_b[o][d]
 # Update auxiliary variable (y)  ( potential_volume_auto, potential_volume_bike)
            for l in lpath_a:
                va_y[l] += assign_flow_a[o][d]
            for l in lpath_b:
                vb_y[l] += assign_flow_b[o][d]
        
        return va_y,vb_y, assign_flow_b,per_b,timecost_b


def update_net_cost(_net_a,_net_b,_va,_vb,_label):
    _net_a.update_cost1(_va,_vb,_label)
    _net_b.update_cost2(_va,_vb,_label)


def initialization(_net_a,_net_b,_origins,_dests,od_flow,_label_lane,_label_station):
    va = {}
    vb = {}
    for l in _net_a.edge_id_set:
        va[l] = 0
    for l in _net_b.edge_id_set:
        vb[l] = 0
    od_flow_a =deepcopy(od_flow)
    od_flow_b =deepcopy(od_flow)
    per_a = deepcopy(od_flow)
    per_b = deepcopy(od_flow)
    _net_a.init_cost1(_label_lane)
    _net_b.init_cost2(_label_lane)
    for o in _origins:
        for d in _dests:
            cost_a, path_a = SPP.dijkstra(_net_a, o, d)
            cost_b, path_b = SPP.dijkstra(_net_b, o, d)
            lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
            lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
            # intial condition set the demand for each mode to be equal
            per_a[o][d]=1
            per_b[o][d]=0
            for i in _label_station:
                if o in ["N{:0>3}".format(i)]:
                    for j in _label_station:
                        if d in ["N{:0>3}".format(j)]:  
                            per_a[o][d]=1/2
                            per_b[o][d]=1/2
                            break
                    break
            
            od_flow_a[o][d]=per_a[o][d]*od_flow[o][d]
            od_flow_b[o][d]=per_b[o][d]*od_flow[o][d]
            for l in lpath_a:
                va[l] += od_flow_a[o][d]
            for l in lpath_b:
                vb[l] += od_flow_b[o][d]
    return va,vb,od_flow_a,od_flow_b,per_b

     
def FW_main(network_a, network_b, od_flow, origins, destinations,_label_lane,_label_station):
    (va_x,vb_x,od_flow_a,od_flow_b,per_b) = initialization(network_a,network_b,origins,destinations,od_flow,_label_lane,_label_station)
    IterCounter = 0
    time_cost=0
    while IterCounter < 100:
        update_net_cost(network_a,network_b,va_x,vb_x,_label_lane)
        (va_y,vb_y,v_b,per_b,timecost_b) = find_y_flow(network_a,network_b,origins,destinations,od_flow,od_flow_a,od_flow_b,_label_station,per_b)
        step = cal_step(network_a,network_b, va_x,vb_x,va_y,vb_y,origins,destinations,od_flow,od_flow_b,v_b,timecost_b,_label_lane,per_b)
        va_old =deepcopy(va_x)
        vb_old =deepcopy(vb_x)
        for link in network_a.edge_id_set:
            va_x[link] += step * (va_y[link] - va_x[link])
        for link in network_b.edge_id_set:
            vb_x[link] += step * (vb_y[link] - vb_x[link]) 
        for o in origins:
            for d in destinations:
                if per_b[o][d]!=0:
                    od_flow_b[o][d] += step*(v_b[o][d]-od_flow_b[o][d])
                else:
                    od_flow_b[o][d]=0
                od_flow_a[o][d]=od_flow[o][d]-od_flow_b[o][d]
        converge = cal_limit(va_x,va_old, vb_x, vb_old)         
        print("Iter = ",IterCounter,"Gap=",converge)
        IterCounter+=1
    time_cost=cal_timecost(network_a,network_b,va_x,vb_x,_label_lane)
    time_cost*=568
    return va_x,vb_x,time_cost
def cal_timecost(_network_a,_network_b,_va_x,_vb_x,_lab_lane):
    _time_cost=0
    a=0
    for lid in _va_x.keys():
        for j in range(1,7):
            if lid in ["E{:0>3}".format(j)]:
                a = _network_a.edgeset[lid].cal_weight1(_va_x[lid],_vb_x[lid],_lab_lane[j-1]) * _va_x[lid]
                _time_cost+=a
    for lid in _vb_x.keys():
        for j in range(1,7):
            if lid in ["E{:0>3}".format(j)]:
                a = _network_b.edgeset[lid].cal_weight2(_va_x[lid],_vb_x[lid],_lab_lane[j-1]) * _vb_x[lid]
                _time_cost+=a
    return _time_cost 
            
    