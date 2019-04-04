# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:49:04 2019

@author: annag
"""

import functions_team_2 as F

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
AdjCountyDict = F.adjcountyDictBuild(countyList)

for county in countyList:
    countyDict[county].update({'Adjacent':AdjCountyDict[county]})  
    
NumPredWeeks = [3,4,5]         #list of options for number of weeks to use as predictor variables
OtherPredVar = []               #other predictor variables


#Predict flu rates with linear regression
#LinearRegressionDict[NumPredWeek][county][year]
TruePredPairLR = F.Linear_Regression(NumPredWeeks, OtherPredVar, years, countyDict, countyList, 'rate' )

#F.plot1("SB",8,TruePredPairLR[3])
#F.plot1("SB",7,TruePredPairLR[4]) 
#F.plot1("SB",7,TruePredPairLR[5])  

AdjacentWAve = {}
for county in countyList:
    AdjacentWAve[county]={}
    for year in years:
        AdjacentWAve[county][year] = F.AdjCounties_WtAverage(county, year, 'rate', countyDict)


OtherPredVar.append(AdjacentWAve)     
TruePredPairLR_AdjCoun = F.Linear_Regression(NumPredWeeks, OtherPredVar[0], years, countyDict, countyList, 'rate')

F.plot1("SB",4,TruePredPairLR_AdjCoun[3])
#F.plot1("SB",8,TruePredPairLR_AdjCoun[4]) 
#F.plot1("SB",8,TruePredPairLR_AdjCoun[5])  
    
##Predict flu counts with KNN

#k=4  #number of weeks that has rate closest to predictor week
#alpha=1/k;
##create an empty prediction dictionary
#predictionDictKNN={}
#for county in countyList:
#    predictionDictKNN.update({county:{}})
#    for year in years:
#        predictionDictKNN[county].update({year:{'rate':[],'count':[]}})
#avgCount = F.kNearest(alpha,k, countyList, years,countyDict, predictionDictKNN)       

#%%plotting different alpha's           
#import matplotlib.pyplot as plt 
##alpha=0.7               
#x=[i for i in range(1,len(countyDict['LA'][4]['count']))]    #weights from week 41 to 1
#y=[i for i in predictionDictKNN['LA'][4]['count'][:-1]]          
#z=[i for i in countyDict['LA'][4]['count'][1:]]
#plt.plot(x,y,'bo-')
#plt.plot(x,z,'ro-')

#
