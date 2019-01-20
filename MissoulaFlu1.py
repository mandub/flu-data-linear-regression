# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 10:50:00 2019

@author: annag
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\Mslaflu_1.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/montana_flu_compiled_master_weekly INITIAL SAMPLE to team2.xlsx"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\Mslaflu_1.csv"
path4 = r"C:\Users\willi\Desktop\flu projrct\flu-data-linear-regression\Mslaflu_1.csv"

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
    
try:   
    with open(path4, encoding = "utf-8") as f:
        print ("Ok")
        path = path4      
except:
    print ("this is not Bill")
    
    
#Get the data from the csv file
#Put it in a dictionary:
    #key - week
    #value - count, population, rate

MslaDict = defaultdict(list)
with open(path, encoding = "utf-8") as f:
    next(f)         #skip the header
    for string in f:
        data = string.split(",")
        MslaDict[data[0]].append([data[1],data[2],data[3].rstrip()]) 
        
#Create a list of pairs that are staggered
    #we want the week (n), rate (n+1)
pair = []
for key in MslaDict.keys():
    if int(key) == 1:
        pair.append((int(key),0))
    else:
        pair.append((int(key)+1,float(MslaDict[key][0][2])))

#create our training data        
x=[]     #week number
y=[]     #flu rate
for i in range(len(pair)):
    x.append(pair[i][0])
    y.append(pair[i][1])

#just looking at this year, so taking the last N weeks
N=10
xTrain = x[-N:]  
yTrain = y[-N:]

#create a linear regression and plot it
slope, intercept, rvalue, pvalue,stderr =linregress(xTrain,yTrain)
x1 = np.linspace(xTrain[0],xTrain[-1],500)
y1 = intercept + slope*x1
plt.plot(np.array(xTrain),np.array(yTrain),"bo")
plt.plot(x1,y1,'-r')
x1 = xTrain[-1]








