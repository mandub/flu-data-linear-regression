# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 23:13:59 2019

@author: vanna
"""

import sys,os
#path = r'C:\Users\vanna\Desktop\MAT567'
#sys.path.insert(0,path)
#if path not in sys.path:
#    sys.path.append(path) #add the path
#path = r'C:\Users\vanna\Desktop\MAT567\data567\initial_flu.csv'


path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\initial_flu.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\Users\willi\Desktop\flu projrct\flu-data-linear-regression\initial_flu.csv"



pathlist = [path1, path2, path3, path4]
names = ["Anna", "Mandub", "Jake", "Bill"]
for paths in range(len(pathlist)):
    try:
        with open(pathlist[paths]) as f:#, encoding = "utf-8"
            print ("This is", names[paths])   
            path = pathlist[paths]
            break
    except:
        print("This is not", names[paths])



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
            #print(countyDict['SB']['year'])
countyDict['CS']['rate']
            
            
            
            
            
            
            
            