# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 14:55:37 2019

@author: annag
"""


import functions_team_2 as F
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

import numpy as np
import matplotlib.pyplot as plt

 

def pathfinder(pathlist):
    #Input: list of paths
    #Output: correct path for user
    #
    names = ["Anna", "Mandub", "Jake", "Bill", "Other"]
    for paths in range(len(pathlist)):
        try:
            with open(pathlist[paths]):#, encoding = "utf-8"
                print ("This is", names[paths])   
                path = pathlist[paths]
                break
        except:
            print("This is not", names[paths])
    return(path)


###############################################################################
#READING IN THE FILE
###############################################################################


def convertData(dataString):
    #Input: string of data
    #Output: float of data
    #
    for i in range(len(dataString)):
        dataString[i]=float(dataString[i])
    return dataString



def readData(countyList, years, countyDict, path):
    #INPUT: Initialized empty list for couties, list of years, initialized empty dictionary for counties, path
    #OUTPUT: Nested dictionary countyDict{county:{year:{'rate'=[],'pop'=[],'county'=[]}}}
    #
    with open(path) as f:
        line = f.readline()
        lineString=line.split(",")
        if lineString[6] == 'Two Char':           #use first 3rd line to make list of counties
            for string in lineString:
                if string not in countyList:
                    countyList.append(string)
            countyList = countyList[2:-1]        #get rid of etxras
            for county in countyList:            #initialized dict of dict
                countyDict[county]={}
                for year in years:
                    countyDict[county][year]={'rate':[],'count':[],'pop':[]}
            next(f)
            next(f)
            next(f)
            next(f)
        for record in f:                         #start on first line of data
            dataString = record.split(",")
            data = convertData(dataString)       #convert data to floats
            for i in range(7,59):    
                countyDict[countyList[i-7]][data[3]]['rate'].append(data[i])   #append rate data
            for i in range(59,111):
                countyDict[countyList[i-59]][data[3]]['count'].append(data[i]) #append count data
            for i in range(111,163):
                countyDict[countyList[i-111]][data[3]]['pop'].append(data[i])   #append pop data
    return countyDict, countyList

###############################################################################
# LINEAR REGRESSION
###############################################################################


def Data(countyList, years, countyDict, PredWeek, OtherPredVar, D, VoI):
    opvn = len(OtherPredVar)
    for county in countyList:
        D[county]={}
        for year in years:
            D[county][year]=[]
            for i in range(len(countyDict[county][year][VoI])-(PredWeek+1)):
                y = np.matrix(countyDict[county][year][VoI][i+PredWeek])
                x0 = [1]
                x1R = []
                for j in range(i,i+PredWeek):
                    x1R.append(countyDict[county][year][VoI][j])
                x1R.reverse()
                x0.extend(x1R)
                q = 1 + PredWeek + opvn 
                if opvn != 0:
                    if county != 'STATE':
                        x0.append(OtherPredVar[county][year][i+PredWeek])
                        q = 1 + PredWeek + 1
                    else:
                        x0.append(0)
                        q = 1 + PredWeek + 1                        
                X = np.matrix(x0).reshape(q,1)
                D[county][year].append((y,X))
    return D, q

def InitialTrainingMatricies( countyList, years, D, Aci, Zci, q, start):   
    for county in countyList:
        Aci[county]={}
        Zci[county]= {}
        for year in years:
            Aci[county][year]= np.zeros(shape =(q,q))
            Zci[county][year]= np.matrix(np.zeros(shape = (q,1)))        
            for i in range(0, start):
                yi = D[county][year][i][0]
                xi = D[county][year][i][1]
                Aci[county][year] += xi*xi.T
                Zci[county][year] += xi*yi
    return Aci, Zci

def NextTrainingMatricies( county, year, D, Aci, Zci, j, start):         
    yi = D[county][year][j][0]
    xi = D[county][year][j][1]
    yrem = D[county][year][j-start][0]
    xrem = D[county][year][j-start][1]    
    Aci[county][year] += xi*xi.T
    Zci[county][year] += xi*yi
    Aci[county][year] -= xrem*xrem.T
    Zci[county][year] -= xrem*yrem
    return Aci, Zci

def InitialBetaSolver(countyList, years, Aci, Zci, Bci, q):
    for county in countyList:
        Bci[county] = {}
        for year in years:
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

def createPredictionDict(countylist):
    predictionDict={}
    for county in countyList:
        predictionDict.update({county:{}})
        for year in years:
            predictionDict[county].update({year:{'rate':[],'count':[],'ybar':[]}})
    return predictionDict

def initialpredictionDict(countyList, years, D, Bci, q, start):
    YTrue = {}
    predictionDict = createPredictionDict(countyList)
    for county in countyList:
        YTrue[county]={}
        for year in years:
            YTrue[county][year] = []
            X = np.matrix(np.zeros(shape = (start, q)))
            for j in range(start):
                X[j,] = D[county][year][j][1].T
            B = Bci[county][year]
            pred = X*B
            ysum = 0
            for j in range(start):
                if float(pred[j,]) <0:
                    pred[j,] = 0
                predictionDict[county][year]['rate'].append(float(pred[j,]))
                ysum += float(D[county][year][j][0])

                ybar = ysum/(j+1)
                predictionDict[county][year]['ybar'].append(ybar)
                YTrue[county][year].append(float(D[county][year][j][0]))
    return predictionDict, ysum, YTrue

def NextpredictionDict(county, year, D, Bci,q, predictionDict, j, YTrue, ysum):
    X = np.matrix(np.zeros(shape = (1, q)))
    X = D[county][year][j][1].T
    B = Bci[county][year]
    pred = X*B
    if float(pred) <0:
        pred = 0
    predictionDict[county][year]['rate'].append(float(pred))
    ysum = predictionDict[county][year]['ybar'][j-1]*(j)
    ysum += float(D[county][year][j][0])
    ybar = ysum/(j+1)
    predictionDict[county][year]['ybar'].append(ybar)
    YTrue[county][year].append(float(D[county][year][j][0]))    
    return predictionDict, ysum, YTrue


def Linear_Regression(OtherPredVar, years, countyDict, countyList, VoI, PredWeek, start):
    #INPUT: array of possible # of pred weeks, List of other pred var, number of pred var, list of years and counties, county dict
    #OUTPUT:dict of predictions by pred weeks, county, year  for each wee, dict of True values by county by year, for each week
    #LinRegPred[# of weeks][county][year] , YTrues[# of weeks][county][year]
    D = {}
    D, q = Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,VoI)
    Aci = {}
    Zci = {}
    Aci, Zci = InitialTrainingMatricies( countyList, years, D, Aci, Zci, q, start)
    Bci = {}
    Bci = InitialBetaSolver(countyList, years, Aci, Zci, Bci, q)
    predictionDict, ysum, YTrue = initialpredictionDict(countyList, years, D, Bci, q, start)
    #TruePredPair = initialpredictionDict(countyList, years, TruePredPair, D, Bci, PredWeek, q)
    for county in countyList:
        for year in years:
            for j in range(start,len(D[county][year])):
                predictionDict, ysum, YTrue = NextpredictionDict(county, year, D, Bci,q,predictionDict, j, YTrue, ysum)
                Aci, Zci = NextTrainingMatricies( county, year, D, Aci, Zci,j, start)
                Bci = NextBetaSolver(county, year, Aci, Zci, Bci, q, j)
    return predictionDict, YTrue


def plot1(County,Year, YTrue, predictionDict):
    Year= Year
    x = range(len (YTrue[County][Year]))
    y = YTrue[County][Year]
    z = predictionDict[County][Year]['rate']
    yb = predictionDict[County][Year]['ybar']
    Title= County +" Year " +str (Year)
    plt.title(Title)
    plt.plot(x, yb, 'go-', linewidth = 2.0, label = "ybar")
    plt.plot(x, y, 'bo-', linewidth = 2.0, label = "Observed Rates")
    plt.plot(x, z, 'ro-', linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()

       
OtherPredVar = []
countyList = []
years = list(range(1,10))
countyDict = {}
countyDict, countyList = F.readData(countyList, years, countyDict, path)
AdjCountyDict = F.adjcountyDictBuild(countyList)

for county in countyList:
    countyDict[county].update({'Adjacent':AdjCountyDict[county]})  
    

PredWeek = 2
start = 5

predictionDict, YTrue = Linear_Regression(OtherPredVar, years, countyDict, countyList, 'rate', PredWeek, start )
plot1("SB",8,YTrue, predictionDict)
 
AdjacentWAve = {}
for county in countyList:
    AdjacentWAve[county]={}
    for year in years:
        AdjacentWAve[county][year] = F.AdjCounties_WtAverage(county, year, 'rate', countyDict)

PredWeek = 2
start = 6

OtherPredVar.append(AdjacentWAve)     
predictionDictAdj, YTrueAdj = Linear_Regression( OtherPredVar[0], years, countyDict, countyList, 'rate', PredWeek, start )
#
plot1("SB",8, YTrueAdj, predictionDictAdj)
#F.plot1("SB",8,TruePredPairLR_AdjCoun[4]) 
#F.plot1("SB",8,TruePredPairLR_AdjCoun[5])  









#def plot1(County,Year, TruePredPair):
#    Year= Year
#    y = range(len (TruePredPair[County][Year]))
#    x = []
#    z = []
#    for i in range(len (TruePredPair[County][Year])):       
#        x.append(TruePredPair[County][Year][i][0])
#        z.append(TruePredPair[County][Year][i][1])
#    #actualNames[counties.index(County)]
#    Title= County +" Year " +str (Year)
#    plt.title(Title)
#    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")
#    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")
#    plt.legend(loc = "upper right")
#    plt.show()
#






