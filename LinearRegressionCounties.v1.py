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




countyList=['SB']
countyDict={}
#countyDict=dict.fromkeys(countyList)
#from Module import dictionary
#print(dictionary)
def convertData(dataString):
    for i in range(len(dataString)):
        dataString[i]=float(dataString[i])
    return dataString
with open(path) as f:
    next(f)
    next(f)
    next(f)
    next(f)
    for county in countyList:
        countyDict[county]={'year':[],'week':[],'rate':[],'count':[],'pop':[]}
        for record in f:
            dataString = record.split(",") #split data
            data=convertData(dataString)
            year=data[1]
            week=data[2]
            rate=data[3]
            count=data[45]
            pop=data[87]
            countyDict[county]['year'].append(year)
            countyDict[county]['week'].append(week)
            countyDict[county]['rate'].append(rate)
            countyDict[county]['count'].append(count)
            countyDict[county]['pop'].append(pop)
            #print(countyDict['SB']['year'])
countyDict['SB']['rate']


#_____________________________________________________________
#Create the model

#Choose N, the week we are predicting
#from the data create the vector y and matrix X
#X is a N-1 by 1 vector of vectors xi  
#where xi refers to the vector [1,xi,xi-1,x-2,...x0,0,0,0] 
#xi is a 1xN-1 vector

rates = countyDict['SB']['rate']

#Define your variables
N=440                  #week number to predict
PredRates = 5          #number of rates used as predictors
PredictorOther = 0     #number of other predictors
n = 5                  #number of observations
q = 1+PredRates+PredictorOther        #number of predictor variables + 1 for augmentation

#formula for data
#y=week N-1-n to week N-1

#xi=week N-2-n to week N-2

def trainingMatricies(n,q,PredRates, rates):
    #Creates y a vector of our target variables. Creates vector z = (X.T)y
    #Creates A a matrix (X.T)X where X represents a matrix of predictor variables using vector xi is to predict yi.
    #xi is the vector of the previous weeks rates for the county of interest, and yi is the current weeks observed rate
    A = np.zeros(shape = (q,q))     #Initialize X the predictor matrix
    z = np.zeros(shape = (q,1))     #Initialize vector z
    
    startWeek = N-1-n     #for  y, for x startWeek - 5
    stopWeek = N-1        #for  y, for x stopWeek - 5
    y = np.matrix(rates[startWeek:stopWeek]).T               #empty list to hold the observed target rates
        
    for i in range(n):
        yi= np.matrix(y[i])        #store yi as a matrix for matrix multiplication
        x1 = [1]                   #Augment the matrix so the 1st column is 1's to predict B0
        x2 = rates[(startWeek-6+i):(stopWeek-6+i)]  #rates from the 5 weeks preceding yi
        x2.reverse()               #reverse the order so most recent is first
        x1.extend(x2)              #add the rates to the list x1
        x= np.matrix(x1).T         #create the 1xn matrix x
        A += x*(x.T)               #create A sum of xi*xi.T
        z += x*yi                  #create z sum of xi*yi

    return A,z,Y                 #Returns the predictor matrix and the target matrix  
    
A,z,Y = trainingMatricies(n,q,PredRates, rates)
betahat = np.linalg.solve(A,z)    #solve for Beta Hat   B=A.inverse*z



    
                
        







