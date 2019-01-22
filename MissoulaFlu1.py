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
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/Mslaflu_1.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\Mslaflu_1.csv"
path4 = r"C:\Users\willi\Desktop\flu projrct\flu-data-linear-regression\Mslaflu_1.csv"



pathlist = [path1, path2, path3, path4]
names = ["Anna", "Mandub", "Jake", "Bill"]
for paths in range(len(pathlist)):
    try:
        with open(pathlist[paths]) as f:#, encoding = "utf-8"
            print ("This is", names[paths])   
            path = pathlist[paths]
    except:
        print("This is not", names[paths])
        
#Get the data from the csv file
#Put it in a dictionary:
    #key - week
    #value - count, population, rate

MslaDict = defaultdict(list)
with open(path) as f:  #, encoding = "utf-8"
    next(f)         #skip the header
    for string in f:
        data = string.split(",")
        MslaDict[data[0]].append([data[1],data[2],data[3].rstrip()])
# printing keys and values in MslaDict dictionary     
#for key, value in MslaDict.iteritems():
#    print ("Key: ", key, " - Value: ", value )
    
#%%         
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
xTrain = x[-N:] # here it will take only 10 numbers   
yTrain = y[-N:] # here it will take only 10 numbers
#print (xTrain)

#create a linear regression and plot it
slope, intercept, rvalue, pvalue,stderr =linregress(xTrain,yTrain)
x1 = np.linspace(xTrain[0],xTrain[-1],500)
y1 = intercept + slope*x1
plt.plot(np.array(xTrain),np.array(yTrain),"bo")
plt.plot(x1,y1,'-r')
plt.title = "Missoula Flu Rates"
plt.ylabel= "Flu Rates"
plt.xlabel =  "Weeks"
x1 = xTrain[-1]
plt.show







