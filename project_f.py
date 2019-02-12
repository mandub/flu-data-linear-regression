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
    
#-----------------------------------------Function to plot observations vs predictions----------------------------        
import matplotlib.pyplot as plt
import numpy as np

def Plot_ObsVsPred(County,Year,nplots):
    
    #Initialize a matrix to store predictions
    predictions = np.zeros((52,10))
    #Get observed rates
    y = CountyRateDict[County][Year]
    #Create a list of weeks
    x = [i for i in range(1,len(y)+1)]
    #use an input of 1 as nplots to get a single plot with all ten lines, use any other input to get ten
    #separate plots.
    if nplots == 1:
        for i in range(0,10):
            #Populates the prediction matrix with test values, change the assignment to extract predictions
            #predictions[:,i] = PredictionDictionary[County][year]  For example
            predictions[:,i] = np.repeat(i/20000,len(y))
            plt.plot(predictions[:,i], label = str(i+1)+" weeks")    
        plt.plot(x, y, color = "black", linewidth = 2.0, label = "Observed Rates")
        plt.legend(loc = "upper right")
        plt.show()
    else:
        for i in range(0,10):
            #Populates the prediction matrix with test values, change the assignment to extract predictions
            #predictions[:,i] = PredictionDictionary[County][year]  For example            
            predictions[:,i] = np.repeat(i/20000,len(y))
            plt.plot(x, predictions[:,i], label = str(i+1)+" weeks")
            plt.plot(x, y, color = "black", linewidth = 2.0, label = "Observed Rates")
            plt.legend(loc = "upper right")
            plt.show()        
            
###################################################################################################################            
#----------------------Function to calculate weighted average of surrounding county rates -------------------------           
###################################################################################################################

#Build Adjacent County Dictionary, required to calculate weighted average
def countyDictBuild():
    countyList=CountyListBuild()
    countyDict={}
    countyDict=dict.fromkeys(countyList)
    countyDict['BE']=['RA','SB','MA','CMHD']
    countyDict['BH']=['YE','TR','CA','RS','PR']
    countyDict['BL']=['HI','PH']
    countyDict['BR']=['LC','JE','GA','ME']
    countyDict['CA']=['PA','YE','BH']
    countyDict['CS']=['TE','LC','ME','CMHD']
    countyDict['CMHD']=['YE','RS','GF','PH','BL','CS','ME','SG']
    countyDict['FA']=['WI','PR','CS']
    countyDict['FL']=['LI','SA','LA','MS','PW','LC','TE','PO','GL']
    countyDict['GA']=['MA','JE','BR','ME','PA']
    countyDict['GF']=['RO','PH','VA','MC','CMHD']
    countyDict['GL']=['FL','PO','TO']
    countyDict['HI']=['LI','CMHD','BL']
    countyDict['JE']=['MA','SB','CMHD','PW','LC','BR','GA']
    countyDict['LA']=['MS','SA','FL','PW']
    countyDict['LC']=['FL','TE','CS','ME','BR','JE','PW']
    countyDict['LI']=['TO','PO','CMHD','HI']
    countyDict['LN']=['FL','SA']
    countyDict['MA']=['BE','SB','JE','GA']
    countyDict['MC']=['GF','VA','RO','RI','CMHD',]
    countyDict['ME']=['LC','CS','SG','PA','GA','BR']
    countyDict['MI']=['SA','MS']
    countyDict['MS']=['MI','SA','LA','FL','PW','RA']
    countyDict['PA']=['GA','ME','SG','CA']
    countyDict['PH']=['BL','GF','VA']
    countyDict['PO']=['GL','FL','TE','CMHD','LI','TO']
    countyDict['PR']=['BH','RS','CMHD',]
    countyDict['PW']=['CMHD','MS','FL','LC','JE']
    countyDict['RA']=['MS','CMHD','BE']
    countyDict['RI']=['RO','MC','CMHD','WI']
    countyDict['RO']=['SH','CMHD','VA','MC','RI']
    countyDict['RS']=['GF','TR','BH','PR','CMHD']
    countyDict['SA']=['LN','FL','LA','MS','MI']
    countyDict['SH']=['CMHD','RO']
    countyDict['SB']=['JE','CMHD','BE','MA']
    countyDict['SG']=['PA']
    countyDict['TE']=['PO','CMHD','CS','LC','FL']
    countyDict['TO']=['GL','PO','LI']
    countyDict['TR']=['RS','BH','YE']
    countyDict['VA']=['PH','GF','MC','RO','CMHD']
    countyDict['WI']=['RI','CMHD','FA']
    countyDict['YE']=['CA','TR','BH']
    return countyDict            

#-----------------------------------------------Weighted Average Function---------------------------------------------------
#This function takes a county name (two letter code) and a year (1 through 9) and returns an array containing the
#weighted average of the rates in adjacent counties for all weeks in the given year. 
#This function uses information from CountyRateDict and CountyPopDict.
def AdjCounties_WtAverage(name,year):
    
    AdjCounties = countyDict[name] #Extract a list of adjacent counties
    matrix = np.zeros((len(CountyRateDict[name][year-1]),len(AdjCounties))) #Initialize a matrix to store weighted rates
    total = sum(CountyPopDict[county][year-1][0] for county in AdjCounties) #Calculate total adjacent population (sum of adjacent counties)
    
    #Extract rates and weight them
    i = 0 #Counter to iterate through columns of the matrix
    for county in AdjCounties:
        pop = CountyPopDict[county][year-1][0] #Get the population of a given county
        #weight = some function of population
        #The weighting function can be easily altered
        weight = pop/total
        weightedList = weight*np.array(CountyRateDict[county][year-1]) #Apply weights
        matrix[ : , i] = weightedList #Add weighted rates to the next column in the matrix
        i += 1
        
    #Sum across rows and divide by the number of adjacent counties to get an average
    weightedAverage = sum(matrix[ : , i] for i in range(0,len(AdjCounties)))/len(AdjCounties)
    return weightedAverage

#This line produces an array of weighted average rates in counties adjacent to Missoula County for year 1
AdjCounties_WtAverage('MS',1)            
            
