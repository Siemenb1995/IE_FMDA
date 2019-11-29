# -*- coding: utf-8 -*-
"""
This program takes data from https://unstats.un.org/sdgs/indicators/database/
to test whether there is a correlation between the proportion of medium and high-
tech industry in a country (SDG 9.b.1) and the compliance with the Rotterdam Convention 
on Hazardous Chemicals and Pesticides in International Trade (SDG 12.4.1).
"""
#%% Import
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sci

#%% Open Data
SDG = open("SDGdata_9-b-1_12-4-1.csv")
SDG.readline()

#%% Datasets
mhtiProp = [] #high- and medium- tech industry proportion
mhtiPropCountryName = []
compRot = [] #compliance with the Rotterdam convention
compRotCountryName = []

try: # the following code splits the data into lists of values and country names for each SDG
    for line in SDG:
        _, _, _, SeriesCode, _, _, GeoAreaName, TimePeriod, Value, _,  _, _, _, _, _, _, _, _\
        = line.strip().split('","')
        if SeriesCode == "NV_IND_TECH" and TimePeriod == '2015': #SDG 9.b.1
            mhtiProp.append(float(Value))
            mhtiPropCountryName.append(GeoAreaName)
        elif SeriesCode == "SG_HAZ_CMRROTDAM": #SDG 12.4.1
            compRot.append(float(Value))
            compRotCountryName.append(GeoAreaName)
except: #stops the code at the white lines
    SDG.close()
    del SeriesCode, GeoAreaName, TimePeriod, Value

#%% Sort
msortarray = np.argsort(mhtiPropCountryName) #creates an array of index positions according to countries' alphabetical order
mhtiPropCountryName = list(np.array(mhtiPropCountryName)[msortarray]) #sorts the country name list to alphabetical order
mhtiProp = list(np.array(mhtiProp)[msortarray]) #sorts the value list according to the same order

msortarray = np.argsort(compRotCountryName) #creates an array of index positions according to countries' alphabetical order
compRotCountryName = list(np.array(compRotCountryName)[msortarray]) #sorts the country name list to alphabetical order
compRot = list(np.array(compRot)[msortarray]) #sorts the value list according to the same order

#%%Delete Missing Values
compRot = [v for i, v in zip(compRotCountryName, compRot) if i in mhtiPropCountryName] #takes out values for country names which do not occur in the other list
compRotCountryName = [i for i in compRotCountryName if i in mhtiPropCountryName] 

mhtiProp = [v for i, v in zip(mhtiPropCountryName, mhtiProp) if i in compRotCountryName] #takes out values for country names which do not occur in the other list  
mhtiPropCountryName = [i for i in mhtiPropCountryName if i in compRotCountryName]
      
#%% Sanity Check
def sanityCheck():
    print('Sanity Check:') # title
    if compRotCountryName == mhtiPropCountryName: #checks whether the two lists of country names are the same
        print("Countries in both lists match")
    else: 
        print("Warning: Countries in the lists don't match!")
    if len(compRot) == len(mhtiProp): #checks whether the two lists of values have the same amount of values
        print("Both lists have the same length")
    else:
        print("Warning: the lists don't have the same length!")
    # the following block of code checks whether dataset values and list values match by country
    misMatchCount = 0
    SDGcheck = open("SDGdata_9-b-1_12-4-1.csv")
    SDGcheck.readline()
    try:
        for line in SDGcheck:
            _, _, _, SeriesCode, _, _, GeoAreaName, TimePeriod, dataBaseValue, _,  _, _, _, _, _, _, _, _ = line.strip().split('","')
            if SeriesCode == "NV_IND_TECH" and TimePeriod == '2015'and GeoAreaName in mhtiPropCountryName:
                indexNr = mhtiPropCountryName.index(GeoAreaName) #returns the index number of the country in mhtiPropCountryName 
                listValue = mhtiProp[indexNr] #returns the value of the country in mhtiProp
                if listValue != float(dataBaseValue): #compares the list value with the database value
                    misMatchCount += 1 #counts the amount of mismatches
            if SeriesCode == "SG_HAZ_CMRROTDAM" and GeoAreaName in compRotCountryName:
                indexNr = compRotCountryName.index(GeoAreaName) #returns the index number of the country in mhtiPropCountryName 
                listValue = compRot[indexNr] #returns the value of the country in mhtiProp
                if listValue != float(dataBaseValue): #compares the list value with the database value
                    misMatchCount += 1 #counts the amount of mismatches
    except:
        SDGcheck.close()
        del SeriesCode, GeoAreaName, TimePeriod, dataBaseValue
    print("Mismatches found between dataset and list values: ", misMatchCount)  

sanityCheck() #to run the sanity check
#%% Plot and Save as PNG
def scatterPlot():
    plt.scatter(mhtiProp, compRot, marker='x',  c = 'black')
    plt.xlabel('Proportion of medium and high-tech industry \n value added in total value added (%)')
    plt.ylabel('Compliance with the Rotterdam Convention \n on hazardous waste and other chemicals (%)')
    plt.xlim(0, 100) #these two lines set the axis range
    plt.ylim(0, 100)
    ax = plt.gca() #these two lines set the aspect ratio
    ax.set_aspect(aspect=1) 
    plt.savefig('scatterplot.png', bbox_inches='tight') #saves the figure without large margins
    plt.close() #closes the plot so it doesn't show in the console
    
scatterPlot() #to make a scatterplot

#%% Calculate Linear & Monotonic Correlation Coefficients and p-Values
def correlationAnalysis():
    print('\nCorrelation Analysis:') # blank line and title
    linCoP = sci.pearsonr(mhtiProp, compRot) #calculates the linear correlation coefficient and p-value
    linCo = (linCoP[0]) #linear correlation coefficient
    linP = (linCoP[1]) #p-value
    
    print ("The Linear Correlation Value is: ", linCo,"\nIts p-value is: ", linP, "\n",
 "\nThe linear correlation coefficient measures the linear relationship\
 between two datasets. Strictly speaking, linear correlation requires\
 that each dataset be normally distributed. Like other correlation\
 coefficients, this one varies between -1 and +1 with 0 implying no\
 correlation. Correlations of -1 or +1 imply an exact linear\
 relationship. Positive correlations imply that as x increases, so does\
 y. Negative correlations imply that as x increases, y decreases.\nThe\
 p-value roughly indicates the probability of an uncorrelated system \
 producing datasets that have a linear correlation at least as extreme \
 as the one computed from these datasets. The p-values are not entirely \
 reliable but are probably reasonable for datasets larger than 500 or so.")
    
    print('\n') # 2 blank lines
    monCoP = sci.spearmanr(mhtiProp, compRot) #calculates the monotonic correlation coefficient and p-value
    monCo = (monCoP[0]) #linear correlation coefficient
    monP = (monCoP[1]) #p-value
    
    print("The Monotonic Correlation Value is: ", monCo,"\nIts p-value\
 is: ", monP, "\n",
 "\nThe monotonic correlation is a nonparametric measure of the monotonicity\
 of the relationship between two datasets. Unlike the linear correlation, \
 the monotonic correlation does not assume that both datasets are normally \
 distributed. Like other correlation coefficients, this one varies between \
 -1 and +1 with 0 implying no correlation. Correlations of -1 or +1 imply an \
 exact monotonic relationship. Positive correlations imply that as x increases,\
 so does y. Negative correlations imply that as x increases, y decreases.\nThe \
 p-value roughly indicates the probability of an uncorrelated system producing\
 datasets that have a monotonic correlation at least as extreme as the one computed\
 from these datasets. The p-values are not entirely reliable but are probably reasonable for datasets larger than 500 or so.")
    
    print(" ") # blank line
    # the following blocks of code print the significance level based on the p-value
    if linP<=0.01: 
        print("The Linear Correlation is statistically significant at a level of 0.01")
    elif linP<=0.05:
        print("The Linear Correlation is statistically significant at a level of 0.05")
    elif linP<=0.1:
        print("The Linear Correlation is statistically significant at a level of 0.1")
    else: print("The Linear Correlation is not statistically significant")
    
    if monP<=0.01:
        print("The Monotonic Correlation is statistically significant at a level of 0.01")
    elif monP<=0.05:
        print("The Monotonic Correlation is statistically significant at a level of 0.05")
    elif monP<=0.1:
        print("The Monotonic Correlation is statistically significant at a level of 0.1")
    else: print("The Monotonic Correlation is not statistically significant")
    
    print("\nThe positive correlation between 0.5 and 0.6 shows that there is relative\
synergy between a country's proportion of medium and high-tech industry in value creation \
and compliance with the Rotterdam Convention on hazardous waste and other chemicals.\
Given that the monotonic correlation is higher and more statistically significant, \
the relationship between the two indicators can be best approximated using monotonic \
correlaton.")

correlationAnalysis() #to run the correlationAnalysis