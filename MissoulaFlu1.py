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
    #we want the week (n+1), rate (n)
pair = []
for key in MslaDict.keys():
    if int(key) == 1:
        pair.append((0, float(MslaDict[key][0][2])))
    else:
        pair.append((int(key)-1,float(MslaDict[key][0][2])))



#Flu rates over time
#create our training data        
x1=[]     #week number
y1=[]     #flu rate
for i in range(len(pair)):
    x1.append(pair[i][0])
    y1.append(pair[i][1])

#just looking at this year, so taking the last N weeks
N=10
xTrain1 = x1[-20:-N-1] # here it will take only 10 numbers   
yTrain1 = y1[-20:-N-1] # here it will take only 10 numbers

xTest1 = x1[-N:]
yTest1 = y1[-N:]


#print (yTest1)



#create a linear regression for flue rates over time and plot it
slope, intercept, rvalue, pvalue,stderr =linregress(xTrain1,yTrain1)
xa = np.linspace(xTrain1[0],xTest1[-1]+3) # can you explain
ya = intercept + slope*xa                  # can you explain this line  
plt.plot(np.array(xTrain1),np.array(yTrain1),"bo")
plt.plot(np.array(xTest1), np.array(yTest1),"ko")
plt.plot(xa,ya,'-r')
plt.title = "Missoula Flu Rates"
plt.ylabel= "Flu Rates"
plt.xlabel =  "Weeks"
plt.show


#----------------------------------------------------------
#x2 value is last weeks flu rate
#y2 vaalue is this weeks flue rate

x2=[]
y2=[]
for i in range(len(pair)-1):
    x2.append(pair[i][1])
    y2.append(pair[i+1][1])
    #print(x2[i],y2[i])
    
#just looking at this year, so taking the last N weeks
N=3
xTrain2 = np.array(x2[-20:-N-1]) # here it will take only 9 numbers   
yTrain2 = np.array(y2[-20:-N-1]) # here it will take only 9 numbers


xTest2 = x2[-N:]
yTest2 = y2[-N:]
    
#create a linear regression for flue rates over time and plot it
slope, intercept, rvalue, pvalue,stderr =linregress(xTrain2,yTrain2)
xb = np.linspace(np.amin(xTrain2),np.amax(xTrain2)) # an array from min of xTrain2 to max of xTrain2+3 to plot linear regression line
yb = intercept + slope*xb                  # regression line using values calulated from above
plt.plot(xTrain2, yTrain2,"bo")
plt.plot(xTest2,xTest2,"ko")
plt.plot(xb,yb,'-r')
plt.title = "Missoula Flu Rates"
plt.ylabel= "Flu Rates"
plt.xlabel =  "Previous Weeks Flu Rates"
plt.show
#
#

