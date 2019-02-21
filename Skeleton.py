

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
# production dictionary
###################################

productionDict = defaultdict(list)

for county in counties:                # fill productionDict with empty list for ecah county 
    productionDict[county] =[]

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



def productionFun2(CountyRate):
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
            
#productionDict["SB"]= productionFun(CountyRateDict["SB"])
for county in counties:
    productionDict[county]= productionFun2(CountyRateDict[county])
"""
for indexyear, year in enumerate (productionDict["SB"]):
    print len(year)
    print ("-------------------------------------------")
    for indexweek, week in enumerate (year):
        print (week,CountyRateDict["SB"][indexyear][indexweek])
""" 
#%%   
###################################
# plot line regulation 
###################################
def plot1(County,Year):
    Year= Year -1
    y = range(len (CountyRateDict[County][Year]))
    x = CountyRateDict[County][Year]
    z = productionDict[County][Year]
    actualNames[counties.index(County)]
    Title= actualNames[counties.index(County)] +" Year " +str (Year +1)
    plt.title(Title)
    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")
    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()
plot1("SB",1)


    
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



def makeCountyDict(counties,CountyRateDict,CountyCDict,CountyPopDict):
    # inputs counties as list and CountyRateDict for rate , CountyCDict for count ,CountyPopDict for pop
    # output  countyDict for use it in kmean and winter functions
    # Example  countyDict['BE'][1]['rate'] = [ from county BE return list of weeks for rate in year 1 ]
    countyDict = defaultdict(list)
    for county in counties:
        countyDict[county]={1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{}}
    for county in counties:
        for index in range(9):
            countyDict[county][index+1]=  {'rate' :CountyRateDict[county][index],
                                            'count':CountyCDict[county][index],
                                            'pop'  :CountyPopDict[county][index]
                                           }
                                
    for i in countyDict['BE'][3]['pop']:
        print (i)
    return countyDict
# to use countyDict
# countyDict[county][year][ 'rate' OR count' OR 'pop'] return list of weeks
countyDict = makeCountyDict(counties,CountyRateDict,CountyCDict,CountyPopDict)

#%%   





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
###################################
# apply another algorithm 
###################################






"""
#path = r"C:\Users\Bill Griffin\flu-data-linear-regression"  
###################################
# write the production to files
###################################
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
            
            output_writer.writerow([County, N, float(yhat), yObserved, delta])
            
                                            # send to console as well           
         
            print("Writing to file")
            print( '\r' + County," Week = ", N, "yhat=", yhat,"y=", yObserved, 'delta = ', delta, end='') 
                 
                                            # increment N, n
            N += 1
            n += 1

 """      
#%%








     







