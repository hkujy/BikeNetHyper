from copy import deepcopy
from assignment.graph import *
from assignment.line import *
from assignment.shortest_path import ShortestPath as SPP
import assignment.globalpara as gl
import math

def find_y_flow(_net_a,_net_b,_origins,_dests,od_flow,od_flow_a,od_flow_b,_label_station):
    va_y = {}
    vb_y = {}
    per_a = deepcopy(od_flow)
    per_b = deepcopy(od_flow)
    v_b =deepcopy(od_flow)
    timecost_b = deepcopy(od_flow)
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
            per_a[o][d]=1
            per_b[o][d]=0
            for i in _label_station:
                if o in ["N{:0>3}".format(i)]:
                    for j in _label_station:
                        if d in ["N{:0>3}".format(j)]:  
                            per_a[o][d]=1/(1+math.exp(gl.sita*(cost_a-cost_b-gl.fy)))
                            per_b[o][d]=1-per_a[o][d]
                            break
                    break
            assign_flow_a = 0
            assign_flow_b = 0
            if od_flow[o][d]==0:
                continue
            elif per_b[o][d]==0:
                assign_flow_a = od_flow[o][d]
                v_b[o][d] = 0
            elif cost_a < (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                assign_flow_a = od_flow[o][d]
                v_b[o][d] = 0
            elif cost_a >(cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                assign_flow_b = od_flow[o][d]
                v_b[o][d] = assign_flow_b
            elif cost_a == (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                continue
 # step2.3 Update auxiliary variable (y)  ( potential_volume_auto, potential_volume_bike)
            for l in lpath_a:
                va_y[l] += assign_flow_a
            for l in lpath_b:
                vb_y[l] += assign_flow_b
        return va_y,vb_y, v_b,per_b,timecost_b


def update_net_cost(_net_a,_net_b,_va,_vb,_label):
    _net_a.update_cost1(_va,_vb,_label)
    _net_b.update_cost2(_va,_vb,_label)


def initialization(_net_a,_net_b,_origins,_dests,od_flow,_label):
    va = {}
    vb = {}
    for l in _net_a.edge_id_set:
        va[l] = 0
    for l in _net_b.edge_id_set:
        vb[l] = 0
    od_flow_a =deepcopy(od_flow)
    od_flow_b =deepcopy(od_flow)
    _net_a.init_cost1(_label)
    _net_b.init_cost2(_label)
    for o in _origins:
        for d in _dests:
            cost_a, path_a = SPP.dijkstra(_net_a, o, d)
            cost_b, path_b = SPP.dijkstra(_net_b, o, d)
            lpath_a = [_net_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
            lpath_b = [_net_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
            # intial condition set the demand for each mode to be equal
            od_flow_a[o][d] = od_flow_a[o][d]/2
            od_flow_b[o][d] = od_flow_b[o][d]/2
            for l in lpath_a:
                va[l] += od_flow[o][d]/2
            for l in lpath_b:
                vb[l] += od_flow[o][d]/2
    return va,vb,od_flow_a,od_flow_b

     
def FW_main(network_a, network_b, od_flow, origins, destinations,_label_lane,_label_station):
    (va_x,vb_x,od_flow_a,od_flow_b) = initialization(network_a,network_b,origins,destinations,od_flow,_label_lane)
    IterCounter = 0
    while IterCounter < 100:
        update_net_cost(network_a,network_b,va_x,vb_x,_label_lane)
        (va_y,vb_y,v_b,per_b,timecost_b) = find_y_flow(network_a,network_b,origins,destinations,od_flow,od_flow_a,od_flow_b,_label_station)
        step = cal_step(network_a,network_b, va_x,vb_x,va_y,vb_y,origins,destinations,od_flow,od_flow_b,v_b,timecost_b,_label_lane,per_b)
        va_old =deepcopy(va_x)
        vb_old =deepcopy(vb_x)
        for link in network_a.edge_id_set:
            va_x[link] += step * (va_y[link] - va_x[link])
        for link in network_b.edge_id_set:
            vb_x[link] += step * (vb_y[link] - vb_x[link]) 
        converge = cal_limit(va_x,va_old, vb_x, vb_old)
        print("Iter = ",IterCounter,"Gap=",converge)
        IterCounter+=1

def frank_wolfe(network_a, network_b, od_flow, origins, destinations,_label_lane,_label_station):

#step1 initilization 
 # initialize the time cost
  # for automotive vehicle network
    network_a.init_cost1(_label_lane)
  # for bike network
    network_b.init_cost2(_label_lane)
 # empty volume
  # auto:
    empty_a = {}
  # bike:
    empty_b = {}
    for l in network_a.edge_id_set:
        empty_a[l] = 0
    for l in network_b.edge_id_set:
        empty_b[l] = 0
 # definition
    potential_volume_a = deepcopy(empty_a)
    potential_volume_b = deepcopy(empty_b)
    od_flow_a = deepcopy(od_flow)
    od_flow_b = deepcopy(od_flow)

    v_a = deepcopy(od_flow)
    v_b = deepcopy(od_flow)
    timecost_a = deepcopy(od_flow)
    timecost_b = deepcopy(od_flow)
    totalcost = deepcopy(od_flow)
    division = deepcopy(od_flow)
    third = deepcopy(od_flow)
    temp_vol_a = deepcopy(empty_a)
    temp_vol_b = deepcopy(empty_b)
    a=deepcopy(od_flow)
    per_a = deepcopy(od_flow)
    per_b = deepcopy(od_flow)
    
    volume_a = deepcopy(potential_volume_a)
    volume_b = deepcopy(potential_volume_b) 
  #  IterOdWriter = open("Iter_OD.txt","w+")
  #  print("Iter,O,D,aCost,bCost",file =IterOdWriter)
    for o in origins:
        for d in destinations:
            timecost_a[o][d]=0
            timecost_b[o][d]=0
            totalcost[o][d]=0
            per_a[o][d]=0
            per_b[o][d]=0
            third[o][d]=0
 # step1.1 Calculate the travel time of the shortest path
     # auto:
            cost_a, path_a = SPP.dijkstra(network_a, o, d)
            timecost_a[o][d] = cost_a
            lpath_a = [network_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
     # bike:   
            cost_b, path_b = SPP.dijkstra(network_b, o, d)
            timecost_b[o][d]=cost_b
            lpath_b = [network_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
  #step1.2 initialize the distributing rate of motor vehicles and bikes
            per_a[o][d]=1
            per_b[o][d]=0
            for i in _label_station:
                if o in ["N{:0>3}".format(i)]:
                    for j in _label_station:
                        if d in ["N{:0>3}".format(j)]:  
                            per_a[o][d]=1/(1+math.exp(gl.sita*(timecost_a[o][d]-timecost_b[o][d]-gl.fy)))
                            per_b[o][d]=1-per_a[o][d]
                            break
                    break
  # initialize the od_flow of motor vehicles and bikes
            od_flow_a[o][d]=per_a[o][d]*od_flow[o][d]
            od_flow_b[o][d]=per_b[o][d]*od_flow[o][d]  

######################Jy: ini flow
            for l in lpath_a:
                volume_a[l] += od_flow_a[o][d]
            for l in lpath_b:
                volume_a[l] += od_flow_b[o][d]             

############################
  # step1.3 Initialize volume_auto,volume_bike(x)
  



  # clear
    potential_volume_a = deepcopy(empty_a)
    potential_volume_b = deepcopy(empty_b)
  # Update time cost of each link
    network_a.update_cost1(volume_a,volume_b,_label_lane)
    network_b.update_cost2(volume_b,volume_b,_label_lane)
# step2 Calculate direction and step size   
    for o in origins:
        for d in destinations:
            v_a[o][d]=0
            v_b[o][d]=0
            a[o][d]=0
 # step2.1 Find the shortest path and calculate the travel time 
            cost_a, path_a = SPP.dijkstra(network_a, o, d)
            timecost_a[o][d]=cost_a
            lpath_a = [network_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
            cost_b, path_b = SPP.dijkstra(network_b, o, d)
            timecost_b[o][d]=cost_b
            lpath_b = [network_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
            division[o][d]=0
            totalcost[o][d]=timecost_a[o][d]+timecost_b[o][d]+division[o][d]
 # step2.2 Calculate the auxiliary variable of demand allocation(v_auto,v_bike)
            if od_flow[o][d]==0:
                continue
            elif per_b[o][d]==0:
                v_a[o][d]=od_flow[o][d]
                v_b[o][d]=0
            elif cost_a < (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                v_a[o][d]=od_flow[o][d]
                v_b[o][d]=0
            elif cost_a >(cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                v_a[o][d]=0
                v_b[o][d]=od_flow[o][d]
            elif cost_a == (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                continue
 # step2.3 Update auxiliary variable (y)  ( potential_volume_auto, potential_volume_bike)
            for l in lpath_a:
                potential_volume_a[l] += v_a[o][d]
            for l in lpath_b:
                potential_volume_b[l] += v_b[o][d]
 # calculate the distributing rate of bike (=od_flow_bike/od_flow)
    od_rate=deepcopy(od_flow)
 # Record the number of iterations
    n=0
 # Record the convergence value of each iteration
    gen={}
 # step2.4 calculate the move-size
    step = cal_step(network_a,network_b,volume_a,volume_b,potential_volume_a,potential_volume_b,origins,destinations,od_flow,od_flow_b,v_b,timecost_b,_label_lane,per_b)
 # step3 Judge whether convergence condition is met
    while cal_limit(volume_a, temp_vol_a,volume_b, temp_vol_b)>gl.UE_converge:
        n=n+1
        for i in range(n+1):
            if i == n:  
                gen[i]=(cal_limit(volume_a, temp_vol_a,volume_b, temp_vol_b))    
                
 # Update the od_flow of motor vehicles and bikes
  # bike:
        for o in origins:
            for d in destinations:
                for i in _label_station:
                    if o in ["N{:0>3}".format(i)]:
                        for j in _label_station:
                            if d in ["N{:0>3}".format(j)]:  
                                od_flow_b[o][d] += step*(v_b[o][d]-od_flow_b[o][d])
                                break
                        break
  # motor vehicle:
        for o in origins:
            for d in destinations:
                od_flow_a[o][d] = od_flow[o][d]-od_flow_b[o][d]
  # rate of bike
        for o in origins:
            for d in destinations:
                if od_flow[o][d]==0:
                    od_rate[o][d]=0
                else:
                    od_rate[o][d]=od_flow_b[o][d]/od_flow[o][d]
        #TODO: output the od rate using the cost of the shortest path
        # Sorry,I don't quite understand. Could you explain it in more detail?
 # Record the link volume to compare with the results of the next iteration
        temp_vol_a = deepcopy(volume_a)
        temp_vol_b = deepcopy(volume_b)        
 # Updata volume
        for link in network_a.edge_id_set:
            volume_a[link] += step * (potential_volume_a[link] - volume_a[link])
        for link in network_b.edge_id_set:
            volume_b[link] += step * (potential_volume_b[link] - volume_b[link]) 
        potential_volume_a = deepcopy(empty_a)
        potential_volume_b = deepcopy(empty_b)
 # Update time cost of each link
        network_a.update_cost1(volume_a,volume_b,_label_lane)
        network_b.update_cost2(volume_a,volume_b,_label_lane)       
        for o in origins:
            for d in destinations:
                division[o][d]=0
 # shortest path
                cost_a, path_a = SPP.dijkstra(network_a, o, d)
                timecost_a[o][d]=cost_a
                lpath_a = [network_a.edgenode[(path_a[i], path_a[i + 1])] for i in range(len(path_a) - 1)]
                cost_b, path_b = SPP.dijkstra(network_b, o, d)
                timecost_b[o][d]=cost_b
                lpath_b = [network_b.edgenode[(path_b[i], path_b[i + 1])] for i in range(len(path_b) - 1)]
              #  if gl.isOutPutDetail:
                #    print("{0},{1},{2},{3},{4}".format(n,o,d,cost_a,cost_b),file=IterOdWriter)
                v_a[o][d]=0
                v_b[o][d]=0
                third[o][d]=0
                a[o][d]=0
 # Calculate the auxiliary variable of demand allocation(v_auto,v_bike)
                if od_flow[o][d]==0:
                    continue
                elif per_b[o][d]==0:
                    v_a[o][d]=od_flow[o][d]
                    v_b[o][d]=0
                elif cost_a < (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                    v_a[o][d]=od_flow[o][d]
                    v_b[o][d]=0
                elif cost_a >= (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                    v_a[o][d]=0
                    v_b[o][d]=od_flow[o][d]
                elif cost_a == (cost_b+gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))):
                    continue
 # compare (timecost_bike+division) with timecost_auto
                if per_b[o][d]!=0:
                    division[o][d]=gl.fy+(1/gl.sita)*math.log(od_flow_b[o][d]/(od_flow[o][d]-od_flow_b[o][d]))
                    a[o][d]=timecost_b[o][d]+division[o][d]
                else:
                    division[o][d]=0
                    a[o][d]=0
                # TODO: ouput cost of each od pairs
                totalcost[o][d]=timecost_a[o][d]+timecost_b[o][d]+division[o][d]
 # Update potential_volume
                for l in lpath_a:
                    potential_volume_a[l] += v_a[o][d]
                for l in lpath_b:
                    potential_volume_b[l] += v_b[o][d]
 # calculate the move-size
        step = cal_step(network_a,network_b, volume_a, volume_b, potential_volume_a,potential_volume_b,origins,destinations,od_flow,od_flow_b,v_b,timecost_b,_label_lane,per_b)
        time_cost=0
        for o in origins:
            for d in destinations:
                time_cost+=totalcost[o][d]
        time_cost *= 800*1000
 # View the value of each variable
  # od_flow
        #print(od_flow_a,od_flow_b)
  # timecost_bike+division
        # print(a)
  # timecost_auto
        # print(timecost_a)
  # Print the convergence value of each iteration
    print("***********Convergence*************")
   # with open ("Iter.txt","w+") as f:
       # for i in gen:
          #  print("{0},{1}".format(i,gen[i]),file=f)
    
   # IterOdWriter.close()
    
    return volume_a,volume_b,time_cost
