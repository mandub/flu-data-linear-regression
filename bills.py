# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:54:27 2019

@author: Bill Griffin
"""

import functions_team_2 as F

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
            
            predictionDict[county][year]['rate'] = [0.0]
            predictionDict[county][year]['count'] = [0.0]
            predictionDict[county][year]['ybar'] = []
            
            #compute 
                  
            for week in range(0,len(countyDict[county][year]['rate'])):
                
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
                
                Count = round(yHat * countyDict[county][year]['pop'][week])
                if Count == 0 and yHat > 0:
                    Count = 1
                
                predictionDict[county][year]['rate'].append(yHat)
                predictionDict[county][year]['count'].append(Count)
                predictionDict[county][year]['ybar'].append(yBar)
                
            predictionDict[county][year]['ybar'].append(yBar) # evens out dictionaries
                
                
    return predictionDict


