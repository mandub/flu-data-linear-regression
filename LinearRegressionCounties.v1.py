# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:54:26 2019

@author: annag

Linear Regression Model v2
"""

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\initial_flu.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\Users\willi\Desktop\flu projrct\flu-data-linear-regression\initial_flu.csv"



pathlist = [path1, path2, path3, path4]
names = ["Anna", "Mandub", "Jake", "Bill"]
for paths in range(len(pathlist)):
    try:
        with open(pathlist[paths]) as f:#, encoding = "utf-8"
            print ("This is", names[paths])   
            path = pathlist[paths]
            break
    except:
        print("This is not", names[paths])
        
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

CountyDict = defaultdict(list)
yeardata=defaultdict(list)

with open(path) as f:  #, encoding = "utf-8"
    next(f)         #skip the header
    next(f)
    for string in f:
        if string.startswith("revised"):
            CountyNames=string.split(",")
            del(CountyNames[0:3],CountyNames[-1])
            CountyNames=list(set(CountyNames))
        else:
            data = string.split(",")  
            yeardata[data[1]].append((data[2],data[3:45]))
del yeardata['year']

            
for name in CountyNames:
    CountyDict[name]=defaultdict(list)
    countIndex=CountyNames.index(name)
    #print(countIndex)
    for year in yeardata.keys():
        CountyDict[name][year]=defaultdict(list)
        for week in yeardata[year]:
            CountyDict[name][year][week[0]]=[]
            print(yeardata[year][int(week[0])-1][1][countIndex])

            #print(int(week[0]))



    
                
        







