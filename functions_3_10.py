# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:41:27 2019

@author: annag
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 12:42:19 2019
@author: Cassidy
"""

import numpy as np
import matplotlib.pyplot as plt

 

def pathfinder(pathlist):
    #Input: list of paths
    #Output: correct path for user
    #
    names = ["Anna", "Mandub", "Jake", "Bill", "Cassidy"]
    for paths in range(len(pathlist)):
        try:
            with open(pathlist[paths]):#, encoding = "utf-8"
                print ("This is", names[paths])   
                path = pathlist[paths]
                break
        except:
            print("This is not", names[paths])
    return(path)


###############################################################################
#READING IN THE FILE
###############################################################################


def convertData(dataString):
    #Input: string of data
    #Output: float of data
    #
    for i in range(len(dataString)):
        dataString[i]=float(dataString[i])
    return dataString




def readData(countyList, years, countyDict, path):
    #INPUT: Initialized empty list for couties, list of years, initialized empty dictionary for counties, path
    #OUTPUT: Nested dictionary countyDict{county:{year:{'rate'=[],'pop'=[],'county'=[]}}}
    #
    with open(path) as f:
        line = f.readline()
        lineString=line.split(",")
        if lineString[6] == 'Two Char':           #use first 3rd line to make list of counties
            for string in lineString:
                if string not in countyList:
                    countyList.append(string)
            countyList = countyList[2:-1]        #get rid of etxras
            for county in countyList:            #initialized dict of dict
                countyDict[county]={}
                for year in years:
                    countyDict[county][year]={'rate':[],'count':[],'pop':[]}
            next(f)
            next(f)
            next(f)
            next(f)
        for record in f:                         #start on first line of data
            dataString = record.split(",")
            data = convertData(dataString)       #convert data to floats
            for i in range(7,59):    
                countyDict[countyList[i-7]][data[3]]['rate'].append(data[i])   #append rate data
            for i in range(59,111):
                countyDict[countyList[i-59]][data[3]]['count'].append(data[i]) #append count data
            for i in range(111,163):
                countyDict[countyList[i-111]][data[3]]['pop'].append(data[i])   #append pop data
    return countyDict, countyList

###############################################################################
# LINEAR REGRESSION
###############################################################################


def Data(countyList, years, countyDict, PredWeek, OtherPredVar, D, VoI):
    #INPUT: PredWeek-#weeks used to predict, OtherPredVar-other predictor variables used, D-empty dictionary, VoI - variable of interest)
    #OUTPUT: D- pairs (observed, pred var matrix) q- 1 + PredWeek + OtherPredVar
    #by Anna
    opvn = len(OtherPredVar)
    for county in countyList:
        D[county]={}
        for year in years:
            D[county][year]=[]
            for i in range(len(countyDict[county][year][VoI])-(PredWeek+1)):
                y = np.matrix(countyDict[county][year][VoI][i+PredWeek])
                x0 = [1]
                x1R = []
                for j in range(i,i+PredWeek):
                    x1R.append(countyDict[county][year][VoI][j])
                x1R.reverse()
                x0.extend(x1R)
                q = 1 + PredWeek + opvn 
                if opvn != 0:
                    if county != 'STATE':
                        x0.append(OtherPredVar[county][year][i+PredWeek])
                        q = 1 + PredWeek + 1
                    else:
                        x0.append(0)
                        q = 1 + PredWeek + 1                        
                X = np.matrix(x0).reshape(q,1)
                D[county][year].append((y,X))
    return D, q

def InitialTrainingMatricies( countyList, years, D, Aci, Zci, q, start):  
    #INPUT: D- pairs (observed, pred var matrix), Aci,Zci - empty Dict, start- #of weeks to initialy train Beta 
    #OUTPUT: Dictionaries Aci[county][year] = xi*xi.T, Zci[county][year] = xi*yi
    #by Anna
    for county in countyList:
        Aci[county]={}
        Zci[county]= {}
        for year in years:
            Aci[county][year]= np.zeros(shape =(q,q))
            Zci[county][year]= np.matrix(np.zeros(shape = (q,1)))        
            for i in range(0, start):
                yi = D[county][year][i][0]
                xi = D[county][year][i][1]
                Aci[county][year] += xi*xi.T
                Zci[county][year] += xi*yi
    return Aci, Zci

def NextTrainingMatricies( county, year, D, Aci, Zci, j, start): 
    #INPUT: j-week index
    #OUTPUT: updated Aci and Zci adding next xi and yi removing previous xi*xi.T and xi*yi
    #by Anna        
    yi = D[county][year][j][0]
    xi = D[county][year][j][1]
    yrem = D[county][year][j-start][0]
    xrem = D[county][year][j-start][1]    
    Aci[county][year] += xi*xi.T
    Zci[county][year] += xi*yi
    Aci[county][year] -= xrem*xrem.T
    Zci[county][year] -= xrem*yrem
    return Aci, Zci


def InitialBetaSolver(countyList, years, Aci, Zci, Bci, q):
    #INPUT: Bci- empty dictionary
    #OUTPUT: Initial Beta
    #by Anna
    for county in countyList:
        Bci[county] = {}
        for year in years:
            A = Aci[county][year]
            Z = Zci[county][year]
            try:
                b = np.linalg.solve(A,Z)
                Bci[county][year]=b
            except:
                Bci[county][year]=(np.zeros(shape = (q,1)))
                pass
    return Bci


def NextBetaSolver(county, year, Aci, Zci, Bci,q,j):
    #INPUT: j-week predicted
    #OUTPUT: Updated Bci using new Aci and Zci
    #by Anna
    A = Aci[county][year]
    Z = Zci[county][year]
    try:
        b = np.linalg.solve(A,Z)
        Bci[county][year]=b
    except:
        Bci[county][year]=(np.zeros(shape = (q,1)))
        pass
    return Bci

def createPredictionDict(countyList, years):
    #INPUT: 
    #OUTPUT:empty prediction dictionary in the format needed for team 3
    #
    predictionDict={}
    for county in countyList:
        predictionDict.update({county:{}})
        for year in years:
            predictionDict[county].update({year:{'rate':[],'count':[],'ybar':[]}})
    return predictionDict


def initialpredictionDict(countyList, years, D, Bci, q, start):
    #INPUT: D- tuple (target, Predictor variable matrix), Bci-Beta, start- # of initial pred var to train Beta
    #OUTPUT: predictionDict - prediction dictionary for first "start" y's and ybar's, ysum- sum of y's of first "start" targets, YTrue- dictionary of observed data
    #by Anna
    YTrue = {}
    predictionDict = createPredictionDict(countyList, years)
    for county in countyList:
        YTrue[county]={}
        for year in years:
            YTrue[county][year] = []
            X = np.matrix(np.zeros(shape = (start, q)))
            for j in range(start):
                X[j,] = D[county][year][j][1].T
            B = Bci[county][year]
            pred = X*B
            ysum = 0
            for j in range(start):
                if float(pred[j,]) <0:
                    pred[j,] = 0
                predictionDict[county][year]['rate'].append(float(pred[j,]))
                ysum += float(D[county][year][j][0])

                ybar = ysum/(j+1)
                predictionDict[county][year]['ybar'].append(ybar)
                YTrue[county][year].append(float(D[county][year][j][0]))
    return predictionDict, ysum, YTrue

def NextpredictionDict(county, year, D, Bci,q, predictionDict, j, YTrue, ysum):
    #INPUT: j- week being predicted, YTrue- dict of observed data to this point, ysum- sum of observations to this point
    #OUTPUT: updated predictionDict, ysum and YTrue for week j
    #by Anna
    X = np.matrix(np.zeros(shape = (1, q)))
    X = D[county][year][j][1].T
    B = Bci[county][year]
    pred = X*B
    if float(pred) <0:
        pred = 0
    predictionDict[county][year]['rate'].append(float(pred))
    ysum = predictionDict[county][year]['ybar'][j-1]*(j)
    ysum += float(D[county][year][j][0])
    ybar = ysum/(j+1)
    predictionDict[county][year]['ybar'].append(ybar)
    YTrue[county][year].append(float(D[county][year][j][0]))    
    return predictionDict, ysum, YTrue



def Linear_Regression(OtherPredVar, years, countyDict, countyList, VoI, PredWeek, start):
    #INPUT: OtherPredVar-dict of other predictor variables,VoI- variable of interest, #number of predictor variables, #of weeks used to train Beta
    #OUTPUT: predictionDict-dict of predictions by county, year  for each week, YTrue- dict of observed values by county by year, for each week
    #by Anna
    D = {}
    D, q = Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,VoI)
    Aci = {}
    Zci = {}
    Aci, Zci = InitialTrainingMatricies( countyList, years, D, Aci, Zci, q, start)
    Bci = {}
    Bci = InitialBetaSolver(countyList, years, Aci, Zci, Bci, q)
    predictionDict, ysum, YTrue = initialpredictionDict(countyList, years, D, Bci, q, start)
    for county in countyList:
        for year in years:
            for j in range(start,len(D[county][year])):
                predictionDict, ysum, YTrue = NextpredictionDict(county, year, D, Bci,q,predictionDict, j, YTrue, ysum)
                Aci, Zci = NextTrainingMatricies( county, year, D, Aci, Zci,j, start)
                Bci = NextBetaSolver(county, year, Aci, Zci, Bci, q, j)
    return predictionDict, YTrue





###############################################################################
#PLOTTING RESULTS
###############################################################################

def plot1(County,Year, YTrue, predictionDict):
    Year= Year
    x = range(len (YTrue[County][Year]))
    y = YTrue[County][Year]
    z = predictionDict[County][Year]['rate']
    yb = predictionDict[County][Year]['ybar']
    Title= County +" Year " +str (Year)
    plt.title(Title)
    plt.plot(x, yb, 'go-', linewidth = 2.0, label = "ybar")
    plt.plot(x, y, 'bo-', linewidth = 2.0, label = "Observed Rates")
    plt.plot(x, z, 'ro-', linewidth = 2.0, label = "Prediction Rates")
    plt.legend(loc = "upper right")
    plt.show()

###############################################################################
#ADJACENT COUNTY FUNCTIONS
###############################################################################

def adjcountyDictBuild(countyList):
    adjcountyDict={}
    adjcountyDict=dict.fromkeys(countyList)
    adjcountyDict['BE']=['RA','SB','MA','CMHD','DL']
    adjcountyDict['BH']=['YE','TR','CA','RS','PR']
    adjcountyDict['BL']=['HI','PH','CH']
    adjcountyDict['BR']=['LC','JE','GA','ME']
    adjcountyDict['CA']=['PA','YE','BH','ST']
    adjcountyDict['CH']=['LI','HI','BL','CMHD','CS','TE','PO']
    adjcountyDict['CS']=['TE','LC','ME','CMHD','CH']
    adjcountyDict['CR']=['PR','CU','FA'] 
    adjcountyDict['CU']=['PR','CR','FA','PI','RS','GF']
    adjcountyDict['CMHD']=['YE','RS','GF','PH','BL','CS','ME','SG','CH']
    adjcountyDict['DA']=['VA','RO','SH'] 
    adjcountyDict['DL']=['RA','GR','PW','JE','SB','BE'] 
    adjcountyDict['DW']=['WI','PI','MC','RI']    
    adjcountyDict['FA']=['WI','PR','CS','CR','CU','PI']
    adjcountyDict['FL']=['LI','SA','LA','MS','PW','LC','TE','PO','GL']
    adjcountyDict['GA']=['MA','JE','BR','ME','PA']
    adjcountyDict['GF']=['RO','PH','VA','MC','CMHD','CU','PI']
    adjcountyDict['GL']=['FL','PO','TO']
    adjcountyDict['GR']=['DL','PW','MS','RA']
    adjcountyDict['HI']=['LI','CMHD','BL','CH']
    adjcountyDict['JE']=['MA','SB','CMHD','PW','LC','BR','GA','DL']
    adjcountyDict['LA']=['MS','SA','FL','PW']
    adjcountyDict['LC']=['FL','TE','CS','ME','BR','JE','PW']
    adjcountyDict['LI']=['TO','PO','CMHD','HI','CH']
    adjcountyDict['LN']=['FL','SA']
    adjcountyDict['MA']=['BE','SB','JE','GA']
    adjcountyDict['MC']=['GF','VA','RO','RI','CMHD','PI','DW']
    adjcountyDict['ME']=['LC','CS','SG','PA','GA','BR']
    adjcountyDict['MI']=['SA','MS']
    adjcountyDict['MS']=['MI','SA','LA','FL','PW','RA','GR']
    adjcountyDict['PA']=['GA','ME','SG','CA','ST']
    adjcountyDict['PH']=['BL','GF','VA']
    adjcountyDict['PI']=['WI','GF','FA','CU','MC','DW']
    adjcountyDict['PO']=['GL','FL','TE','CMHD','LI','TO','CH']
    adjcountyDict['PR']=['BH','RS','CMHD','CR','CS']
    adjcountyDict['PW']=['CMHD','MS','FL','LC','JE','DL','GR']
    adjcountyDict['RA']=['MS','CMHD','BE','DL','GR']
    adjcountyDict['RI']=['RO','MC','CMHD','WI','DW']
    adjcountyDict['RO']=['SH','CMHD','VA','MC','RI','DA']
    adjcountyDict['RS']=['GF','TR','BH','PR','CMHD','CU']
    adjcountyDict['SA']=['LN','FL','LA','MS','MI']
    adjcountyDict['SH']=['CMHD','RO','DA']
    adjcountyDict['SB']=['JE','CMHD','BE','MA','DL']
    adjcountyDict['SG']=['PA','ST']
    adjcountyDict['ST']=['SG','YE','CA','PA']    
    adjcountyDict['TE']=['PO','CMHD','CS','LC','FL','CH']
    adjcountyDict['TO']=['GL','PO','LI']
    adjcountyDict['TR']=['RS','BH','YE']
    adjcountyDict['VA']=['PH','GF','MC','RO','CMHD','DA']
    adjcountyDict['WI']=['RI','CMHD','FA','PI','DW']
    adjcountyDict['YE']=['CA','TR','BH','ST']
    return adjcountyDict




def AdjCounties_WtAverage(name,year,statistic,countyDict):
    #INPUT: county of interest, year of interest, statistic of interest(ie 'rate','count')
    #OUTPUT:array of weighted average of the statistic of interest for each week in the year and county of interest
    #by Jake
    if name != 'STATE':
        AdjCounties = countyDict[name]['Adjacent'] #Extract a list of adjacent counties
        matrix = np.zeros((len(countyDict[name][year][statistic]),len(AdjCounties))) #Initialize a matrix to store weighted rates
        total = sum(countyDict[name][year]['pop'][0] for county in AdjCounties) #Calculate total adjacent population (sum of adjacent counties)
        
        #Extract statistic and weight them
        i = 0 #Counter to iterate through columns of the matrix
        for county in AdjCounties:
            pop = countyDict[county][year]['pop'][0] #Get the population of a given county
            #weight = some function of population
            #The weighting function can be easily altered
            weight = pop/total
            weightedList = weight*np.array(countyDict[county][year][statistic]) #Apply weights
            matrix[ : , i] = weightedList #Add weighted rates to the next column in the matrix
            i += 1
            
        #Sum across rows and divide by the number of adjacent counties to get an average
        weightedAverage = sum(matrix[ : , i] for i in range(0,len(AdjCounties)))/len(AdjCounties)
    else:
        weightedAverage = 0
    return weightedAverage


##############################################################################
#K-Nearest Exponential Function
##############################################################################

def kNearest(predictionDict, countyList, years, countyDict):
    #INPUT:Numver of nearest weeks:k
    #OUTPUT: prediction counts for 
    #by Van
    for county in countyList:
        for year in years:
            counts=countyDict[county][year]['count']
            for j in range(1,len(counts)+1):
                weightedCount=0
                ysum=0
                alpha=1-(0.01)**float(1/j)
                for i in range(1,j+1):
                    weight=alpha*(1-alpha)**(i-1) #exponential weights of each count
                    weightedCount+=weight*countyDict[county][year]['count'][j-i]
                    ysum+=countyDict[county][year]['count'][j-i]
                ybar=ysum/len(range(1,j+1))
                predictionDict[county][year]['count'].append(weightedCount)
                predictionDict[county][year]['ybar'].append(ybar)
    return predictionDict

##############################################################################
#K-Nearest COnventional Function
##############################################################################

def kNearestCon(predictionDict,countyList,years, countyDict):
    #INPUT:Numver of nearest weeks:k
    #OUTPUT: prediction counts for 
    #by Van
    for county in countyList:
        for year in years:
            counts=countyDict[county][year]['count']
            k=3           #number of nearest weeks to predict week k+1
            for j in range(1,k):   #start to predict from week 2 to week k
                weightedCount=0
                ysum=0
                alpha=1-(0.01)**float(1/j)
                for i in range(0,j):
                    ysum+=countyDict[county][year]['count'][i]
                    weight=alpha*(1-alpha)**(j-1) #exponential weights of each count
                    weightedCount+=weight*countyDict[county][year]['count'][i]
                ybar=ysum/len(range(0,j))
                predictionDict[county][year]['count'].append(weightedCount)
                predictionDict[county][year]['ybar'].append(ybar)
            for j in range(k,len(counts)+1):   #start to predict from week k+1(6)
                weightedCount=0
                ysum=0
                alpha=1-(0.01)**float(1/k)
                for i in range(1,j+1):
                    ysum+=countyDict[county][year]['count'][j-i]
                ybar=ysum/len(range(1,j+1))
                predictionDict[county][year]['ybar'].append(ybar)
                for i in range(k):
                    weight=alpha*(1-alpha)**(i) #exponential weights of each count
                    weightedCount+=weight*countyDict[county][year]['count'][j-i-1]
                    
                predictionDict[county][year]['count'].append(weightedCount)
    return predictionDict
