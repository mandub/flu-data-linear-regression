# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 14:55:37 2019

@author: annag
"""


import functions as F
import numpy as np


#If you are using for the first time please enter your path as path 5 and add path5 to the pathlist

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\current.csv"
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
                y = np.matrix(countyDict[county][year]['rate'][i+PredWeek])
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

def InitialTrainingMatricies( countyList, years, D, Aci, Zci,q):   
    for county in countyList:
        Aci[county]={}
        Zci[county]= {}
        for year in years:
            Aci[county][year]= np.zeros(shape =(q,q))
            Zci[county][year]= np.matrix(np.zeros(shape = (q,1)))        
            for i in range(0, 10):
                yi = D[county][year][i][0]
                xi = D[county][year][i][1]
                Aci[county][year] += xi*xi.T
                Zci[county][year] += xi*yi
    return Aci, Zci

def NextTrainingMatricies( county, year, D, Aci, Zci,q,j):         
    yi = D[county][year][j][0]
    xi = D[county][year][j][1]
    Aci[county][year] += xi*xi.T
    Zci[county][year] += xi*yi
    return Aci, Zci




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
def InitialBetaSolver(countyList, years, Aci, Zci, Bci,q):
    for county in countyList:
        Bci[county] = {}
        for year in years:
            #Bc[county][year]=[]
            A = Aci[county][year]
            Z = Zci[county][year]
            try:
                b = np.linalg.solve(A,Z)
                Bci[county][year]=b
            except:
                Bci[county][year]=(np.zeros(shape = (q,1)))
                pass
    return Bci

def NextBetaSolver(county, year, Aci, Zci, Bci,q,j):
    A = Aci[county][year]
    Z = Zci[county][year]
    try:
        b = np.linalg.solve(A,Z)
        Bci[county][year]=b
    except:
        Bci[county][year]=(np.zeros(shape = (q,1)))
        pass
    return Bci


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

def initialpredictionDict(countyList, years, D, Bci,q,PredWeek):
    TruePredPair[PredWeek] = {}
    for county in countyList:
        TruePredPair[PredWeek][county]={}
        for year in years:
            TruePredPair[PredWeek][county][year] = []
            X = np.matrix(np.zeros(shape = (10, q)))
            for j in range(10):
                X[j,] = D[county][year][j][1].T
            B = Bci[county][year]
            pred = X*B
            for j in range(10):
                TruePredPair[PredWeek][county][year].append((float(D[county][year][j][0]),float(pred[j,])))

    return TruePredPair

def NextpredictionDict(county, year, D, Bci,q,TruePredPair, j, PredWeek):
    X = np.matrix(np.zeros(shape = (1, q)))
    X = D[county][year][j][1].T
    B = Bci[county][year]
    pred = X*B
    TruePredPair[PredWeek][county][year].append((float(D[county][year][j][0]),float(pred)))

    return TruePredPair


       
NumPredWeeks = [3,4,5]         #list of options for number of weeks to use as predictor variables
OtherPredVar = []

def Linear_Regression(NumPredWeeks, OtherPredVar):
    
    
    
    for i in NumPredWeeks:
        PredWeek = i
        q = 1 + PredWeek + len(OtherPredVar)
        D = {}
        D = Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,q)
        print('PredWeek =', PredWeek)
        print(D['SB'][8][5:10])
        Aci = {}
        Zci = {}
        Aci, Zci = InitialTrainingMatricies( countyList, years, D, Aci, Zci,q)
        Bci = {}
        Bci = InitialBetaSolver(countyList, years, Aci, Zci, Bci, q)
        TruePredPair = initialpredictionDict(countyList, years, D, Bci,q, PredWeek)
        for county in countyList:
            for year in years:
                for j in range(10,len(D[county][year])):
                    Aci, Zci = NextTrainingMatricies( county, year, D, Aci, Zci,q,j)
                    Bci = NextBetaSolver(county, year, Aci, Zci, Bci, q, j)
                    TruePredPair = NextpredictionDict(county, year, D, Bci,q,TruePredPair, j, PredWeek)
    return TruePredPair

TruePredPair = Linear_Regression(NumPredWeeks, OtherPredVar )









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

def plot1(County,Year, TruePredPair):
    Year= Year
    y = range(len (TruePredPair[County][Year]))
    x = []
    z = []
    for i in range(len (TruePredPair[County][Year])):       
        x.append(TruePredPair[County][Year][i][0])
        z.append(TruePredPair[County][Year][i][1])
    #actualNames[counties.index(County)]
    Title= County +" Year " +str (Year)
    plt.title(Title)
    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")
    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()


for year in years:
    initialplot1("SB",year,TruePredPair[4])

initialplot1("SB",8,TruePredPair[3])
initialplot1("SB",8,TruePredPair[4]) 
initialplot1("SB",8,TruePredPair[5])   




