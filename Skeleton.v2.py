# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:49:04 2019

@author: annag
"""

import functions_3_10 as F

#If you are using for the first time please enter your path as path 5 and add path5 to the pathlist

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\Apr6\current.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\flu-data-linear-regression\initial_flu.csv"
pathlist = [path1, path2, path3, path4]

path = F.pathfinder(pathlist)



countyList = []
years = list(range(1,10))
countyDict = {}
#Read in data and create county dictionary, county List
countyDict, countyList = F.readData(countyList, years, countyDict, path)

#Create Dictionary of Adjacent counties
AdjCountyDict = F.adjcountyDictBuild(countyList)
#Add AdjCountDict to countyDict
for county in countyList:
    countyDict[county].update({'Adjacent':AdjCountyDict[county]})  

#%%
#Linear Regression without adjacent counties 
#Found the best starting values to enter into Linear Regression without adjacent counties 
VoI = 'count'
OtherPredVar = []
PredWeek = 3
start = 6
alpha0 =  0
alpha1 = 0

predictionDict, YTrue = F.Linear_Regression(OtherPredVar, years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
F.plot1("SB", 8, YTrue, predictionDict, VoI)

    
#%% 

#This one is not quite right

#Van's Exponentially weighted linear regression
#OtherPredVar = []
#PredWeek = 1
#start = 5
#alpha0 = 0.4
#alpha1 = 0
#predictionDict, YTrue = F.Linear_Regression(OtherPredVar, years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
#F.plot1("SB", 8, YTrue, predictionDict, VoI)
  
#%% 

#Anna's Exponentially weighted linear regression
OtherPredVar = []
PredWeek = 1
start = 10
alpha0 = 0
alpha1 = 0.7
predictionDict, YTrue = F.Linear_Regression(OtherPredVar, years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
F.plot1("SB", 8, YTrue, predictionDict, VoI)
 
#%%

#Linear Regression with adjacent counties

#Create weighted averages for adjacent counties
AdjacentWAve = {}
for county in countyList:
    AdjacentWAve[county]={}
    for year in years:
        AdjacentWAve[county][year] = F.AdjCounties_WtAverage(county, year, VoI, countyDict)

#Found the best starting values for Linear Regression with adjacent counties
PredWeek = 1
start = 6
alpha0 = 0
alpha1 = 0
#Add AdjacentWAve to OtherPredVar List
OtherPredVar.append(AdjacentWAve) 
    
predictionDictAdj, YTrueAdj = F.Linear_Regression( OtherPredVar[0], years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
F.plot1("SB",8, YTrueAdj, predictionDictAdj, VoI)   

#%% 

#This one is not quite right yet


#adjacent counties, Van's exponentially weighted linear regression  
#PredWeek = 1
#start = 10
#alpha0 = .4
#alpha1 = 0
##Add AdjacentWAve to OtherPredVar List
#
#    
#predictionDictAdj, YTrueAdj = F.Linear_Regression( OtherPredVar[0], years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
#F.plot1("SB",8, YTrueAdj, predictionDictAdj, VoI)   

#%%  

#adjacent counties, Anna's exponentially weighted linear regression
PredWeek = 1
start = 5
alpha0 = 0
alpha1 = 0.65
#Add AdjacentWAve to OtherPredVar List

    
predictionDictAdj, YTrueAdj = F.Linear_Regression( OtherPredVar[0], years, countyDict, countyList, VoI, PredWeek, start, alpha0, alpha1 )
F.plot1("SB",8, YTrueAdj, predictionDictAdj, VoI)   
#%%
#KNN

predictionDictKN = F.createPredictionDict(countyList, years)    
predictionDictKN = F.kNearest(predictionDictKN,countyList, years, countyDict)  

    
#%%

predictionDictKNCon = F.createPredictionDict(countyList, years)
predictionDictKNCon = F.kNearestCon(predictionDictKNCon,countyList,years, countyDict)
