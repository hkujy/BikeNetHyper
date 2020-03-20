import math
import assignment.globalpara as gl
from copy import deepcopy



# Derivation
def div(net_a, net_b, prior_a,prior_b, posterior_a, posterior_b,origins,destinations,od_flow,od_flow_b,v_b,step,timecost_b,_ulabel_lane,per_b):

    third =deepcopy(od_flow)
    idiv = 0
    cost_a={}
    cost_b={}
    dist_a={}
    dist_b={}
    for o in origins:
        for d in destinations:
            if od_flow[o][d]==0:
                idiv+=0
                continue
            elif per_b[o][d]==0:
                idiv+=0
            else:
                third[o][d] = (v_b[o][d]-od_flow_b[o][d])*((1/gl.sita)*math.log((od_flow_b[o][d]+step*(v_b[o][d]-od_flow_b[o][d]))/(od_flow[o][d]-(od_flow_b[o][d]+step*(v_b[o][d]-od_flow_b[o][d]))))+gl.fy+timecost_b[o][d])
                idiv += third[o][d]
    for lid in prior_a.keys():
        dist_a[lid] = posterior_a[lid] - prior_a[lid]
    for lid in prior_b.keys():    
        dist_b[lid] = posterior_b[lid] - prior_b[lid]
    for lid in prior_a.keys():
        cost_a[lid] = dist_a[lid]*net_a.edgeset[lid].cal_weight1(prior_a[lid] + step * dist_a[lid],prior_b[lid] + step * dist_b[lid],_ulabel_lane)
        idiv += cost_a[lid]
    for lid in prior_b.keys():
        cost_b[lid] = dist_b[lid]*net_b.edgeset[lid].cal_weight2(prior_a[lid] + step * dist_a[lid],prior_b[lid] + step * dist_b[lid],_ulabel_lane)
        idiv += cost_b[lid]
    return idiv

def cal_step(net_a, net_b, prior_a,prior_b, posterior_a, posterior_b,origins,destinations,od_flow,od_flow_b,v_b,timecost_b,_ulabel_lane,per_b):
    """
        bi-section method line search 
    """
    lb = 0.0000000001
    ub = 0.99
    step = (lb + ub) / 2.0
    while abs(div(net_a, net_b, prior_a,prior_b, posterior_a, posterior_b,origins,destinations,od_flow,od_flow_b,v_b,step,timecost_b,_ulabel_lane,per_b)) >= 0.01 and abs(ub-lb) > 0.0001:
        if div(net_a, net_b, prior_a,prior_b, posterior_a, posterior_b,origins,destinations,od_flow,od_flow_b,v_b,step,timecost_b,_ulabel_lane,per_b) * div(net_a, net_b, prior_a,prior_b, posterior_a, posterior_b,origins,destinations,od_flow,od_flow_b,v_b,ub,timecost_b,_ulabel_lane,per_b) > 0:
            ub = step
        else:
            lb = step
        step = (lb + ub) / 2.0
    return step


def cal_limit(prior_a, posterior_a,prior_b, posterior_b):
    """
        Compute the convergence measurements
    """
    limiter = 0
    a=0
    b=0
    for l in prior_a:
        limiter += math.pow((prior_a[l]-posterior_a[l]),2)
        a+=posterior_a[l]
    for l in prior_b:
        limiter += math.pow((prior_b[l]-posterior_b[l]),2)
        a+=posterior_b[l] 
   # a=0 do not meet the condition, need to continue iteration
    if a==0:
        b=1
        print("Warning: line.py: sum posterior flow = 0")
    else:
        b=math.sqrt(limiter)/a
    return b

