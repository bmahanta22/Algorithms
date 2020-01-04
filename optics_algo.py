# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 17:38:43 2020

@author: Birina Mahanta
"""

from sklearn.datasets import make_blobs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

X,y = make_blobs(n_samples=10,n_features=2,centers=2,random_state=19) 
 ### X is the data and y are cluster labels. 

master_df = pd.DataFrame(columns=["points","cluster","reachability_dist","core_dist"])
master_df["points"] = list(X)
master_df["cluster"] = [0]*X.shape[0]
master_df["reachability_dist"] = [1000]*X.shape[0]
master_df["core_dist"]=[0]*X.shape[0]

min_pts = 3
eps = 5

def unclustered_data(p):
    '''checking if the point is clustered or not'''
    if master_df["cluster"][p]==0:
        return "unclustered point"
    else:
        return "clustered point"




def nbd_points(p):
    '''list of neighbourhood points of pth indexed point'''
    nb_points = []
    q = master_df["points"][master_df.index != p]
    for i in q.index:
        d = np.linalg.norm(X[p]-q[i])
        if (d<eps):
            nb_points.append((i,d))  #index and distance
    return nb_points        
     

def core_reachability_dist(p,v):
    v.sort(key = lambda x: x[1])
    c_dist = v[min_pts-1][1]    ###finding the core distance
    master_df.iloc[p,3] = c_dist  ##updating the core distance the original dataframe
    for i in range(len(v)):
            reach_dist = max(c_dist,v[i][1])   ##finding reachability distance
            if reach_dist<master_df["reachability_dist"][v[i][0]]:
               master_df["reachability_dist"][master_df.index== v[i][0]] = reach_dist
                ##updating reachability distance if condition is fulfilled

c=0
for i in range(X.shape[0]):
    if unclustered_data(i) == "unclustered point": 
           if len(nbd_points(i))>=min_pts:
               c+=1
               master_df.iloc[i,1] = c
               v = nbd_points(i)
               core_reachability_dist(i,v)
               for i in range(len(v)):
                   if unclustered_data(v[i][0]) == "unclustered point": 
                       if len(nbd_points(v[i][0]))>=min_pts:
                           master_df.iloc[v[i][0],1] = master_df.iloc[i,1]
                           u = nbd_points(v[i][0])
                           core_reachability_dist(v[i][0],u) 
                       else:
                           pass
           else:
               pass
