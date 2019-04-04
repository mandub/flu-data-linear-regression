# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:41:29 2019

@author: annag
"""
import numpy as np
import matplotlib.pyplot as plt

 

def pathfinder(pathlist):
    #Input: list of paths
    #Output: correct path for user
    #
    names = ["Anna", "Mandub", "Jake", "Bill", "Other"]
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
                        x0.append(OtherPredVar[county][year][i+PredWeek-1])
                        q = 1 + PredWeek + 1
                    else:
                        x0.append(0)
                        q = 1 + PredWeek + 1                        
                X = np.matrix(x0).reshape(q,1)
                D[county][year].append((y,X))
    return D, q

def InitialTrainingMatricies( countyList, years, D, Aci, Zci, q):   
    for county in countyList:
        Aci[county]={}
        Zci[county]= {}
        for year in years:
            Aci[county][year]= np.zeros(shape =(q,q))
            Zci[county][year]= np.matrix(np.zeros(shape = (q,1)))        
            for i in range(0, 10):
                yi = D[county][year][i][0]
                xi = D[county][year][i][1]
                Aci[county][year] += xi*xi.T
                Zci[county][year] += xi*yi
    return Aci, Zci

def NextTrainingMatricies( county, year, D, Aci, Zci, j):         
    yi = D[county][year][j][0]
    xi = D[county][year][j][1]
    Aci[county][year] += xi*xi.T
    Zci[county][year] += xi*yi
    return Aci, Zci

def InitialBetaSolver(countyList, years, Aci, Zci, Bci, q):
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
    A = Aci[county][year]
    Z = Zci[county][year]
    try:
        b = np.linalg.solve(A,Z)
        Bci[county][year]=b
    except:
        Bci[county][year]=(np.zeros(shape = (q,1)))
        pass
    return Bci

def initialpredictionDict(countyList, years, TruePredPair, D, Bci, PredWeek, q):
    TruePredPair[PredWeek] = {}
    for county in countyList:
        TruePredPair[PredWeek][county]={}
        for year in years:
            TruePredPair[PredWeek][county][year] = []
            X = np.matrix(np.zeros(shape = (10, q)))
            for j in range(10):
                X[j,] = D[county][year][j][1].T
            B = Bci[county][year]
            pred = X*B
            for j in range(10):
                TruePredPair[PredWeek][county][year].append((float(D[county][year][j][0]),float(pred[j,])))

    return TruePredPair

def NextpredictionDict(county, year, D, Bci,q,TruePredPair, j, PredWeek):
    X = np.matrix(np.zeros(shape = (1, q)))
    X = D[county][year][j][1].T
    B = Bci[county][year]
    pred = X*B
    TruePredPair[PredWeek][county][year].append((float(D[county][year][j][0]),float(pred)))

    return TruePredPair


def Linear_Regression(NumPredWeeks, OtherPredVar, years, countyDict, countyList, VoI):
    #INPUT: array of possible # of pred weeks, List of other pred var, number of pred var, list of years and counties, county dict
    #OUTPUT:dict of predictions by pred weeks, county, year  for each wee, dict of True values by county by year, for each week
    #LinRegPred[# of weeks][county][year] , YTrues[# of weeks][county][year]
    TruePredPair = {}
    for i in NumPredWeeks:
        PredWeek = i
        D = {}
        D, q = Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,VoI)
        Aci = {}
        Zci = {}
        Aci, Zci = InitialTrainingMatricies( countyList, years, D, Aci, Zci, q)
        Bci = {}
        Bci = InitialBetaSolver(countyList, years, Aci, Zci, Bci, q)
        TruePredPair = initialpredictionDict(countyList, years, TruePredPair, D, Bci, PredWeek, q)
        for county in countyList:
            for year in years:
                for j in range(10,len(D[county][year])):
                    TruePredPair = NextpredictionDict(county, year, D, Bci,q,TruePredPair, j, PredWeek)
                    Aci, Zci = NextTrainingMatricies( county, year, D, Aci, Zci,j)
                    Bci = NextBetaSolver(county, year, Aci, Zci, Bci, q, j)
    return TruePredPair

###############################################################################
# K NEAREST NEIGHBORS
###############################################################################
# K-Nearest Exponential Function
def kNearest(alpha,k, countyList, years,countyDict, predictionDict):
    #INPUT:Numver of nearest weeks:k
    #OUTPUT: prediction counts for all weeks staring from week 1
    #
    for county in countyList:
        for year in years:
            counts=countyDict[county][year]['count']
            for j in range(1,len(counts)+1):
                sumWeight=0
                for i in range(1,j+1):
                    weight=alpha*(1-alpha)**(i-1) #exponential weights of each rate
                    weightedCount=weight*countyDict[county][year]['count'][j-i]
                    sumWeight += weightedCount    #sum of weighted counts 
                    avgCount=sumWeight            #average of weighted rates
                predictionDict[county][year]['count'].append(avgCount)
    return avgCount


###############################################################################
#PLOTTING RESULTS
###############################################################################

def plot1(County,Year, TruePredPair):
    Year= Year
    y = range(len (TruePredPair[County][Year]))
    x = []
    z = []
    for i in range(len (TruePredPair[County][Year])):       
        x.append(TruePredPair[County][Year][i][0])
        z.append(TruePredPair[County][Year][i][1])
    Title= County +" Year " +str (Year)
    plt.title(Title)
    plt.plot(y, x,  'bo-', linewidth = 2.0, label = "Observed Rates")
    plt.plot(y, z, 'ro-', linewidth = 2.0, label = "Prediction Rates")
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
    #
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



def createPredictionDict(countylist):
    predictionDict={}
    for county in countyList:
        predictionDict.update({county:{}})
        for year in years:
            predictionDict[county].update({year:{'rate':[],'count':[],'ybar':[]}})
    return predictionDict
























