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

        next(f)

        next(f)

        line = f.readline()

        lineString=line.split(",")

        if lineString[0] == 'revised':           #use first 3rd line to make list of counties

            for string in lineString:

                if string not in countyList:

                    countyList.append(string)

            countyList = countyList[2:-1]        #get rid of etxras

            for county in countyList:            #initialized dict of dict

                countyDict[county]={}

                for year in years:

                    countyDict[county][year]={'rate':[],'count':[],'pop':[]}

            next(f)

        for record in f:                         #start on first line of data

            dataString = record.split(",")

            data = convertData(dataString)       #convert data to floats

            for i in range(3,len(data)-84):    

                countyDict[countyList[i-3]][data[1]]['rate'].append(data[i])   #append rate data

            for i in range(45,len(data)-42):

                countyDict[countyList[i-45]][data[1]]['count'].append(data[i]) #append count data

            for i in range(87,len(data)):

                countyDict[countyList[i-87]][data[1]]['pop'].append(data[i])   #append pop data

    return countyDict, countyList



###############################################################################

# LINEAR REGRESSION

###############################################################################





def Data(countyList, years, countyDict, PredWeek, OtherPredVar, D, q):

    #INPUT: Lists of counties, years, # of weeks used to predict, and other predictor variables, empty Dict, q

    #OUTPUT: Tuple containing (matrix of single Actual rate, matrix of other preidctor variables)

    #

    for county in countyList:

        D[county]={}

        for year in years:

            D[county][year]=[]

            for i in range(len(countyDict[county][year]['rate'])-(PredWeek+1)):

                y = np.matrix(countyDict[county][year]['rate'][i+PredWeek+1])

                x0 = [1]

                x1R = []

                for j in range(i,i+PredWeek):

                    x1R.append(countyDict[county][year]['rate'][j])

                x1R.reverse()

                x0.extend(x1R)

                if len(OtherPredVar) != 0:

                    OPV = OtherPredVar[county][year][i]

                    x0.append(float(OPV))

                X = np.matrix(x0).reshape(q,1)

                D[county][year].append((y,X))

    return D



def TrainingMatricies( countyList, years, D, Ac, Zc,q):  

    #INPUT: Lists of counties, years, List of Tupels, empty Dicts Ac and Zc, and q

    #OUTPUT: dicts for ea county and year of q x q matrix A = X*X.T and q x 1 matrix Z = X*Y

    #  Ac[county][year]

    for county in countyList:

        Ac[county]={}

        Zc[county]= {}

        for year in years:

            Ac[county][year]= np.zeros(shape =(q,q))

            Zc[county][year]= np.matrix(np.zeros(shape = (q,1)))        

            for i in range(0, len(D[county][year])-1):

                yi = D[county][year][i][0]

                xi = D[county][year][i][1]

                Ac[county][year] += xi*xi.T

                Zc[county][year] += xi*yi

    return Ac, Zc



def BetaSolver(countyList, years, Ac, Zc, Bc,q):

    #INPUT: Lists of counties and years, Dicts of Ac and Zc, empty dict Bc, and q

    #OUTPUT: Dict for ea county and year of Beta's 

    #  Bc[county][year]

    for county in countyList:

        Bc[county] = {}

        for year in years:

            #Bc[county][year]=[]

            A = Ac[county][year]

            Z = Zc[county][year]

            try:

                b = np.linalg.solve(A,Z)

                Bc[county][year]=b

            except:

                Bc[county][year]=(np.zeros(shape = (q,1)))

                pass

    return Bc



def predictionDict(countyList, years, D, Bc,q):

    #INPUT: List of counties and years, Data tuples, Beta Dict,q

    #OUTPUT: Dicts per county per year of YTrue = Actual data and YHat = Predicted data

    #

    YTrue = {}

    YHat = {}

    for county in countyList:

        YTrue[county]={}

        YHat[county]={}

        for year in years:

            YTrue[county][year] = []

            X = np.matrix(np.zeros(shape = (len(D[county][year]), q)))

            for i in range(len(D[county][year])):

                YTrue[county][year].append(float(D[county][year][i][0]))

                X[i,] = D[county][year][i][1].T

            B = Bc[county][year]

            YHat[county][year] = X*B

    return YTrue, YHat



def Linear_Regression(NumPredWeeks, OtherPredVar, opvn, years, countyDict, countyList):

    #INPUT: array of possible # of pred weeks, List of other pred var, number of pred var, list of years and counties, county dict

    #OUTPUT:dict of predictions by pred weeks, county, year  for each wee, dict of True values by county by year, for each week

    #LinRegPred[# of weeks][county][year] , YTrues[# of weeks][county][year]

    LinRegPred = {}

    YTrues = {}

    for i in NumPredWeeks:

        PredWeek = i

        q = 1 + PredWeek + opvn

        D = {}

        D =  Data(countyList, years, countyDict, PredWeek, OtherPredVar, D,q)

        Ac = {}

        Zc = {}

        Ac, Zc = TrainingMatricies(countyList, years, D, Ac, Zc,q)

        Bc = {}

        Bc = BetaSolver(countyList, years, Ac, Zc, Bc, q) 

        YTrue, YHat = predictionDict(countyList, years, D, Bc,q)

        LinRegPred[i]= YHat

        YTrues[i] = YTrue

    return LinRegPred, YTrues





###############################################################################

#PLOTTING RESULTS

###############################################################################



def plot1(County,Year, YTrue, predictionDict):

    #INPUT: County and year you want to plot, YTrue[PredWeek], prediction dict[PredWeek] PredWeek = number from NumPredWeeks

    #OUTPUT: Plot of true values (black) and predicted values (blue)

    #    

    Year= Year

    y = range(len (YTrue[County][Year]))

    x = YTrue[County][Year]

    z = predictionDict[County][Year]

    #actualNames[counties.index(County)]

    Title= County +" Year " +str (Year)

    plt.title(Title)

    plt.plot(y, x, color = "black", linewidth = 2.0, label = "Observed Rates")

    plt.plot(y, z, color = "blue", linewidth = 2.0, label = "Prediction Rates")

    plt.legend(loc = "upper right")

    plt.show()



###############################################################################

#ADJACENT COUNTY FUNCTIONS

###############################################################################



def adjcountyDictBuild(countyList):

    adjcountyDict={}

    adjcountyDict=dict.fromkeys(countyList)

    adjcountyDict['BE']=['RA','SB','MA','CMHD']

    adjcountyDict['BH']=['YE','TR','CA','RS','PR']

    adjcountyDict['BL']=['HI','PH']

    adjcountyDict['BR']=['LC','JE','GA','ME']

    adjcountyDict['CA']=['PA','YE','BH']

    adjcountyDict['CS']=['TE','LC','ME','CMHD']

    adjcountyDict['CMHD']=['YE','RS','GF','PH','BL','CS','ME','SG']

    adjcountyDict['FA']=['WI','PR','CS']

    adjcountyDict['FL']=['LI','SA','LA','MS','PW','LC','TE','PO','GL']

    adjcountyDict['GA']=['MA','JE','BR','ME','PA']

    adjcountyDict['GF']=['RO','PH','VA','MC','CMHD']

    adjcountyDict['GL']=['FL','PO','TO']

    adjcountyDict['HI']=['LI','CMHD','BL']

    adjcountyDict['JE']=['MA','SB','CMHD','PW','LC','BR','GA']

    adjcountyDict['LA']=['MS','SA','FL','PW']

    adjcountyDict['LC']=['FL','TE','CS','ME','BR','JE','PW']

    adjcountyDict['LI']=['TO','PO','CMHD','HI']

    adjcountyDict['LN']=['FL','SA']

    adjcountyDict['MA']=['BE','SB','JE','GA']

    adjcountyDict['MC']=['GF','VA','RO','RI','CMHD',]

    adjcountyDict['ME']=['LC','CS','SG','PA','GA','BR']

    adjcountyDict['MI']=['SA','MS']

    adjcountyDict['MS']=['MI','SA','LA','FL','PW','RA']

    adjcountyDict['PA']=['GA','ME','SG','CA']

    adjcountyDict['PH']=['BL','GF','VA']

    adjcountyDict['PO']=['GL','FL','TE','CMHD','LI','TO']

    adjcountyDict['PR']=['BH','RS','CMHD',]

    adjcountyDict['PW']=['CMHD','MS','FL','LC','JE']

    adjcountyDict['RA']=['MS','CMHD','BE']

    adjcountyDict['RI']=['RO','MC','CMHD','WI']

    adjcountyDict['RO']=['SH','CMHD','VA','MC','RI']

    adjcountyDict['RS']=['GF','TR','BH','PR','CMHD']

    adjcountyDict['SA']=['LN','FL','LA','MS','MI']

    adjcountyDict['SH']=['CMHD','RO']

    adjcountyDict['SB']=['JE','CMHD','BE','MA']

    adjcountyDict['SG']=['PA']

    adjcountyDict['TE']=['PO','CMHD','CS','LC','FL']

    adjcountyDict['TO']=['GL','PO','LI']

    adjcountyDict['TR']=['RS','BH','YE']

    adjcountyDict['VA']=['PH','GF','MC','RO','CMHD']

    adjcountyDict['WI']=['RI','CMHD','FA']

    adjcountyDict['YE']=['CA','TR','BH']

    return adjcountyDict





def AdjCounties_WtAverage(name,year,statistic,countyDict):

    #INPUT: county of interest, year of interest, statistic of interest(ie 'rate','count')

    #OUTPUT:array of weighted average of the statistic of interest for each week in the year and county of interest

    #

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

    return weightedAverage





'''Van's K Nearest Neighbors Functions'''



years=[1,2,3,4,5,6,7,8,9]       

def countyData(countyList):

    #INPUT: county

    #OUTPUT: year, rate, count

    countyDict={}

    path = '/Users/Cassidy/Desktop/Flu_project/current.csv'

    for county in countyList: 

        countyDict.update({county:{'adjCounty':[]}})

        for year in years:

            countyDict[county].update({year:{'rate':[],'count':[]}})

    with open(path) as f:

        next(f)

        next(f)

        next(f)

        next(f)

        line=f.readline()  #Read the 4th line(row)

        lineString=line.split(",")  #split the 4th line(row)

        for record in f:   #goes through every row, starting at 5th row

            dataString = record.split(",") #split data

            data=convertData(dataString)   #convert all data rows to floating points

            for county in countyDict:

                for string in lineString:  #goes through the 4th line(row)

                    if string==county+' '+'rate':

                        position_rate=lineString.index(string)

                    if string==county+' '+'count':

                        position_count=lineString.index(string)

                        for year in years:

                            if data[3]==year:

                                rate=data[position_rate]       #position of county's rate

                                countyDict[county][year]['rate'].append(rate)

                                count=data[position_count]     #position of county's counts

                                countyDict[county][year]['count'].append(count)

                                

    if ValueError:

        pass

    return countyDict





countyList=['BE','BH','BL','BR','CA','CS','CMHD','FA','FL','GA','GF','GL','HI',

          'JE','LA','LC','LI','LN','MA','MC','ME','MI','MS','PA','PH','PO','PR','PW',

          'RA','RI','RO','RS','SA','SH','SB','SG','TE','TO','TR','VA','WI','YE']

countyDict=countyData(countyList)

def adjcountyDict(countyList):

    countyDict['BE']['adjCounty']=['RA','SB','MA','CMHD']

    countyDict['BH']['adjCounty']=['YE','TR','CA','RS','PR']

    countyDict['BL']['adjCounty']=['HI','PH']

    countyDict['BR']['adjCounty']=['LC','JE','GA','ME']

    countyDict['CA']['adjCounty']=['PA','YE','BH']

    countyDict['CS']['adjCounty']=['TE','LC','ME','CMHD']

    countyDict['CMHD']['adjCounty']=['YE','RS','GF','PH','BL','CS','ME','SG']

    countyDict['FA']['adjCounty']=['WI','PR','CS']

    countyDict['FL']['adjCounty']=['LI','SA','LA','MS','PW','LC','TE','PO','GL']

    countyDict['GA']['adjCounty']=['MA','JE','BR','ME','PA']

    countyDict['GF']['adjCounty']=['RO','PH','VA','MC','CMHD']

    countyDict['GL']['adjCounty']=['FL','PO','TO']

    countyDict['HI']['adjCounty']=['LI','CMHD','BL']

    countyDict['JE']['adjCounty']=['MA','SB','CMHD','PW','LC','BR','GA']

    countyDict['LA']['adjCounty']=['MS','SA','FL','PW']

    countyDict['LC']['adjCounty']=['FL','TE','CS','ME','BR','JE','PW']

    countyDict['LI']['adjCounty']=['TO','PO','CMHD','HI']

    countyDict['LN']['adjCounty']=['FL','SA']

    countyDict['MA']['adjCounty']=['BE','SB','JE','GA']

    countyDict['MC']['adjCounty']=['GF','VA','RO','RI','CMHD',]

    countyDict['ME']['adjCounty']=['LC','CS','SG','PA','GA','BR']

    countyDict['MI']['adjCounty']=['SA','MS']

    countyDict['MS']['adjCounty']=['MI','SA','LA','FL','PW','RA']

    countyDict['PA']['adjCounty']=['GA','ME','SG','CA']

    countyDict['PH']['adjCounty']=['BL','GF','VA']

    countyDict['PO']['adjCounty']=['GL','FL','TE','CMHD','LI','TO']

    countyDict['PR']['adjCounty']=['BH','RS','CMHD',]

    countyDict['PW']['adjCounty']=['CMHD','MS','FL','LC','JE']

    countyDict['RA']['adjCounty']=['MS','CMHD','BE']

    countyDict['RI']['adjCounty']=['RO','MC','CMHD','WI']

    countyDict['RO']['adjCounty']=['SH','CMHD','VA','MC','RI']

    countyDict['RS']['adjCounty']=['GF','TR','BH','PR','CMHD']

    countyDict['SA']['adjCounty']=['LN','FL','LA','MS','MI']

    countyDict['SH']['adjCounty']=['CMHD','RO']

    countyDict['SB']['adjCounty']=['JE','CMHD','BE','MA']

    countyDict['SG']['adjCounty']=['PA']

    countyDict['TE']['adjCounty']=['PO','CMHD','CS','LC','FL']

    countyDict['TO']['adjCounty']=['GL','PO','LI']

    countyDict['TR']['adjCounty']=['RS','BH','YE']

    countyDict['VA']['adjCounty']=['PH','GF','MC','RO','CMHD']

    countyDict['WI']['adjCounty']=['RI','CMHD','FA']

    countyDict['YE']['adjCounty']=['CA','TR','BH']

    return countyDict

countyDict=adjcountyDict(countyList)



#%% K-Nearest Exponential Function
def kNearest(predictionDict,countyList,years):
    #INPUT:Numver of nearest weeks:k
    #OUTPUT: prediction counts for 
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
#%%K-Nearest COnventional Function
def kNearestCon(predictionDict,countyList,years):
    #INPUT:Numver of nearest weeks:k
    #OUTPUT: prediction counts for 
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



def createPredictionDict(countylist):

    predictionDict={}

    for county in countyList:

        predictionDict.update({county:{}})

        for year in years:

            predictionDict[county].update({year:{'rate':[],'count':[],'ybar':[]}})

    return predictionDict

#predictionkNearest=createPredictionDict(countyList)#example for kNearest

#sumWeight,ybar=kNearest(alpha,k,predictionkNearest)
