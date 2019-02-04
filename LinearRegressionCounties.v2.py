

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:54:26 2019

@author: annag

Linear Regression Model v2
"""

path1 = r"C:\Users\annag\Documents\2018-2019\Spring_2019\BigDataProjects\flu-data-linear-regression\initial_flu.csv"
path2 = "/home/mandub/Desktop/6th semester/courses/Data Science Projects/data flu/flu-data-linear-regression/initial_flu.csv"
path3 = r"C:\Users\jakeo\OneDrive\Documents\M467\flu-data-linear-regression\initial_flu.csv"
path4 = r"C:\Users\Bill Griffin\flu-data-linear-regression\initial_flu.csv"



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
import csv

#%%

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

for county in counties:                # fill productionDict with empty list for ecah county 
    productionDict[county] =[]
    
def linearRegression(weeksRateslist):
    aWeekPredictionList =[]
    if len (weeksRateslist) ==1:
        aWeekPredictionList.append(weeksRateslist[0])
        return aWeekPredictionList
    for Rates in weeksRateslist:
        print (Rates)
        

    return aWeekPredictionList
def productionFun(CountyRate):
    alist3D = []
    for yearIndex,year in enumerate (CountyRate):
        alist3D.append([])               # make space for a year
        ## chunks the year to lists of number 10
        alist =year
        temps=[]
        num =10
        for index,i in enumerate (alist):
            L =[]
            t=index
            if index ==0:
                L.append(alist[t])
                temps.append(L)
            elif index < num :
                while (t!=0):
                    L.append(alist[t])
                    t -=1
                L.reverse()
                temps.append(L)
            else :
                while (t!=index - num):
                    L.append(alist[t])
                    t -=1
                L.reverse()
                temps.append(L)
                
        for weekIndex,week in enumerate(year):
            alist3D[yearIndex].append([])   #make space for a week
            aWeekPredictionList = []
            #NumberOfobservations= len(temps[weekIndex])      # use observations from 1 up to 10
            weeksRateslist= temps[weekIndex]                 # hold 10 previous weeks or less
            
            aWeekPredictionList = linearRegression(weeksRateslist)
            alist3D[yearIndex][weekIndex].append(aWeekPredictionList) # Add a week prediction list to that week
            
    return alist3D  # return 3D object of one county [year][week][predictionlist]

productionDict["SB"]= productionFun(CountyRateDict["SB"])

# def function(County , number of weeks , index of staring weak , list of nibers)
# return list of preductions




#============================================================Edn mandub code
#%%   
###################################
# write the production to files
###################################
# def function to writ to preductions files 

#_____________________________________________________________
#Create the model

#Choose N, the week we are predicting
#from the data create the vector y and matrix X
#X is a N-1 by 1 vector of vectors xi  
#where xi refers to the vector [1,xi,xi-1,x-2,...x0,0,0,0] 
#xi is a 1xN-1 vector


CountyRateDict1={}
for county in CountyRateDict.keys():
    CountyRateDict1[county]=[]
    for year in range(len(CountyRateDict[county])):
        CountyRateDict1[county].extend(CountyRateDict[county][year])



#Define your variables
N=440                  #week number to predict
n = 433                 #number of observations N-6
PredRates = 6          #number of rates used as predictors



#Interactive Defining of variables
County = input("Which County would you like to predict?\n")
if County.upper() in CountyRateDict.keys():
    print("Predicting for ", County.upper())
else:
    print("Invalid entry. Please try again")
    County = input("Which County would you like to predict?\n")
County = County.upper()

PredRates = int(input("How many weeks would you like to use as predictors? (integer between 3 and 10):\n"))
if 3<= PredRates <= 10:
    print("Number of pridictor rates =", PredRates)
else:
    print("Invalid entry, please try again")
    PredRates = int(input("How many weeks would you like to use as predictors? (integer between 3 and 10):\n"))
    
    
N = int(input("Enter the week you want to predict (integer between number of predictors and 441):\n"))
if PredRates <= N <= 441:
    print("N=", N)
else:
    print("Invalid. Please try again")
    N = int(input("Enter the week you want to predict (integer between number of predictors and 441):\n"))

n = int(input("How many obsetvations would you like to use? (integer less than or equal to N-number of predictors):\n"))
if n <= N-PredRates:
    print("n=", n)
else:
    print("Invalid entry, please try again")
    n = int(input("How many obsetvations would you like to use? (integer less than or equal to N-number of predictors):\n"))




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
    rates=CountyRateDict1[County]
    ratesRange=list(range(len(rates)))
    ratesDict = dict(zip(ratesRange,rates))
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
print(County)

print("yhat=", yhat,"y=", yObserved, 'delta = ', delta) 
              
print("betahat =", betahat)    





#######################
# Main Program Sequence
#######################

        
####################### Initial conditions
#        
weekRequest = 366                           # enter the starting week here
#                                            # This is year 8 week 1
#
#  
#                                            # N is what we pass, so change program run above     
N = weekRequest                             #
#                                            # Change as required this will change all other computations
#
#                                            # since we decided on 6 predictor variables we will use
n = N - PredRates                                   # every week in the set, up to the predict week
#                                            # to compute Betas
#
#PredRates = 5                               # as above. Executive decision, change as req'd
#
#PredictorOther = 0                          # Leaving this in just in case we develop this model with other preds
#
#q = 1 + PredRates + PredictorOther          # just as it was before
#                                            
#path = r"C:\Users\Bill Griffin\flu-data-linear-regression"  
pathprint = path.strip("initial_flue.csv") +  "\County Flu Forecasts Weeks " + str(N) + " to 441.csv"

                                            # change this path as applicable
                                                                                   
###################### Iterate through counties, weeks, build .csv file ... output to console for S&G's


with open(pathprint, mode = 'w') as output_file:
    
    output_writer = csv.writer(output_file, dialect = 'excel')
    
    for County in counties:
        
        N = weekRequest                     # start each county at the week requested
        n = N - PredRates
    
        while N < 442:                      # we want the last yhat to be week 441, which is last year we
                                            # have a y
                                                
            rates=CountyRateDict1[County]   # load in the rate column for interated county
            
                                            # Execute functions -- Solve lineq
            yhat,yObserved, delta, betahat = MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1)
            
            output_writer.writerow([County, N, yhat, yObserved, delta])
            
                                            # send to console as well           
         
            print("Writing to file")
            print( '\r' + County," Week = ", N, "yhat=", yhat,"y=", yObserved, 'delta = ', delta, end='') 
                 
                                            # increment N, n
            N += 1
            n += 1

       
#%%








     







