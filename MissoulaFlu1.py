# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 10:50:00 2019

@author: annag
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
path =""
path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\Mslaflu_1.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/montana_flu_compiled_master_weekly INITIAL SAMPLE to team2.xlsx"
try:
    with open(path, encoding = "utf-8") as f:
        print ("Ok")
    path = path1  
except:
    print "This is an error message!"
try:
    with open(path, encoding = "utf-8") as f:
        print ("Ok")
    path = path2  
except:
    print "this is not mandub"
    
MslaDict = defaultdict(list)
with open(path, encoding = "utf-8") as f:
    next(f)         #skip the header
    for string in f:
        data = string.split(",")
        MslaDict[data[0]].append([data[1],data[2],data[3].rstrip()]) 
        

MslaDict['1']
x = list(MslaDict.keys())

for key in MslaDict.keys():
    print(key)









