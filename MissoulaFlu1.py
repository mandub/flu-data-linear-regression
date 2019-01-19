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

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\Mslaflu_1.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/montana_flu_compiled_master_weekly INITIAL SAMPLE to team2.xlsx"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\Mslaflu_1.csv"
try:
    
 
    with open(path1, encoding = "utf-8") as f:
        print ("Ok")   
        path = path1
except:
    print ("This is an error message!")
try:   
    with open(path2, encoding = "utf-8") as f:
        print ("Ok")
        path = path2      
except:
    print ("this is not mandub")

try:   
    with open(path3, encoding = "utf-8") as f:
        print ("Ok")
        path = path3      
except:
    print ("this is not Jake")
    
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









