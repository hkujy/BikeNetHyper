import random
import copy
from assignment.assign import frank_wolfe,FW_main
from assignment.graph import * 
from assignment.line import *
import set_input
import time
#Step 0:Initialization
 #sequence
SEQ=[]
 #initially every element in the two matrices is assigned the value ‘1’
 #transition_matrix
TM={
        'L0': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L1': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L2': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L3': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L4': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L5': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1},
        'L6': {'L0':1,'L1':1,'L2':1,'L3':1,'L4':1,'L5':1,'L6':1}}
 #low level heuristics set 
LLH=['L0','L1','L2','L3','L4','L5','L6']
 #probability
pro_TM=copy.deepcopy(TM)
 #cumulative probability
cumulative_pro_TM=copy.deepcopy(TM)
 #sequence_metricx
SM={
        'L0': {'STOP':1,'CONTINUE':1},
        'L1': {'STOP':1,'CONTINUE':1},
        'L2': {'STOP':1,'CONTINUE':1},
        'L3': {'STOP':1,'CONTINUE':1},
        'L4': {'STOP':1,'CONTINUE':1},
        'L5': {'STOP':1,'CONTINUE':1},
        'L6': {'STOP':1,'CONTINUE':1}}
pro_SM=copy.deepcopy(SM)
CHOICE=['STOP','CONTINUE']
cumulative_pro_SM=copy.deepcopy(SM)
 # alternative station
station=range(0,6)
 # alternative lane
lane=range(0,6)
# demand point
demand=range(1,4)
 # 1 means alternative station j can been selected by demand point i
match_station={1: {0:1,1:1,2:0,3:0,4:0,5:0},
 2: {0:0,1:0,2:1,3:1,4:1,5:1},
 3: {0:0,1:0,2:0,3:0,4:1,5:1}}
 # label_station represents the selected stations (station 3,4,8,10;demand point 1,2,3,4)
label_station=[1,0,0,2,0,3]
 # judge_lane means alternative lane i has been selected,else 0
label_lane=[]
for i in lane:
    label_lane.append(1)
cost_station=[3000,4000,4000,3000,3000,4000]
cost_lane=[3000,2500,3000,3500,3000,2000]
best_cost=1037387
best_lane=copy.deepcopy(label_lane)
best_station=[1,0,0,2,0,3]
cur_cost=1037387
cur_lane=copy.deepcopy(label_lane)
cur_station=[1,0,0,2,0,3]


#Step 1: Low level heuristics
#LLH0:Select an unselected link and add it to the bicycle link set.
def cal_L0_add_bike_link(_label_lane,_lane):
 # d,e for temporary data storage,meaningless
    d=[]    
    e=0
    for i in _lane:
        if _label_lane[i]==0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d)
        _label_lane[e]=1
    return _label_lane
'''
print("Before Cal_L0")
print(label_lane)
#cal_L0_add_bike_link(_label_lane=label_lane,_lane=lane)
print("After Cal_L0")
print(label_lane)
'''
#LLH1:Select a link in the bicycle link set and move it out of the bicycle link set.
def cal_L1_remove_bike_link(_label_lane,_lane): 
    d=[]    
    e=0
    for i in _lane:
        if _label_lane[i]==1:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d)
        _label_lane[e]=0
    return _label_lane
'''
print("Before cal_L1")
print(label_lane)
cal_L1_remove_bike_link(_label_lane=label_lane,_lane=lane)
print("After cal_L1")
print(label_lane)
'''
#LLH2:Select an unassigned node and a random node set (it belongs to an O/D) and assign the node to the set.
def cal_L2_add_bike_station(_label_station,_station,_match_station,_demand): 
    d=[]    
    e=0
    f=0
    for i in _station:
        if _label_station[i]==0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d)
    d=[]
    for i in _demand:
        if _match_station[i][e]==1:
             d.append(i) 
    if len(d)!=0:
        f=random.choice(d) 
        _label_station[e]=f
    return _label_station
'''
print("Before cal_L2")
print(label_station)
cal_L2_add_bike_station(_label_station=label_station,_station=station,_match_station=match_station,_demand=demand)
print("After cal_L2")
print(label_station)
'''
#LLH3:Select a random node in the set and move it out of the set.
def cal_L3_remove_bike_station(_label_station,_station,_match_station,_demand): 
    d=[]    
    e=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        _label_station[e]=0
    return _label_station
'''
print("Before cal_L3")
print(label_station)
cal_L3_remove_bike_station(_label_station=label_station,_station=station,_match_station=match_station,_demand=demand)
print("After cal_L3")
print(label_station)
'''
#LLH4:Select a random node set and a random node in it and replace the node with another unassigned node.
def cal_L4_replace_bike_station(_label_station,_station,_match_station,_demand): 
 # d,g,e,f,h are used for temporary data storage,meaningless
    d=[]  
    g=[]
    e=0
    f=0
    h=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        for i in _station:
            if _match_station[f][i]==1 and _label_station[i]==0:
                g.append
        if len(g)!=0:
            h=random.choice(g) 
            _label_station[h]=_label_station[e]
            _label_station[e]=0
    return _label_station
'''
print("Before cal_L4")
print(label_station)
cal_L4_replace_bike_station(_label_station=label_station,_station=station,_match_station=match_station,_demand=demand)
print("After cal_L4")
print(label_station)
'''
#LLH5:Select two random sets and a random node in each set. The node in the first set is inserted into the second set.
def cal_L5_insert_bike_station(_label_station,_station,_match_station,_demand): 
    d=[]  
    e=0
    f=0
    g=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        d=[]
        for i in _station:
            if _label_station[i]!=0 and _label_station[i]!=f and _match_station[f][i]==1:
                d.append(i)   
        if len(d)!=0:
            g=random.choice(d) 
            _label_station[e]=_label_station[g]
    return _label_station
'''
print("Before cal_L5")
print(label_station)
cal_L5_insert_bike_station(_label_station=label_station,_station=station,_match_x=match_station,_demand=demand)
print("After cal_L5")
print(label_station)
'''
#LLH6:Select two random sets and a random node in each set and swap the nodes.
def cal_L6_swap_bike_station(_label_station,_station,_match_station,_demand): 
    d=[]  
    e=0
    f=0
    g=0
    for i in _station:
        if _label_station[i]!=0:
            d.append(i)
    if len(d)!=0:
        e=random.choice(d) 
        f=_label_station[e]
        d=[]
        for i in _station:
            if _label_station[i]!=0 and _label_station[i]!=f and _match_station[f][i]==1 and _match_station[_label_station[i]][e]==1:
                d.append(i)   
        if len(d)!=0:
            g=random.choice(d) 
            _label_station[e]=_label_station[g]
            _label_station[g]=f
    return _label_station
'''
print("Before cal_L6")
print(label_station)
cal_L6_swap_bike_station(_label_station=label_station,_station=station,_match_station=match_station,_demand=demand)
print("After cal_L6")
print(label_station)
'''

#Step2:Hueristics Sequence Selection
def cal_HSS():
    """
    a random low level heuristic is selected and add to the sequence
    """
    cur=random.randint(0,len(LLH)-1)
    SEQ.append(LLH[cur])
    
    # LLH(next) is chosen by a selection procedure based on the roulette wheel selection strategy 
    """
    start of the roulette wheel
    """
    a=0
    b=0
    c=random.uniform(0,1)
    for i in LLH:
        for j in LLH:
            cumulative_pro_TM[i][j]=0
    for j in LLH:
        a+=TM[LLH[cur]][j]

    for j in LLH:
        pro_TM[LLH[cur]][j]=TM[LLH[cur]][j]/a
        cumulative_pro_TM[LLH[cur]][j]=b+pro_TM[LLH[cur]][j]
        b=cumulative_pro_TM[LLH[cur]][j]

    for j in LLH:
        if cumulative_pro_TM[LLH[cur]][j]<c:
            continue
        else:
            SEQ.append(j)
            cur=j
            break
    """
    end of the roulette wheel
    """
    # judge whether the sequence will terminate at this point
    a=0
    c=random.uniform(0,1)
    for j in CHOICE:
        a+=SM[cur][j]
    for j in CHOICE:
        pro_SM[cur][j]=SM[cur][j]/a
    cumulative_pro_SM[cur][CHOICE[0]]=pro_SM[cur][CHOICE[0]]
    cumulative_pro_SM[cur][CHOICE[1]]=1
    while cumulative_pro_SM[cur][CHOICE[0]]<c:      
        a=0
        b=0
        c=random.uniform(0,1)
        for i in LLH:
            for j in LLH:
                cumulative_pro_TM[i][j]=0
        for j in LLH:
            a+=TM[cur][j]
        for j in LLH:
            pro_TM[cur][j]=TM[cur][j]/a
            cumulative_pro_TM[cur][j]=b+pro_TM[cur][j]
            b=cumulative_pro_TM[cur][j]
        for j in LLH:
            if cumulative_pro_TM[cur][j]<c:
                continue
            else:
                SEQ.append(j)
                cur=j
                break
        a=0
        c=random.uniform(0,1)
        for j in CHOICE:
            a+=SM[cur][j]
        for j in CHOICE:
            pro_SM[cur][j]=SM[cur][j]/a
        cumulative_pro_SM[cur][CHOICE[0]]=pro_SM[cur][CHOICE[0]]
        cumulative_pro_SM[cur][CHOICE[1]]=1
    return SEQ

 #step 3:apply SEQ
def cal_apply(_uSEQ,_ulabel_lane,_ulane,_ulabel_station,_ustation,_umatch_station,_udemand):
    for i in _uSEQ:
        if i in ["L0"]:
            _ulabel_lane=cal_L0_add_bike_link(_label_lane=_ulabel_lane,_lane=_ulane)
            continue
        if i in ["L1"]:
            _ulabel_lane=cal_L1_remove_bike_link(_label_lane=_ulabel_lane,_lane=_ulane)
            continue
        if i in ["L2"]:
            _ulabel_station=cal_L2_add_bike_station(_label_station=_ulabel_station,_station=_ustation,_match_station=_umatch_station,_demand=_udemand)
            continue
        if i in ["L3"]:
            _ulabel_station=cal_L3_remove_bike_station(_label_station=_ulabel_station,_station=_ustation,_match_station=_umatch_station,_demand=_udemand)
            continue
        if i in ["L4"]:
            _ulabel_station=cal_L4_replace_bike_station(_label_station=_ulabel_station,_station=_ustation,_match_station=_umatch_station,_demand=_udemand)
        if i in ["L5"]: 
            _ulabel_station=cal_L5_insert_bike_station(_label_station=_ulabel_station,_station=_ustation,_match_station=_umatch_station,_demand=_udemand)
            continue
        if i in ["L6"]:
            _ulabel_station=cal_L6_swap_bike_station(_label_station=_ulabel_station,_station=_ustation,_match_station=_umatch_station,_demand=_udemand)
    return _ulabel_lane,_ulabel_station
#Step 4: Calculate the cost
def cal_new_cost(_station,_label_station,_label_lane,_cost_station,_cost_lane,_lane):
   # fixed_cost
    fixed_cost=0
    _new_cost=0
    for i in _station:
        if _label_station[i]!=0:
            fixed_cost+=_cost_station[i]
    for i in _lane:
        if _label_lane[i]!=0:
            fixed_cost+=_cost_lane[i]
   # time_cost
    time_cost=0
    od_flow, origins, destinations = set_input.od_demand()
    nt_a = set_input.read_network_auto(_label_lane)
    nt_b = set_input.read_network_bike(_label_lane)
#############
    FW_main(nt_a,nt_b,od_flow,origins,destinations,_label_lane,_label_station)
#############
    vol_a,vol_b,time_cost = frank_wolfe(nt_a, nt_b, od_flow, origins, destinations,_label_lane,_label_station)
    
    if gl.isOutPutDetail:
        print("*****motor vehicles*****")
        for link in vol_a.keys():
            print("{0},{1}".format(link,vol_a[link]))
        print("*****bikes*****")
        for link in vol_b.keys():
            print("{0},{1}".format(link,vol_b[link]))
    _new_cost=time_cost+fixed_cost
    return _new_cost

#Step 5: test upper
n=0
start_time = time.perf_counter()
while n<5:
    print(n)
    n+=1
    SEQ=[]
    SEQ=cal_HSS()
    label_lane,label_station=cal_apply(_uSEQ=SEQ,_ulabel_lane=label_lane,_ulane=lane,_ulabel_station=label_station,_ustation=station,_umatch_station=match_station,_udemand=demand)
    new_cost=cal_new_cost(_station=station,_label_station=label_station,_label_lane=label_lane,_cost_station=cost_station,_cost_lane=cost_lane,_lane=lane)
    # Acceptence method:Only Improve
    print(new_cost,label_lane,label_station)
    if new_cost<cur_cost:
        cur_cost=new_cost
        cur_lane=copy.deepcopy(label_lane)
        cur_station=copy.deepcopy(label_station)   
      # Update TM and SM
        for i in range(len(SEQ)-1):
            TM[SEQ[i]][SEQ[i+1]]+=1
        for i in range(len(SEQ)-1):
            SM[SEQ[i]][CHOICE[0]]+=1
        SM[SEQ[len(SEQ)-1]][CHOICE[1]]+=1
  # Update best_cost,best_label_lane,best_label_station
        if cur_cost<best_cost:
            best_cost=cur_cost
            best_lane=copy.deepcopy(cur_lane)
            best_station=copy.deepcopy(cur_station)
    else:
        new_cost=cur_cost
        label_lane=copy.deepcopy(cur_lane)
        label_station=copy.deepcopy(cur_station)

print(best_cost,best_lane,best_station)


cal_new_cost(_station=station,_label_station=best_station,_label_lane=best_lane,_cost_station=cost_station,_cost_lane=cost_lane,_lane=lane)

elapsed_time = time.perf_counter() - start_time  
print('time of f-w: ', elapsed_time)