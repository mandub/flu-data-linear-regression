# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 23:13:59 2019

@author: vanna
"""

import sys,os
path = r'C:\Users\vanna\Desktop\MAT567'
sys.path.insert(0,path)
if path not in sys.path:
    sys.path.append(path) #add the path
path = r'C:\Users\vanna\Desktop\MAT567\data567\initial_flu.csv'
countyList=['SB','CS']
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
            print(countyDict['SB']['year'])