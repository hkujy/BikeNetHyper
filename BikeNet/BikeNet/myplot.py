# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:29:55 2019

@author: 99335
"""


import matplotlib.pylab as pl
import pandas as pd
def drew_lines():
    df = pd.read_csv("Iter.txt",header=None)
    x= df[0]
    y = df[1]
    # print(x)
    # print(y)
    # x = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    # y = [0.14948457218320477,0.005659542576882991,0.04356962394355591,0.002997302183375481, 0.02713460123479413, 0.002109024720013894, 0.017654866984622063, 0.0015232841327758606, 0.014057391788740114, 0.0012593661464550066, 0.01012298540302038, 0.0009950440437616226,  0.009077814154627533, 0.0008958341250388494, 0.007056800015181458, 0.0007324511409461337, 0.008664244946636793, 0.000588105933036304, 0.005532115275168927, 0.0006100158554697515, 0.005107949448979659, 0.0005494944107548127, 0.004352792601259831, 0.000488044003293672]
    pl.plot(x,y)
    pl.grid(True) 
    pl.title("Convergence Trend", fontsize=16)
    pl.xlabel("Iteration times", fontsize=14)
    pl.ylabel("Value", fontsize=14)
    pl.show()

def CheckOdPair():
    """
        remark: the check for the OD pair OD valid for the four OD pair case
    """
    df = pd.read_csv("Iter_OD.txt")
    # print (df)
    od_cost_a = {"1":[],"2":[],"3":[],"4":[]}
    od_cost_b = {"1":[],"2":[],"3":[],"4":[]}
    # print(df.shape[0])
    num_row = df.shape[0]
    for i in range(0,df.shape[0]):
        if df["O"][i]=="N001" and df["D"][i] =="N002":
            od_cost_a["1"].append(df["aCost"][i])
            od_cost_b["1"].append(df["bCost"][i])
        if df["O"][i]=="N001" and df["D"][i] =="N003":
            od_cost_a["2"].append(df["aCost"][i])
            od_cost_b["2"].append(df["bCost"][i])
        if df["O"][i] =="N004" and df["D"][i] =="N002":
            od_cost_a["3"].append(df["aCost"][i])
            od_cost_b["3"].append(df["bCost"][i])
        if df["O"][i] =="N004" and df["D"][i] =="N003":
            od_cost_a["4"].append(df["aCost"][i])
            od_cost_b["4"].append(df["bCost"][i])

    # print(od_cost_a["1"])
    pl.figure()
    # pl.plot(od_cost_a["1"])
    pl.plot(od_cost_a["2"])
    # pl.plot(od_cost_a["3"])
    # pl.plot(od_cost_a["4"])
    pl.title("Convergence of Auto Cost", fontsize=16)
    pl.show()
    pl.figure()
    pl.title("Convergence of Bike Cost", fontsize=16)
    # pl.plot(od_cost_b["1"])
    pl.plot(od_cost_b["2"])
    # pl.plot(od_cost_b["3"])
    # pl.plot(od_cost_b["4"])
    # TODO: Check the cost function of bike
    pl.show()



def plot_main():
    drew_lines()
    CheckOdPair()
