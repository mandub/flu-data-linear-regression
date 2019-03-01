# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:49:04 2019

@author: annag
"""

import functions as F

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
AdjCountyDict = F.adjcountyDictBuild(countyList)

for county in countyList:
    countyDict[county].update({'Adjacent':AdjCountyDict[county]})  
    
NumPredWeeks = [3,4,5]         #list of options for number of weeks to use as predictor variables
OtherPredVar = []               #other predictor variables
opvn = len(OtherPredVar)

#Predict flu rates with linear regression
#LinearRegressionDict[NumPredWeek][county][year]
LinearRegressionDict, YTrueLG = F.Linear_Regression(NumPredWeeks, OtherPredVar, opvn, years, countyDict, countyList)

for year in years:
    F.plot1("MS",year,YTrueLG[5],LinearRegressionDict[5])

AdjacentWAve = {}
for county in countyList:
    AdjacentWAve[county]={}
    for year in years:
        AdjacentWAve[county][year] = F.AdjCounties_WtAverage(county, year, 'rate', countyDict)
#for i in range(len(AdjacentWAve['SB'][1])):
#    print((AdjacentWAve['SB'][1][i]))


OtherPredVar.append(AdjacentWAve)   
opvn = len(OtherPredVar)  
LinearRegressionWithAdjCounties, YTrueLGAC = F.Linear_Regression(NumPredWeeks, OtherPredVar[0], opvn, years, countyDict, countyList)

for year in years:
    F.plot1("MS",year,YTrueLGAC[5],LinearRegressionWithAdjCounties[5])




