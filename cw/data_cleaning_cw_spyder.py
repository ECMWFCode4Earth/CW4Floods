# -*- coding: utf-8 -*-
"""
Created on Sun May 22 12:05:38 2022

@author: Emiliana
"""

import pandas as pd
import numpy as np


#importing the dataset by reading the csv file
df = pd.read_csv('C:/Users/Emiliana/Desktop/ESOWC_2022/DATA/export.csv',sep = ';')

#displaying the first five rows of dataset 
print(df.head())

#drop some useless columns
to_drop = ['IMAGE', 'PP_TYPE', 'PP_RIVER_STAGNENT',
           'PP_STREAM_OBSERVATION_TIME', 'PP_STREAM_PROPORTIONS',
           'PP_SHORE_PLOTSIZE', 'PP_AMOUNT','PP_ADVANCED','PP_ADV_PET','PP_ADV_POSOFT',
           'PP_ADV_POHARD','PP_ADV_PS','PP_ADV_PSE', 'PP_ADV_MULTILAYER', 'PP_ADV_OTHER',
           'PP_PLASTIC_REMOVED_CHECK','ID','STREAMTYPE_WATERCOLOR', 'STREAMTYPE_ANIMALS', 'STREAMTYPE_POLLUTION',
           'STREAMTYPE_DRINK_WATER','STREAMTYPE_SWIMMING']

df.drop(to_drop, inplace=True, axis=1)

#keep only stations with more than one observation
df=df[df.groupby('ROOT_ID')['ROOT_ID'].transform('size') > 1]
df2 = df[df.duplicated(subset=['ROOT_ID'], keep=False)]
#drop empty values of water level column
df2.dropna(subset = ["WATER_LEVEL"], inplace=True)

df2=df2[df2.groupby('ROOT_ID')['ROOT_ID'].transform('size') > 1]
df2 = df2[df2.duplicated(subset=['ROOT_ID'], keep=False)]
df2=df2.sort_values("ROOT_ID")


#df2=df2.sort_values("ROOT_ID")

#drop other columns
to_drop = ['FLOW_TYPE', 'SNOW_ICE_PRESENT', 'MOISTURE', 'WL_ADVANCED', 
           'WL_WIDTH', 'WL_DEPTH', 'STREAMTYPE_TYPE', 
           'STREAMTYPE_BUILTIN', 'WL_MATERIAL', 'STREAMTYPE_GROUNDVISIBLE', 
           'STREAMTYPE_DRIESUP', 'STREAMTYPE_NAME',
           'WL_METHOD', 'WL_FLOW_VELOCITY', 'WL_DISTANCE']

df2.drop(to_drop, inplace=True, axis=1)
to_drop = ['WL_TIME_A', 'WL_TIME_B', 'WL_TIME_C', 'WL_DISTANCE_B',
           'WL_DISTANCE_C', 'PHYSICAL_SCALE_UNIT',
           'PHYSICAL_SCALE_LEVEL', 'DESCRIPTION']

df2.drop(to_drop, inplace=True, axis=1)
df2



#replace minus plus with - +
df2['WATER_LEVEL'] = df2['WATER_LEVEL'].replace({'minus' : '-'}, regex=True)
df2['WATER_LEVEL'] = df2['WATER_LEVEL'].replace({'plus' : '+'}, regex=True)

#eliminate spaces between operator and number
df2['WATER_LEVEL'] = df2['WATER_LEVEL'].str.replace(" ", "")



#transform water level columns from string to float/int
df2['WATER_LEVEL'] = df2['WATER_LEVEL'].astype(int)

df2[['SPOTTED_AT_DATE','SPOTTED_AT_TIME']] = df2.SPOTTED_AT.str.split(' ', expand=True)



import matplotlib.pyplot as plt

#plotting a bar chart: root id - xaxis; number of measures in y axis

x = df2.groupby('ROOT_ID')['ROOT_ID'].count().to_frame()

x.plot.bar()
plt.show()

#visuzlize data in excel
#df2.to_excel("table1.xlsx") 
#x.to_excel("table2.xlsx")

#plot bar chart stations with more than 99 measures

df2=df2[df2.groupby('ROOT_ID')['ROOT_ID'].transform('size') > 99]
z = df2.groupby('ROOT_ID')['ROOT_ID'].count().to_frame().rename(columns = {'ROOT_ID': 'COUNT'})
#df100=z.to_frame()

#df100 = df100.rename(columns={'ROOT_ID': 'COUNT'})
z.plot.bar()
plt.show()

z.sort_values('COUNT', ascending=True).plot.bar()

#time series graphs
WL_date = df2[['ROOT_ID','WATER_LEVEL', "SPOTTED_AT_DATE"]]


# column value in list
root_132084 = ['132084']
a1= WL_date[WL_date['ROOT_ID'].isin(root_132084)]
a1.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_17263 = ['17263']
# a2= WL_date[WL_date['ROOT_ID'].isin(root_17263)]
# a2.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_21368 = ['21368']
# a3= WL_date[WL_date['ROOT_ID'].isin(root_21368)]
# a3.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_219084 = ['219084']
# a4= WL_date[WL_date['ROOT_ID'].isin(root_219084)]
# a4.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_220891 = ['220891']
# a5= WL_date[WL_date['ROOT_ID'].isin(root_220891)]
# a5.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_221750 = ['221750']
# a6= WL_date[WL_date['ROOT_ID'].isin(root_221750)]
# a6.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_233176 = ['233176']
# a7= WL_date[WL_date['ROOT_ID'].isin(root_233176)]
# a7.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_23445 = ['23445']
# a8= WL_date[WL_date['ROOT_ID'].isin(root_23445)]
# a8.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_301198 = ['301198']
# a9= WL_date[WL_date['ROOT_ID'].isin(root_301198)]
# a9.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_35919 = ['35919']
# a10= WL_date[WL_date['ROOT_ID'].isin(root_35919)]
# a10.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_35970 = ['35970']
# a11= WL_date[WL_date['ROOT_ID'].isin(root_35970)]
# a11.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_42809 = ['42809']
# a12= WL_date[WL_date['ROOT_ID'].isin(root_42809)]
# a12.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')

# root_64534 = ['64534']
# a13= WL_date[WL_date['ROOT_ID'].isin(root_64534)]
# a13.plot(x = 'SPOTTED_AT_DATE', y = 'WATER_LEVEL')
    
