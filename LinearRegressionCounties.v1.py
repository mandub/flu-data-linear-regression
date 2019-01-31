# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:54:26 2019

@author: annag

Linear Regression Model v2
"""

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



        
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
#################################################
# read from the file and create Data dictionaries
#################################################
#============================================================ Mandub code 
CountyDict = defaultdict(list)
yeardata=defaultdict(list)

CountyRateDict = defaultdict(list)  # Rate
CountyCDict = defaultdict(list)     # C
CountyPopDict = defaultdict(list)   #population
actualNames=[]         # hold the actual county Names for presentation purpose
countyLicenceNumber=[] # hold the actual county Licence Number for presentation purpose
counties=[]              # hold county Shortcut names
countyIndexes=defaultdict(list)       # hold 3 name and indexes for each county 
                                        # first will be for the rate 
                                        # the second will be for C
                                        # the third will be for population
counter = 1     # number of line in the file 
with open(path) as f:
    for line in f:
        if counter == 1: # read the first line in the file
            actualNames = line.split(",")
            actualNames = actualNames[3:] # remove the first 3 elements in the list
            actualNames[-1] = actualNames[-1].rstrip('\n') # remove newline char from last element
            counter +=1
            # need to clean redundant data
            
        elif counter == 2: #read the second line in the file
            countyLicenceNumber= line.split(",")
            countyLicenceNumber    = countyLicenceNumber[3:] # remove the first 3 elements in the list
            countyLicenceNumber[-1] = countyLicenceNumber[-1].rstrip('\n') # remove newline char from last element
            counter +=1
            # need to clean redundant data and convert  to int
            
        elif counter == 3: #read the third line in the file
            counter +=1
            counties = line.split(",")
            counties[-1] = counties[-1].rstrip('\n') # remove newline char from last element
            temp = counties                 # hold the line structure to use the indexes
            counties = counties[3:]
            
            counties2 = []                  # to remove redundant data  
            for county in counties:
                if county not in counties2:
                    counties2.append(county)
            counties = counties2
            
             
            for county in counties:        # add counties indexes to countyIndexes
                indexes= []                    #hold indexes for only one county
# =============================================================================
                CountyRateDict[county]= [] # ...we fill CountyRateDict by counties with empty list for the years
                                           # ....where index zreo will be year 1
                CountyCDict[county]=[]     # ...we fill CountyCDict by counties with empty list for the years
                CountyPopDict[county]= []  # ...we fill CountyPopDict by counties with empty list for the years
# =============================================================================
                for index,value in enumerate (temp):  # if the same county append the index 
                    if county == value:
                        indexes.append(index)
                countyIndexes[county]=indexes 
                
        
        elif counter == 4:               #read the third line in the file
            counter+=1                   # we do not do any thing because this line is headers line     
        else:                            # read the others lines in the file for Data 
            data =line.split(",")
            year = int (data[1]) -1      # to use year as index for Dicts
            weak = int (data[2]) -1      # to use weak as index ofr Dicts

            if weak == 0 :                #newyear start
                for county in CountyRateDict:
                    CountyRateDict[county].append([])   # add new list for the weaks
                    CountyCDict[county].append([])
                    CountyPopDict[county].append([])
                    
                    rateIndex= countyIndexes[county][0] #take the index of rate
                    rate = float (data[rateIndex])
                    
                    CIndex= countyIndexes[county][1] #take the index of C
                    C = int (data[CIndex])
                    
                    popIndex= countyIndexes[county][2] #take the index of population
                    pop = int (data[popIndex])
                    
                    CountyRateDict[county][year].append(rate)
                    CountyCDict[county][year].append(C)
                    CountyPopDict[county][year].append(pop)
                    #repat for othre dict
            else:
                for county in CountyRateDict:
                    rateIndex= countyIndexes[county][0] #take the index of rate
                    rate = float (data[rateIndex])

                    CIndex= countyIndexes[county][1] #take the index of C
                    C = int (data[CIndex])
                    
                    popIndex= countyIndexes[county][2] #take the index of population
                    pop = int (data[popIndex])
                    
                    CountyRateDict[county][year].append(rate)
                    CountyCDict[county][year].append(C)
                    CountyPopDict[county][year].append(pop)
                
# testing            
#for i in  CountyPopDict["SB"]:
#    print (i)
#%%   
###################################
# Apply line regulation and create
# production dictionary
###################################
productionDict = defaultdict(list)

for county in counties:                # fill productionDict with empty list for ecah county 
    productionDict[county] =[]

def productionFun(CountyRate,numberOfWeaks):
    for year in CountyRate:
        for weak in year:
            print (weak)
    return None
Numweak= 10
WeaksList= []
for i in range (1,Numweak+1):
    WeaksList.append(i)
    
for numberOfWeak in WeaksList:
    #productionDict["SB"].append(numberOfWeak)
    productionDict["SB"]= productionFun(CountyRateDict["SB"],numberOfWeak)
    
# def function(County , number of weeks , index of staring weak , list of nibers)
# return list of preductions

# def function to writ to preductions files 


#============================================================Edn mandub code
#%%   
###################################
# write the production to files
###################################

countyList=['SB']
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
countyDict['SB']['rate']


#_____________________________________________________________
#Create the model

#Choose N, the week we are predicting
#from the data create the vector y and matrix X
#X is a N-1 by 1 vector of vectors xi  
#where xi refers to the vector [1,xi,xi-1,x-2,...x0,0,0,0] 
#xi is a 1xN-1 vector

rates = countyDict['SB']['rate']

#Define your variables
N=440                  #week number to predict
PredRates = 5          #number of rates used as predictors
PredictorOther = 0     #number of other predictors
n = 433                 #number of observations
q = 1+PredRates+PredictorOther        #number of predictor variables + 1 for augmentation

#formula for data
#y=week N-1-n to week N-1

#xi=week N-2-n to week N-2

def trainingMatricies(n,q,PredRates, rates):
    #Creates y a vector of our target variables. Creates vector z = (X.T)y
    #Creates A a matrix (X.T)X where X represents a matrix of predictor variables using vector xi is to predict yi.
    #xi is the vector of the previous weeks rates for the county of interest, and yi is the current weeks observed rate
    A = np.zeros(shape = (q,q))     #Initialize X the predictor matrix
    z = np.zeros(shape = (q,1))     #Initialize vector z
    
    startWeek = N-1-n     #for  y, for x startWeek - 5
    stopWeek = N-1        #for  y, for x stopWeek - 5
    y = np.matrix(rates[startWeek:stopWeek]).T               #empty list to hold the observed target rates
        
    for i in range(n):
        yi= np.matrix(y[i])        #store yi as a matrix for matrix multiplication
        x1 = [1]                   #Augment the matrix so the 1st column is 1's to predict B0
        x2 = rates[(startWeek-(PredRates+1)+i):(startWeek-1+i)]  #rates from the 5 weeks preceding yi
        x2.reverse()               #reverse the order so most recent is first
        x1.extend(x2)              #add the rates to the list x1
        x= np.matrix(x1).T         #create the 1xn matrix x
        A += x*(x.T)               #create A sum of xi*xi.T
        z += x*yi                  #create z sum of xi*yi

    return A,z,y                 #Returns the predictor matrix and the target matrix  
    
A,z,Y = trainingMatricies(n,q,PredRates, rates)
betahat = np.linalg.solve(A,z)    #solve for Beta Hat   B=A.inverse*z
betahat=np.matrix(betahat)
xpredictors=countyDict['SB']['rate'][N-PredRates-1:N-1]
xpredictors.insert(0,1)
xpredictors=np.matrix(xpredictors)
    
yhat= xpredictors*betahat
print("yhat=", yhat)               
        







