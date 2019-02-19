# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 11:41:29 2019

@author: annag
"""



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
