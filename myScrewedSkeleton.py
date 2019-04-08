# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:49:04 2019

@author: annag
"""

import functions_3_10 as F


def HWforecast(countyList,years,countyDict,predictionDict,alphaMu=0.4,alphaBeta=0.3):
    #Code section from Bill Griffin
    #OUTPUT: prediction counts for all weeks staring from week 1
    #

    for county in countyList:
        for year in years:
            
            beta = 0
            y=0
            mu=0
            muOld = 0
            yHat = 0
            yBarList = []

            predictionDict[county][year]['rate'].append(0.0)
            predictionDict[county][year]['count'].append('0.0')
            predictionDict[county][year]['ybar'] = []
            
            #compute 
                  
            for week in range(len(countyDict[county][year]['rate'])):
                
                y = countyDict[county][year]['rate'][week]
                yBarList.append(y)
                
                if week > 0:
                    mu = (countyDict[county][year]['rate'][week-1] + y)/2
                mu = alphaMu*y + (1-alphaMu)*(mu+beta)
                beta = alphaBeta*(mu-muOld) + (1-alphaBeta) * beta
                yHat = mu + beta
                yBar = sum(yBarList) / len(yBarList)
                muOld = mu
                
                if yHat<0:
                    yHat = 0
                    beta = 0
                
                Count = round(yHat * countyDict[county][year]['count'][week])
                if Count == 0 and yHat > 0:
                    Count = 1
                
                predictionDict[county][year]['rate'].append(yHat)
                predictionDict[county][year]['count'].append(Count)
                predictionDict[county][year]['ybar'].append(yBar)
                
            predictionDict[county][year]['ybar'].append(yBar) # evens out dictionaries
                
                
    return predictionDict

#If you are using for the first time please enter your path as path 5 and add path5 to the pathlist

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\current.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\flu-data-linear-regression\current.csv"
pathlist = [path1, path2, path3, path4]

path = F.pathfinder(pathlist)

#Read in data and create county dictionary
countyList = []
years = list(range(1,10))
countyDict = {}

countyDict, countyList = F.readData(countyList, years, countyDict, path)

predictionDict = F.createPredictionDict(countyList,years)

alphaMu=.1
alphaBeta=.1

predictionDict = HWforecast(countyList,years, countyDict,predictionDict,alphaMu,alphaBeta)
