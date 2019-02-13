

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:54:26 2019

@author: annag

Linear Regression Model v2
"""
import matplotlib.pyplot as plt
import numpy as np

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
                

#%%   
###################################
# Apply line regulation and create
# prediction dictionary
###################################

predictionDict = defaultdict(list)

for county in counties:                # fill predictionDict with empty list for ecah county 
    predictionDict[county] =[]

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

def sklearn_linear_Regression(weeksRateslist):
    Y_hat=np.array(weeksRateslist[-1])
    del weeksRateslist[-1]
    X_hat=np.array([weeksRateslist[-1]])
    x_hat= weeksRateslist[-1]
    del weeksRateslist[-1]
    X = np.array(weeksRateslist)
    del weeksRateslist[0]
    weeksRateslist.append(x_hat)
    Y= np.array(weeksRateslist)
    # Create linear regression object
    regr = linear_model.LinearRegression()
    regr.fit(X.reshape(-1, 1), Y)
    y_pred = regr.predict(X_hat.reshape(1, -1))    
    return y_pred[0]
 
def linearRegression2(weeksRateslist):
    if len (weeksRateslist) ==1:
        return weeksRateslist[0]
    elif len (weeksRateslist) == 2:
        return weeksRateslist[1]
    elif len (weeksRateslist) == 3:
        return weeksRateslist[2]
    else:
        y_pred = sklearn_linear_Regression(weeksRateslist)
    return y_pred



def predictionFun2(CountyRate):
    alist2D = []
    
    for yearIndex,year in enumerate (CountyRate):
        weeks_up_today=[]
        alist2D.append([])
        for weekIndex,week in enumerate(year):
            alist2D[yearIndex].append([])   #make space for a week
            weeks_up_today.append(week)
            aWeekPrediction = linearRegression2(weeks_up_today)
            alist2D[yearIndex][weekIndex]=aWeekPrediction
    return alist2D
            
#predictionDict["SB"]= predictionFun(CountyRateDict["SB"])
for county in counties:
    predictionDict[county]= predictionFun2(CountyRateDict[county])
"""
for indexyear, year in enumerate (predictionDict["SB"]):
    print len(year)
    print ("-------------------------------------------")
    for indexweek, week in enumerate (year):
        print (week,CountyRateDict["SB"][indexyear][indexweek])
""" 
def plot1(County,Year):
    Year= Year -1
    y = range(len (CountyRateDict[County][Year]))
    x = CountyRateDict[County][Year]
    z = predictionDict[County][Year]
    actualNames[counties.index(County)]
    Title= actualNames[counties.index(County)] +" Year " +str (Year +1)
    plt.title(Title)
    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")
    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()
plot1("SB",1)
plot1("SB",2)
plot1("SB",3)
plot1("SB",4)
plot1("SB",5)
plot1("SB",6)
plot1("SB",7)
plot1("SB",8)

    
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
#Plot_ObsVsPred("SB",1,1)       
# def function(County , number of weeks , index of staring weak , list of nibers)
# return list of preductions





#%%   

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






"""
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

"""





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



def MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1):
    rates=CountyRateDict1[County]       
    ratesRange=list(range(len(rates)))
    ratesDict = dict(zip(ratesRange,rates))
    A,z,y = trainingMatricies(N,n,q,PredRates, rates)
    betahat = np.linalg.solve(A,z)    #solve for Beta Hat   B=A.inverse*z
    betahat=np.matrix(betahat)
    xpredictors=rates[N-PredRates-1:N-1] #xpredictors=CountyRateDict1[County][N-PredRates-1:N-1]
    xpredictors.insert(0,1)
    xpredictors=np.matrix(xpredictors)
    yhat= xpredictors*betahat
    yObserved = ratesDict[N-1]
    delta =yObserved - yhat
    
    return yhat,yObserved,delta,betahat


#for county in counties:
#Define your variables
N=440                  #week number to predict
n = 433                 #number of observations N-6
PredRates = 6          #number of rates used as predictors

PredictorOther = 0     #number of other predictors
q = 1+PredRates+PredictorOther        #number of predictor variables + 1 for augmentation
County='CS' 
rates=CountyRateDict1[County]
ratesRange=list(range(len(rates)))
ratesDict = dict(zip(ratesRange,rates))

#yhat,yObserved, delta, betahat=MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1)
#"""
#newlist=[]
#for County in counties:
#    
#    try :
#        for N in range (10,len (CountyRateDict1[County])-1):
#            PredRates = 6
#            n = N-PredRates 
#            yhat,yObserved, delta, betahat=MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1)
#            #print (yhat.item(0),yObserved )
#        newlist.append(County)
#        print (County, 'OK')
#    except:
#        print(County, "has problems")
#"""      
#"""
#for county in counties:
#    print (county)
#    for year in CountyRateDict[county]:
#        print (len (year))
#        N = 45
#        PredRates = 6
#        n = N-PredRates
#        rates=year
#        PredictorOther = 0
#        q = 1+PredRates+PredictorOther
#        yhat,yObserved, delta, betahat=MatrixSolve(N,n,q,PredRates,rates)
#        print (yhat,yObserved)
#        
#        
#
## =============================================================================
## print("\n")
## print(County)
## 
## print("yhat=", yhat,"y=", yObserved, 'delta = ', delta) 
##               
## print("betahat =", betahat)    
## 
## =============================================================================
#
#
#
#
########################
## Main Program Sequence
########################
#
#        
######################## Initial conditions
##        
#weekRequest = 366                           # enter the starting week here
##                                            # This is year 8 week 1
##
##  
##                                            # N is what we pass, so change program run above     
#N = weekRequest                             #
##                                            # Change as required this will change all other computations
##
##                                            # since we decided on 6 predictor variables we will use
#n = N - PredRates                                   # every week in the set, up to the predict week
##                                            # to compute Betas
##
##PredRates = 5                               # as above. Executive decision, change as req'd
##
##PredictorOther = 0                          # Leaving this in just in case we develop this model with other preds
##
##q = 1 + PredRates + PredictorOther          # just as it was before
##                                            
#
##path = r"C:\Users\Bill Griffin\flu-data-linear-regression"  
####################################
## write the prediction to files
####################################
#pathprint = path.strip("initial_flue.csv") +  "\County Flu Forecasts Weeks " + str(N) + " to 441.csv"
#
#                                            # change this path as applicable
#                                                                                   
####################### Iterate through counties, weeks, build .csv file ... output to console for S&G's
#
#
#with open(pathprint, mode = 'w') as output_file:
#    
#    output_writer = csv.writer(output_file, dialect = 'excel')
#    
#    for County in counties:
#        
#        N = weekRequest                     # start each county at the week requested
#        n = N - PredRates
#    
#        while N < 442:                      # we want the last yhat to be week 441, which is last year we
#                                            # have a y
#                                                
#            rates=CountyRateDict1[County]   # load in the rate column for interated county
#            
#                                            # Execute functions -- Solve lineq
#            yhat,yObserved, delta, betahat = MatrixSolve(N,n,q,PredRates,rates,County,CountyRateDict1)
#            
#            output_writer.writerow([County, N, float(yhat), yObserved, delta])
#            
#                                            # send to console as well           
#         
#            print("Writing to file")
#            print( '\r' + County," Week = ", N, "yhat=", yhat,"y=", yObserved, 'delta = ', delta, end='') 
#                 
#                                            # increment N, n
#            N += 1
#            n += 1
#
# """
#






     







