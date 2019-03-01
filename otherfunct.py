# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 22:36:58 2019

@author: matth
"""
#countyDict['GR']=['MI','PW','CMHD','RA','BE']
#countyDict['PI']=['GF','MC','CMHD','WI','FA','CMHD']
#countyDict['ST']=['PA','SG','YE','CA']
#'GR','PI','ST'

def CountyListBuild():
    countyList=['BE','BH','BL','BR','CA','CS','CMHD','FA','FL','GA','GF','GL','HI',
          'JE','LA','LC','LI','LN','MA','MC','ME','MI','MS','PA','PH','PO','PR','PW',
          'RA','RI','RO','RS','SA','SH','SB','SG','TE','TO','TR','VA','WI','YE']
    return countyList
def countyDictBuild():
    countyList=CountyListBuild()
    countyDict={}
    countyDict=dict.fromkeys(countyList)
    countyDict['BE']=['RA','SB','MA','CMHD']
    countyDict['BH']=['YE','TR','CA','RS','PR']
    countyDict['BL']=['HI','PH']
    countyDict['BR']=['LC','JE','GA','ME']
    countyDict['CA']=['PA','YE','BH']
    countyDict['CS']=['TE','LC','ME','CMHD']
    countyDict['CMHD']=['YE','RS','GF','PH','BL','CS','ME','SG']
    countyDict['FA']=['WI','PR','CS']
    countyDict['FL']=['LI','SA','LA','MS','PW','LC','TE','PO','GL']
    countyDict['GA']=['MA','JE','BR','ME','PA']
    countyDict['GF']=['RO','PH','VA','MC','CMHD']
    countyDict['GL']=['FL','PO','TO']
    countyDict['HI']=['LI','CMHD','BL']
    countyDict['JE']=['MA','SB','CMHD','PW','LC','BR','GA']
    countyDict['LA']=['MS','SA','FL','PW']
    countyDict['LC']=['FL','TE','CS','ME','BR','JE','PW']
    countyDict['LI']=['TO','PO','CMHD','HI']
    countyDict['LN']=['FL','SA']
    countyDict['MA']=['BE','SB','JE','GA']
    countyDict['MC']=['GF','VA','RO','RI','CMHD',]
    countyDict['ME']=['LC','CS','SG','PA','GA','BR']
    countyDict['MI']=['SA','MS']
    countyDict['MS']=['MI','SA','LA','FL','PW','RA']
    countyDict['PA']=['GA','ME','SG','CA']
    countyDict['PH']=['BL','GF','VA']
    countyDict['PO']=['GL','FL','TE','CMHD','LI','TO']
    countyDict['PR']=['BH','RS','CMHD',]
    countyDict['PW']=['CMHD','MS','FL','LC','JE']
    countyDict['RA']=['MS','CMHD','BE']
    countyDict['RI']=['RO','MC','CMHD','WI']
    countyDict['RO']=['SH','CMHD','VA','MC','RI']
    countyDict['RS']=['GF','TR','BH','PR','CMHD']
    countyDict['SA']=['LN','FL','LA','MS','MI']
    countyDict['SH']=['CMHD','RO']
    countyDict['SB']=['JE','CMHD','BE','MA']
    countyDict['SG']=['PA']
    countyDict['TE']=['PO','CMHD','CS','LC','FL']
    countyDict['TO']=['GL','PO','LI']
    countyDict['TR']=['RS','BH','YE']
    countyDict['VA']=['PH','GF','MC','RO','CMHD']
    countyDict['WI']=['RI','CMHD','FA']
    countyDict['YE']=['CA','TR','BH']
    return countyDict

def databuild(county,adj,input2,lag,f,countyDict,countylist):
    keep_col = ['year','flu week',county+" rate",county+" pop",county+" count",county+" weighted rate"]
    newf=f[keep_col]
    if adj=="Y":
        adjcounty=countyDict[county]
        n=0
        #print(adjcounty)
        adjlist=[]         
        for n in range(len(adjcounty)):
            keep_adj=[adjcounty[n]+' rate', adjcounty[n]+' count', adjcounty[n]+' pop',adjcounty[n]+" weighted rate"]
            n=n+1
            adjlist.extend(keep_adj)
            #keep_col.extend(keep_adj)
            i=0
            #print(keep_col)
    if input2[i] in countylist:
        for i in range(len(input2)):
            add_county=[input2[i]+' rate', input2[i]+' count', input2[i]+' pop',input2[i]+" weighted rate"]
            print(add_county)
            adjlist.extend(add_county)
            i=i+1
    new_f1 = f[adjlist]
    #new_f1.rename(columns={'flu week':'lag week'},inplace=True)
    new_f1=new_f1.shift(lag)
    new_f= newf.join(new_f1, how='outer')
    if len(adjlist)==0:
        new_f=newf
    return new_f
def smoothdata(countylist,a,f):
    import pandas as pd
    for county in countylist:
        key_col=county+ " rate"
        colnum=f.columns.get_loc(key_col)
        lastrow=f.shape[0]
        colname = county+" weighted rate"
        d=[0.0]
        yhat1=f.iloc[1,colnum]
        d.append(yhat1)
        for i in range(2,lastrow):
            b=f.iloc[i,colnum]
            c=d[i-1]
            b=a*b+(1-a)*c
            d.append(b)
        d=pd.Series(d)
        f.insert(colnum+1,colname,d)
    return f