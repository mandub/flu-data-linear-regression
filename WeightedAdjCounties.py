# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:28:15 2019

@author: jakeo
"""
import numpy as np
#---------------------------------------------Neighboring county dictionary-----------------------------------------
#This is an example of what a neighboring county dictionary might look like. This example has only one key,
#'MS' for Missoula county, whose value is a list of adjacent county names (two letter codes). Subsequent versions
#will have a key-value pair for each county. 
#Team 1 has this information, since Matt's data compiler includes adjacent counties, but I'm not exactly sure how...
#We can either modify this function to work with their system, or just extract a dictionary from their dataset
#that will work with the function. 
neighborDict = {}
neighborDict['MS'] = ['LA','RA','FL','PW','SA','MI']

#-----------------------------------------------Weighted Average Function---------------------------------------------------
#This function takes a county name (two letter code) and a year (1 through 9) and returns an array containing the
#weighted average of the rates in adjacent counties for all weeks in the given year. 
#This function uses information from CountyRateDict and CountyPopDict.
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

#This line produces an array of weighted average rates in counties adjacent to Missoula County for year 1
#AdjW = AdjCounties_WtAverage('MS',1)

AdjacentWAve = {}
for county in countyList:
    AdjacentWAve[county]={}
    for year in years:
        AdjacentWAve[county][year] = AdjCounties_WtAverage(county, year, 'rate', countyDict)


