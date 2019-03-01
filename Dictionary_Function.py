# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 08:29:36 2019

@author: vanna
"""

#%%Testing Function
import sys
path = r'C:\Users\vanna\Desktop\MAT567'
sys.path.insert(0,path)
if path not in sys.path:
    sys.path.append(path) #add the path
path = r'C:\Users\vanna\Desktop\MAT567\data567\initial_flu.csv'
#convert all data strings to floating point numbers
def convertData(dataString):
    #INPUT: data line staring from 5th row in string form
    #OUTPUT: data in floating points
    for i in range(len(dataString)):
        dataString[i]=float(dataString[i])
    return dataString
years=[1,2,3,4,5,6,7,8,9]
def countyData(county):
    #INPUT: county
    #OUTPUT: year, rate, pop, count
    for record in f:   #goes through every row
        dataString = record.split(",") #split data
        data=convertData(dataString)   #convert all data rows to floating points
        for county in countyDict:
            for string in lineString:  #goes through the 4th line(row)
                if string==county+' '+'rate':
                    position_rate=lineString.index(string)
                if string==county+' '+'count':
                    position_count=lineString.index(string)
                    for year in years:
                        if data[1]==year:
                            rate=data[position_rate]       #position of county's rate
                            countyDict[county][year]['rate'].append(rate)
                            count=data[position_count]     #position of county's counts
                            countyDict[county][year]['count'].append(count)
    return countyDict[county]
countyList=['BE','BH','BL','BR','CA','CS','CMHD','FA','FL','GA','GF','GL','HI',
          'JE','LA','LC','LI','LN','MA','MC','ME','MI','MS','PA','PH','PO','PR','PW',
          'RA','RI','RO','RS','SA','SH','SB','SG','TE','TO','TR','VA','WI','YE']
countyDict={}
for county in countyList:
    countyDict.update({county:{}})
    for year in years:
        countyDict[county].update({year:{'rate':[],'count':[]}})
with open(path) as f:
    next(f)
    next(f)
    next(f)
    line=f.readline()  #Read the 4th line(row)
    lineString=line.split(",")  #split the 4th line(row)
    countyDict[county]=countyData(county)

