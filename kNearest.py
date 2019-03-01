# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:29:36 2019

@author: vanna
"""

import sys,os
#path = r'C:\Users\vanna\Desktop\MAT567'
#sys.path.insert(0,path)
#if path not in sys.path:
#    sys.path.append(path) #add the path
#path = r'C:\Users\vanna\Desktop\MAT567\data567\initial_flu.csv'
path = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\initial_flu.csv"

#convert all data strings to floating point numbers
def convertData(dataString):
    for i in range(len(dataString)):
        dataString[i]=float(dataString[i])
    return dataString

countyList = []
years = list(range(1,10))
countyDict = {}
with open(path) as f:
    next(f)
    next(f)
    line = f.readline()
    lineString=line.split(",")
    if lineString[0] == 'revised':
        for string in lineString:
            if string not in countyList:
                countyList.append(string)
        countyList = countyList[2:-1]
        for county in countyList:    
            countyDict[county]={}
            for year in years:
                countyDict[county][year]={'rate':[],'count':[]}
        next(f)
    for record in f:
        dataString = record.split(",")
        data = convertData(dataString)
        for i in range(3,len(data)-84):    
            countyDict[countyList[i-3]][data[1]]['rate'].append(data[i])
        for i in range(45,len(data)-42):
            countyDict[countyList[i-45]][data[1]]['count'].append(data[i])
#           

#                countyDict[countyList[i]][data[1]]['rate'].append(data[i])
#            except (IndexError):
#                pass
    #                try:
#                    countyDict[countyList[i-42]][data[1]]['count'].append(data[i])
#                except(IndexError):
#                    print(i)
                
                
                
    
        
##        
#
#
#
#print (countyList)
#countyDict={}
#for county in countyList:    
#    countyDict[county]={}
#    for year in years:
#        countyDict[county][year]={'pop':[],'week':[],'rate':[],'count':[]}
#
#def countyData(county,lineString):
#    for string in lineString:
#        if string==county+' '+'rate':
#            position_rate=lineString.index(string)
#        if string==county+' '+'count':
#            position_count=lineString.index(string)
#        if string==county+' '+'pop':
#            position_pop=lineString.index(string)
#        for record in f:
#            dataString = record.split(",") #split data
#            data=convertData(dataString)   
#            for year in years:
#                if data[1]==year:
#                    rate=data[position_rate]       #position of county's rate
#                    countyDict[county][year]['rate'].append(rate)
#                    count=data[position_count]     #position of county's counts
#                    countyDict[county][year]['count'].append(count)
##                        pop=data[position_pop]         #position of county's population
##                        countyDict[county]['pop']=pop
#                    week=data[2]                   #position of week
#                    countyDict[county][year]['week'].append(week)
#    return countyDict
#
#
#with open(path) as f:
#    next(f)
#    next(f)
#    next(f)
#    line=f.readline()
#    lineString=line.split(",")
#    for county in countyList:
#        countyDict.update(countyData(county,lineString))



##%% K-Nearest Exponential Function
#def kNearest(week):
#    sumWeight=0
#    for i in range(week-1):
#        weight=alpha*(1-alpha)**i      #exponential weights of each rate
#        weightedRate=weight*countyDict[county][year]['rate'][week-2-i]
#        sumWeight += weightedRate        #sum of weighted rates 
#        avgRate=sumWeight/(week-1)       #average of weighted rates
#    return avgRate
##%% K-Nearest Conventional Function
#def convkNearest(week):
#    sumWeight=0
#    for i in range(k):
#        weight=1/k
#        weightedRate=weight*countyDict[county][year]['rate'][week-2-i]
#        sumWeight += weightedRate        #sum of weighted rates 
#        avgRateCon=sumWeight/k       #average of weighted rates
#    return avgRateCon
##%%Run k-nearest exponential function
#k=4   #number of weeks that has rate closest to predictor week
#alpha=1/k;
#N=300 # week that we want to predict
#year=7 #year want to use to predict
#week=33 #week want to predict
#avgRate=kNearest(week)
#avgRateCon=convkNearest(week)
#print(avgRate,avgRateCon)
##%%plotting different alpha's           
#import matplotlib.pyplot as plt 
##alpha=0.7               
#x=[alpha*(1-alpha)**i for i in range(week-1)]    #weights from week 41 to 1
#y=[alpha*(1-alpha)**i*countyDict[county][year]['rate'][week-2-i] for i in range(week-1)]          
#plt.plot(x,y,'bo-')
