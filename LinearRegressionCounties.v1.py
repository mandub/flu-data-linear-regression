

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
 #   print (i)
#%%   
###################################
# Apply line regulation and create
# production dictionary
###################################
productionDict = defaultdict(list)
# def function(County , number of weeks , index of staring weak , list of nibers)
# return list of preductions

# def function to writ to preductions files 


#============================================================Edn mandub code
#%%   
###################################
# write the production to files
###################################


#_____________________________________________________________
#Create the model

#Choose N, the week we are predicting
#from the data create the vector y and matrix X
#X is a N-1 by 1 vector of vectors xi  
#where xi refers to the vector [1,xi,xi-1,x-2,...x0,0,0,0] 
#xi is a 1xN-1 vector
#
#CountyRateDict1={}
#for county in CountyRateDict.keys():
#    CountyRateDict1[county]=[]
#    for year in range(len(CountyRateDict[county])):
#        CountyRateDict1[county].extend(CountyRateDict[county][year])
#
#
#
#Define your variables
N=440                  #week number to predict
n = 433                 #number of observations N-6
PredRates = 6          #number of rates used as predictors

#
#
##Interactive Defining of variables
#County = input("Which County would you like to predict?\n")
#if County.upper() in CountyRateDict.keys():
#    print("Predicting for ", County.upper())
#else:
#    print("Invalid entry. Please try again")
#    County = input("Which County would you like to predict?\n")
#County = County.upper()
#
#N = int(input("Enter the week you want to predict (integer between 6 and 440):\n"))
#if 6 <= N <= 440:
#    print("N=", N)
#else:
#    print("Invalid. Please try again")
#    N = int(input("Enter the week you want to predict (integer between 6 and 440):\n"))
#
#n = int(input("How many obsetvations would you like to use? (integer less than or equal to N-6):\n"))
#if n <= N-6:
#    print("n=", n)
#else:
#    print("Invalid entry, please try again")
#    n = int(input("How many obsetvations would you like to use? (integer less than or equal to N-6):\n"))
#
#
#PredRates = int(input("How many weeks would you like to use as predictors? (integer between 3 and 10):\n"))
#if 3<= PredRates <= 10:
#    print("Number of pridictor rates =", PredRates)
#else:
#    print("Invalid entry, please try again")
#    PredRates = int(input("How many weeks would you like to use as predictors? (integer between 3 and 10):\n"))

PredictorOther = 0     #number of other predictors
q = 1+PredRates+PredictorOther        #number of predictor variables + 1 for augmentation







#formula for data
#y=week N-1-n to week N-1

#xi=week N-2-n to week N-2
def trainingMatricies(N,n,q,PredRates,data):
    #INPUT: n-number of observations, q, number of predictors, PredRates- number of rates from previous weeks data
    #OUTPUT: A-the matrix (X*X.T), z-The matrix X*y, y-the vector of target values
    #
    A = np.zeros(shape = (q,q))     #Initialize X the predictor matrix
    z = np.zeros(shape = (q,1))     #Initialize vector z
    
    startWeek = N-1-n     #for  y, for x startWeek - 5
    stopWeek = N-1        #for  y, for x stopWeek - 5
    y = np.matrix(data[startWeek:stopWeek]).T               #empty list to hold the observed target rates
        
    for i in range(n):
        yi= np.matrix(y[i])        #store yi as a matrix for matrix multiplication
        x1 = [1]                   #Augment the matrix so the 1st column is 1's to predict B0
        x2 = data[(startWeek-(PredRates+1)+i):(startWeek-1+i)]  #rates from the 5 weeks preceding yi
        x2.reverse()               #reverse the order so most recent is first
        x1.extend(x2)              #add the rates to the list x1
        x= np.matrix(x1).T         #create the 1xn matrix x
        A += x*(x.T)               #create A sum of xi*xi.T
        z += x*yi                  #create z sum of xi*yi

    return A,z,y                 #Returns the predictor matrix and the target matrix  
 
rates=CountyRateDict1[County]
ratesRange=list(range(len(rates)))
ratesDict = dict(zip(ratesRange,rates))

def MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1):
    A,z,y = trainingMatricies(N,n,q,PredRates, rates)
    betahat = np.linalg.solve(A,z)    #solve for Beta Hat   B=A.inverse*z
    betahat=np.matrix(betahat)
    xpredictors=CountyRateDict1[County][N-PredRates-1:N-1]
    xpredictors.insert(0,1)
    xpredictors=np.matrix(xpredictors)
    yhat= xpredictors*betahat
    yObserved = ratesDict[N-1]
    delta =yhat - yObserved
    
    return yhat,yObserved,delta,betahat

yhat,yObserved, delta, betahat=MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1)
print("\n")
print("yhat=", yhat,"y=", yObserved, 'delta = ', delta) 
              
print("betahat =", betahat)        

       







