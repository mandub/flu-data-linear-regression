# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 14:55:37 2019

@author: annag
"""


import functions as F
import numpy as np


#If you are using for the first time please enter your path as path 5 and add path5 to the pathlist

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\initial_flu.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\flu-data-linear-regression\initial_flu.csv"
pathlist = [path1, path2, path3, path4]

path = F.pathfinder(pathlist)

#Read in data and create county dictionary
countyList = []
years = list(range(1,10))
countyDict = {}

countyDict, countyList = F.readData(countyList, years, countyDict, path)


def Data(countyList, years, countyDict, PredWeek, OtherPredVar, D, q):
    for county in countyList:
        D[county]={}
        for year in years:
            D[county][year]=[]
            for i in range(len(countyDict[county][year]['rate'])-(PredWeek+1)):
                y = np.matrix(countyDict[county][year]['rate'][i+PredWeek+1])
                x0 = [1]
                x1R = []
                for j in range(i,i+PredWeek):
                    x1R.append(countyDict[county][year]['rate'][j])
                x1R.reverse()
                x0.extend(x1R)
                if len(OtherPredVar) != 0:
                    x0.extend(OtherPredVar)
                X = np.matrix(x0).reshape(q,1)
                D[county][year].append((y,X))
    return D

def TrainingMatricies( countyList, years, D, Ac, Zc,q):   
    for county in countyList:
        Ac[county]={}
        Zc[county]= {}
        for year in years:
            Ac[county][year]= np.zeros(shape =(q,q))
            Zc[county][year]= np.matrix(np.zeros(shape = (q,1)))        
            for i in range(0, len(D[county][year])-1):
                yi = D[county][year][i][0]
                xi = D[county][year][i][1]
                Ac[county][year] += xi*xi.T
                Zc[county][year] += xi*yi
    return Ac, Zc

def BetaSolver(countyList, years, Ac, Zc, Bc,q):
    for county in countyList:
        Bc[county] = {}
        for year in years:
            #Bc[county][year]=[]
            A = Ac[county][year]
            Z = Zc[county][year]
            try:
                b = np.linalg.solve(A,Z)
                Bc[county][year]=b
            except:
                Bc[county][year]=(np.zeros(shape = (q,1)))
                pass
    return Bc

def predictionDict(countyList, years, D, Bc,q):
    YTrue = {}
    YHat = {}
    for county in countyList:
        YTrue[county]={}
        YHat[county]={}
        for year in years:
            YTrue[county][year] = []
            X = np.matrix(np.zeros(shape = (len(D[county][year]), q)))
            for i in range(len(D[county][year])):
                YTrue[county][year].append(float(D[county][year][i][0]))
                X[i,] = D[county][year][i][1].T
            B = Bc[county][year]
            YHat[county][year] = X*B
    return YTrue, YHat


       
NumPredWeeks = [3,4,5]         #list of options for number of weeks to use as predictor variables
OtherPredVar = []

def Linear_Regression(NumPredWeeks, OtherPredVar):
    LinRegPred = {}
    YTrues = {}
    for i in NumPredWeeks:
        PredWeek = i
        q = 1 + PredWeek + len(OtherPredVar)
        D = {}
        D = Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,q)
        Ac = {}
        Zc = {}
        Ac, Zc = TrainingMatricies( countyList, years, D, Ac, Zc,q)
        Bc = {}
        Bc = BetaSolver(countyList, years, Ac, Zc, Bc, q) 
        YTrue, YHat = predictionDict(countyList, years, D, Bc,q)
        LinRegPred[i]= YHat
        YTrues[i] = YTrue
    return LinRegPred, YTrues

LinRegPred, YTrue = Linear_Regression(NumPredWeeks, OtherPredVar )









import matplotlib.pyplot as plt

def plot1(County,Year, YTrue, predictionDict):
    Year= Year
    y = range(len (YTrue[County][Year]))
    x = YTrue[County][Year]
    z = predictionDict[County][Year]
    #actualNames[counties.index(County)]
    Title= County +" Year " +str (Year)
    plt.title(Title)
    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")
    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()

for year in years:
    plot1("SB",year,YTrue[5],LinRegPred[5])


    




