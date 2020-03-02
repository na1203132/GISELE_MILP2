# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 12:09:03 2019

@author: Silvia
"""
import pandas as pd
from scipy.spatial import distance_matrix

df=pd.read_csv(r"C:\Users\silvi\Politecnico di Milano\Alessandro Bosisio - Feeder routing\Modello Gisele\Namanjavira.csv")
coords=pd.DataFrame()
coords['X']=df['X']
coords['Y']=df['Y']
Dist_matrix=pd.DataFrame(distance_matrix(coords.values, coords.values), index=df['id'], columns=df['id'])
df.index=df['id']
df=df.assign(Power=0.1) #create new column with absorbed power
#save nodes index
df['id'].to_csv('nodes.csv',index=False)
df.loc['N25','Power']=-4.9
df['Power'].to_csv('power.csv')
#Create dataframe to save allowed connections (evertything but diagonal elements)
connection=pd.DataFrame(columns=['id1','id2','distance'])
k=0
for i, row in Dist_matrix.iterrows():
    for j, column in row.iteritems():
        if column !=0:
            if i<=j:
                connection.loc[k,'id1']=i
                connection.loc[k,'id2']=j
            else:
                connection.loc[k, 'id1'] = j
                connection.loc[k, 'id2'] = i
            connection.loc[k,'distance']=column
            k=k+1
connection.drop_duplicates(inplace=True)
connection[['id1','id2']].to_csv('links.csv',index=False)
connection.to_csv('distances.csv',index=False)

